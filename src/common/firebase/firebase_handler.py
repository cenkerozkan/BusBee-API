"""
This is the class responsible from communicating
with the firebase authentication service.
"""
import time

import requests

from ..meta.singleton_meta import SingletonMeta
from src.common.util.logger import get_logger

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin.auth import *
import os

class FirebaseHandler(metaclass=SingletonMeta):
    def __init__(
            self
    ):
        self._cred: credentials.Certificate = credentials.Certificate(
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
        self._app: firebase_admin = firebase_admin.initialize_app(self._cred)
        self._api_key: str = os.getenv("WEB_API_KEY")
        self._logger = get_logger(__name__)

    def _post_request_executor(
            self,
            payload: dict,
            endpoint: str
    ) -> dict:
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:{endpoint}?key={self._api_key}",
            json=payload
        )
        return response.json()

    def get_user_info(
            self,
            email: str
    ) -> dict:
        user_details = auth.get_user_by_email(email, app=self._app)
        return {
            "userUid": user_details.uid,
            "email": user_details.email,
            "emailVerified": user_details.email_verified,
        }

    def login(
            self,
            email: str,
            password: str
    ) -> dict:
        response: dict = self._post_request_executor({"email": email, "password": password, "returnSecureToken": True}, "signInWithPassword")
        return response

    def logout(
            self,
            user_uid: str
    ) -> bool:
        auth.revoke_refresh_tokens(user_uid, app=self._app)
        return True

    def register(
            self,
            email: str,
            password: str
    ) -> dict:
        # NOTE: We can also get username for this method.
        response = self._post_request_executor({"email": email, "password": password, "returnSecureToken": True}, "signUp")

        return response

    def delete_unverified_email(
            self,
            email: str
    ) -> None:
        self._logger.info(f"Waiting for 5 minutes to delete unverified email: {email}")
        time.sleep(5)
        user: UserRecord = auth.get_user_by_email(email)
        if not user.email_verified:
            auth.delete_user(user.uid)

    def send_verification_email(
            self,
            user_uid: str
    ) -> dict:
        response = self._post_request_executor({"requestType": "VERIFY_EMAIL", "idToken": user_uid}, "sendOobCode")
        return response


    def validate_token(
            self,
            token: str
    ) -> bool:
        try:
            decoded_token = auth.verify_id_token(token)
            return True
        except (auth.InvalidIdTokenError, auth.ExpiredIdTokenError, auth.RevokedIdTokenError):
            return False
        except Exception:
            return False