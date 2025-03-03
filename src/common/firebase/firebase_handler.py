"""
This is the class responsible from communicating
with the firebase authentication service.
"""
from ..meta.singleton_meta import SingletonMeta

from fastapi import HTTPException
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin.auth import *
import os

class AuthHandler(metaclass=SingletonMeta):
    def __init__(self):
        self.cred: credentials.Certificate = credentials.Certificate(
            {
                "type": os.getenv("TYPE"),
                "project_id": os.getenv("PROJECT_ID"),
                "private_key_id": os.getenv("PRIVATE_KEY_ID"),
                "private_key": os.getenv("PRIVATE_KEY"),
                "client_email": os.getenv("CLIENT_EMAIL"),
                "client_id": os.getenv("CLIENT_ID"),
                "auth_uri": os.getenv("AUTH_URI"),
                "token_uri": os.getenv("TOKEN_URI"),
                "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
                "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
                "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
            }
        )
        self.app = firebase_admin.initialize_app(self.cred)

    def login(
            self,
            email: str,
            password: str
    ) -> str:
        user = auth.get_user_by_email(email)
        custom_token = auth.create_custom_token(user.uid)
        return custom_token.decode()



    def register(self, email: str, password: str):
        user: UserRecord = auth.create_user(
            email=email,
            password=password,
            email_verified=False
        )

    def validate_token(self):
        pass