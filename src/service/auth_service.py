from fastapi import HTTPException
from fastapi.responses import JSONResponse

from ..common.meta.singleton_meta import SingletonMeta
from ..common.firebase.firebase_handler import AuthHandler
from ..common.response_model.response_model import ResponseModel


class AuthService(metaclass=SingletonMeta):
    def __init__(self):
        self._auth_handler = AuthHandler()

    def login(
            self,
            email: str,
            password: str
    ) -> dict:
        result: dict = {
            "message": "",
            "token": "",
            "error": ""
        }
        try:
            token:str = self._auth_handler.login(email, password)
            result.update({"message": "Login successful", "token": f"{token}"})
            return result
        except Exception as e:
            result.update({"message": "Login failed", "error": str(e)})
            return result


    def register(
            self,
            email: str,
            password: str
    ) -> str:
        return self._auth_handler.register(email, password)