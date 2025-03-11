from fastapi import HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pprint import pprint

from ..common.meta.singleton_meta import SingletonMeta
from ..common.firebase.firebase_handler import FirebaseHandler
from ..common.response_model.response_model import ResponseModel
from ..common.logger import get_logger


# TODO: After finishing firebase auth,
#       look up for email verification
#       and password reset

# TODO: Do not forget to implement mongodb hashing.
class EndUserAuthService(metaclass=SingletonMeta):
    def __init__(self):
        self._auth_handler = FirebaseHandler()
        self._logger = get_logger(__name__)

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
            if "error" in response:
                result.update(
                    {
                        "code": response.get("error").get("code"),
                        "success": False,
                        "message": response.get("error").get("errors")[0].get("message"),
                    }
                )
            else:
                user_info: dict = self._auth_handler.get_user_info(email)
                result.update(
                    {
                        "code": 200,
                        "success": True,
                        "message": "Login successful",
                        "refresh_token": response.get("refreshToken"),
                        "id_token": response.get("idToken"),
                        "data": user_info
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
        response: dict = {}
        try:
            response = self._auth_handler.register(email, password)

        except Exception as e:
            result.update({"message": "Registration failed", "error": str(e)})
            return result

        if "error" in response:
            result.update(
                {
                    "code": response.get("error").get("code"),
                    "success": False,
                    "message": response.get("error").get("message"),
                }
            )
        else:
            # Send verification email
            self._auth_handler.send_verification_email(response.get("idToken"))
            # Then add background task to delete unverified email
            background_tasks.add_task(self._auth_handler.delete_unverified_email, email)

            user_info: dict = self._auth_handler.get_user_info(email)
            result.update(
                {
                    "code": 200,
                    "success": True,
                    "message": "Registration successful",
                    "refresh_token": response.get("refreshToken"),
                    "id_token": response.get("idToken"),
                    "data": user_info
                }
            )
        return result

    def logout(
            self,
            user_uid: str
    ) -> bool:
        try:
            logout_result: bool = self._auth_handler.logout(user_uid)
            return True
        except Exception as e:
            print("Error: ", e)
            return False

    def validate_token(
            self,
            token: str
    ) -> bool:
        result: bool = self._auth_handler.validate_token(token)
        return result