from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pprint import pprint

from ..common.meta.singleton_meta import SingletonMeta
from ..common.firebase.firebase_handler import FirebaseHandler
from ..common.response_model.response_model import ResponseModel


# TODO: After finishing firebase auth,
#       look up for email verification
#       and password reset

# TODO: Do not forget to implement mongodb hashing.
class AuthService(metaclass=SingletonMeta):
    def __init__(self):
        self._auth_handler = FirebaseHandler()

    def login(
            self,
            email: str,
            password: str
    ) -> dict:
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "refresh_token": "",
            "id_token":"",
            "error": "",
            "data": {}
        }
        try:
            response:dict = self._auth_handler.login(email, password)
            pprint(response)
            if "error" in response:
                result.update(
                    {
                        "code": response.get("error").get("code"),
                        "success": False,
                        "message": response.get("error").get("errors")[0].get("message"),
                    }
                )
            else:
                result.update(
                    {
                        "code": 200,
                        "success": True,
                        "message": "Login successful",
                        "refresh_token": response.get("refreshToken"),
                        "id_token": response.get("idToken"),
                    }
                )

            return result

        except Exception as e:
            result.update(
                {
                    "code": 500,
                    "success": False,
                    "message": "Login failed",
                    "error": str(e)
                }
            )
            return result


    def register(
            self,
            email: str,
            password: str
    ) -> dict:
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "refresh_token": "",
            "id_token": "",
            "error": "",
            "data": {}
        }
        try:
            response:dict = self._auth_handler.register(email, password)
            pprint(response)
            if "error" in response:
                result.update(
                    {
                        "code": response.get("error").get("code"),
                        "success": False,
                        "message": response.get("error").get("errors")[0].get("message"),
                    }
                )
            else:
                result.update(
                    {
                        "code": 200,
                        "success": True,
                        "message": "Registration successful",
                        "refresh_token": response.get("refreshToken"),
                        "id_token": response.get("idToken"),
                    }
                )
            return result

        except Exception as e:
            result.update({"message": "Registration failed", "error": str(e)})
            return result

    def validate_token(
            self,
            token: str
    ) -> bool:
        result: bool = self._auth_handler.validate_token(token)
        return result