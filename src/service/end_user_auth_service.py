import datetime as dt
import asyncio

from ..common.firebase.firebase_handler import firebase_handler
from ..common.db.model.end_user_model import EndUserModel
from ..repository.end_user_repository import end_user_repository
from ..common.util.logger import get_logger
from ..common.util.error_messages import get_error_message

from pprint import pprint


# TODO: After finishing firebase auth,
#       look up for email verification
#       and password reset

# TODO: Do not forget to implement mongodb hashing.
class EndUserAuthService:
    def __init__(self):
        self._logger = get_logger(__name__)
        self._auth_handler = firebase_handler
        self._end_user_repository = end_user_repository

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
        response: dict
        try:
            response:dict = self._auth_handler.login(email, password)

        except Exception as e:
            self._logger.error(f"Login failed: {e}")
            result.update(
                {
                    "code": 500,
                    "success": False,
                    "message": "Login failed",
                    "error": str(e)
                }
            )
            return result

        if "error" in response:
            self._logger.error(f"Login failed: {response['error']}")
            result.update(
                {
                    "code": response.get("error").get("code"),
                    "success": False,
                    "message": get_error_message(response.get("error").get("errors")[0].get("message")),
                }
            )
        else:
            firebase_user_info: dict = self._auth_handler.get_user_info(email)
            user_info: EndUserModel = asyncio.run(self._end_user_repository.get_one(email))
            result.update(
                {
                    "code": 200,
                    "success": True,
                    "message": "Login successful",
                    "refresh_token": response.get("refreshToken"),
                    "id_token": response.get("idToken"),
                    "data": user_info.model_dump()
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
        response: dict
        try:
            response = self._auth_handler.register(email, password)

        except Exception as e:
            result.update({"message": "Registration failed", "error": str(e)})
            return result

        if "error" in response:
            self._logger.error(f"Registration failed: {response['error']}")
            result.update(
                {
                    "code": response.get("error").get("code"),
                    "success": False,
                    "message": get_error_message(response.get("error").get("message")),
                }
            )

        else:
            # Send verification email
            self._auth_handler.send_verification_email(response.get("idToken"))
            user_info: dict = self._auth_handler.get_user_info(email)
            end_user_model = EndUserModel(
                uid=user_info.get("userUid"),
                created_at=str(dt.datetime.now().isoformat()),
                last_active=str(dt.datetime.now().isoformat()),
                email=email,
                saved_routes=[]
            )
            is_saved: bool = asyncio.run(self._end_user_repository.insert_one(end_user_model.model_dump()))
            result.update(
                {
                    "code": 200,
                    "success": True,
                    "message": "Registration successful",
                    "refresh_token": response.get("refreshToken"),
                    "id_token": response.get("idToken"),
                    "data": end_user_model.model_dump()
                }
            )
        return result

    def logout(
            self,
            user_uid: str
    ) -> bool:
        try:
            logout_result: bool = self._auth_handler.logout(user_uid)

        except Exception as e:
            print("Error: ", e)
            return False

        return True

    def delete_account(
            self,
            user_uid: str
    ) -> bool:
        self._logger.info(f"Delete account request for {user_uid}")
        try:
            self._auth_handler.delete_user(user_uid)
            asyncio.run(self._end_user_repository.delete_one_by_uid(user_uid))

        except Exception as e:
            self._logger.error(f"Delete account failed: {e}")
            return False

        return True

    def validate_token(
            self,
            token: str
    ) -> bool:
        result: bool = self._auth_handler.validate_token(token)
        return result


end_user_auth_service = EndUserAuthService()