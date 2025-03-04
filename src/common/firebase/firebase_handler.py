"""
This is the class responsible from communicating
with the firebase authentication service.
"""
import requests

from ..meta.singleton_meta import SingletonMeta

from fastapi import HTTPException
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin.auth import *
import os

class FirebaseHandler(metaclass=SingletonMeta):
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
        self._api_key = os.getenv("WEB_API_KEY")

    def _request_executor(
            self,
            email: str,
            password: str,
            endpoint: str
    ) -> dict:
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:{endpoint}?key={self._api_key}",
            json={"email": email, "password": password, "returnSecureToken": True}
        )
        return response.json()

    def login(
            self,
            email: str,
            password: str
    ) -> dict:
        response: dict = self._request_executor(email, password, "signInWithPassword")
        return response


    def register(
            self,
            email: str,
            password: str
    ) -> dict:
        response = self._request_executor(email, password, "signUp")
        return response

    def validate_token(self):
        pass