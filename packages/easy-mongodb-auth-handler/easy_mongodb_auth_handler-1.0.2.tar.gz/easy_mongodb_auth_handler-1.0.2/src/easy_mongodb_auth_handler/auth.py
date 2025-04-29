"""
Authentication and user management for the easy_mongodb_auth_handler package.
"""

from pymongo import MongoClient
from .utils import (
    validate_email,
    hash_password,
    verify_password,
    generate_secure_code,
    send_verification_email,
)


class Auth:
    """
    Handles user authentication and management using MongoDB.
    """

    def __init__(self, mongo_uri, db_name, mail_info=None):
        """
        initializes the Auth class

        Args:
            mongo_uri (str): MongoDB connection URI.
            db_name (str): Name of the database.
            mail_info (dict, optional): Email server configuration with keys:
                'server', 'port', 'username', 'password'.
        """
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.users = self.db["users"]
        self.mail_info = mail_info or {}

    def register_user_no_verif(self, email, password):
        """
        registers a user without email verification

        Args:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            dict: Success status and message.
        """
        if not validate_email(email):
            return {"success": False, "message": "Invalid email format."}
        if self.users.find_one({"email": email}):
            return {"success": False, "message": "User already exists."}

        hashed_password = hash_password(password)
        self.users.insert_one(
            {"email": email, "password": hashed_password, "verified": True}
        )
        return {"success": True, "message": "User registered without verification."}

    def reset_password_no_verif(self, email, old_password, new_password):
        """
        resets a user's password without email verification

        Args:
            email (str): User's email address.
            old_password (str): User's current password.
            new_password (str): New password.

        Returns:
            dict: Success status and message.
        """
        user = self.users.find_one({"email": email})
        if not user:
            return {"success": False, "message": "User not found."}
        if not verify_password(old_password, user["password"]):
            return {"success": False, "message": "Invalid old password."}

        hashed_password = hash_password(new_password)
        self.users.update_one({"email": email}, {"$set": {"password": hashed_password}})
        return {"success": True, "message": "Password reset successful."}

    def register_user(self, email, password):
        """
        registers a user with email verification

        Args:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            dict: Success status and message.
        """
        if not validate_email(email):
            return {"success": False, "message": "Invalid email format."}
        if self.users.find_one({"email": email}):
            return {"success": False, "message": "User already exists."}

        hashed_password = hash_password(password)
        verification_code = generate_secure_code()
        self.users.insert_one(
            {
                "email": email,
                "password": hashed_password,
                "verified": False,
                "verification_code": verification_code,
            }
        )
        send_verification_email(self.mail_info, email, verification_code)
        return {"success": True, "message": "User registered. Verification email sent."}

    def verify_user(self, email, code):
        """
        Verifies a user's email using a verification code.

        Args:
            email (str): User's email address.
            code (str): Verification code.

        Returns:
            dict: Success status and message.
        """
        user = self.users.find_one({"email": email})
        if not user:
            return {"success": False, "message": "User not found."}
        if user["verification_code"] == code:
            self.users.update_one({"email": email}, {"$set": {"verified": True}})
            return {"success": True, "message": "User verified."}
        return {"success": False, "message": "Invalid verification code."}

    def authenticate_user(self, email, password):
        """
        authenticates a user

        Args:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            dict: Success status and message.
        """
        user = self.users.find_one({"email": email})
        if not user:
            return {"success": False, "message": "User not found."}
        if not user["verified"]:
            return {"success": False, "message": "User not verified."}
        if verify_password(password, user["password"]):
            return {"success": True, "message": "Authentication successful."}
        return {"success": False, "message": "Invalid credentials."}

    def delete_user(self, email, password):
        """
        deletes a user account

        Args:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            dict: Success status and message.
        """
        user = self.users.find_one({"email": email})
        if not user:
            return {"success": False, "message": "User not found."}
        if not verify_password(password, user["password"]):
            return {"success": False, "message": "Invalid password."}

        result = self.users.delete_one({"email": email})
        if result.deleted_count > 0:
            return {"success": True, "message": "User deleted."}
        return {"success": False, "message": "Failed to delete user."}

    def generate_reset_code(self, email):
        """
        Generates a password reset code and sends it to the user's email.

        Args:
            email (str): User's email address.

        Returns:
            dict: Success status and message.
        """
        user = self.users.find_one({"email": email})
        if not user:
            return {"success": False, "message": "User not found."}

        reset_code = generate_secure_code()
        self.users.update_one({"email": email}, {"$set": {"reset_code": reset_code}})
        send_verification_email(self.mail_info, email, reset_code)
        return {"success": True, "message": "Reset code sent to email."}

    def verify_reset_code_and_reset_password(self, email, reset_code, new_password):
        """
        verifies a reset code and resets the user's password

        Args:
            email (str): User's email address.
            reset_code (str): Reset code.
            new_password (str): New password.

        Returns:
            dict: Success status and message.
        """
        user = self.users.find_one({"email": email})
        if not user:
            return {"success": False, "message": "User not found."}
        if user.get("reset_code") != reset_code:
            return {"success": False, "message": "Invalid reset code."}

        hashed_password = hash_password(new_password)
        self.users.update_one(
            {"email": email}, {"$set": {"password": hashed_password, "reset_code": None}}
        )
        return {"success": True, "message": "Password reset successful."}
