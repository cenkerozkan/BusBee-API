import datetime as dt
import asyncio

from ..common.firebase.firebase_handler import firebase_handler
from ..common.db.model.end_user_model import EndUserModel
from ..repository.end_user_repository import end_user_repository
from ..common.util.logger import get_logger
from ..common.util.error_messages import get_error_message

from pprint import pprint



class EndUserAuthService:
    __slots__ = ("_logger", "_firebase_handler", "_end_user_repository")
    def __init__(self):
        self._logger = get_logger(__name__)
        self._firebase_handler = firebase_handler
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
            response:dict = self._firebase_handler.login(email, password)

        except Exception as e:
            self._logger.error(f"Login failed: {e}")
            result.update({"code": 500, "success": False, "message": "Login failed", "error": str(e)})
            return result

        if "error" in response:
            self._logger.error(f"Login failed: {response['error']}")
            result.update({"code": response.get("error").get("code"), "success": False, "message": get_error_message(response.get("error").get("errors")[0].get("message"))})
        else:
            firebase_user_info: dict = self._firebase_handler.get_user_info(email)
            user_info: EndUserModel = asyncio.run(self._end_user_repository.get_one(email))
            result.update({"code": 200, "success": True, "message": "Login successful", "refresh_token": response.get("refreshToken"), "id_token": response.get("idToken"), "data": user_info.model_dump()})
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
            response = self._firebase_handler.register(email, password)

        except Exception as e:
            result.update({"message": "Registration failed", "error": str(e)})
            return result

        if "error" in response:
            self._logger.error(f"Registration failed: {response['error']}")
            result.update({"code": response.get("error").get("code"), "success": False, "message": get_error_message(response.get("error").get("message"))})

        else:
            # Send verification email
            self._firebase_handler.send_verification_email(response.get("idToken"))
            user_info: dict = self._firebase_handler.get_user_info(email)
            end_user_model = EndUserModel(
                uid=user_info.get("userUid"),
                created_at=str(dt.datetime.now().isoformat()),
                last_active=str(dt.datetime.now().isoformat()),
                email=email,
            )
            is_saved: bool = asyncio.run(self._end_user_repository.insert_one(end_user_model.model_dump()))
            result.update({
                    "code": 200,
                    "success": True,
                    "message": "Registration successful",
                    "refresh_token": response.get("refreshToken"),
                    "id_token": response.get("idToken"),
                    "data": end_user_model.model_dump()
                })
        return result

    def delete_account(
            self,
            user_uid: str
    ) -> bool:
        self._logger.info(f"Delete account request for {user_uid}")
        try:
            self._firebase_handler.delete_user(user_uid)
            asyncio.run(self._end_user_repository.delete_one_by_uid(user_uid))

        except Exception as e:
            self._logger.error(f"Delete account failed: {e}")
            return False

        return True

    def validate_token(
            self,
            token: str
    ) -> bool:
        result: bool = self._firebase_handler.validate_token(token)
        return result

    async def create_account(
            self,
            uid: str,
            email: str,
            first_name: str,
            last_name: str
    ) -> dict:
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "data": {},
            "error": ""
        }
        crud_result: bool = False
        new_user_model: EndUserModel = EndUserModel(
            uid=uid,
            created_at=str(dt.datetime.now().isoformat()),
            last_active=str(dt.datetime.now().isoformat()),
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        crud_result = await self._end_user_repository.insert_one(new_user_model.model_dump())
        result.update({"code": 500, "success": False, "message": "Failed to create account", "error": "Failed to create account"} if not crud_result else {"code": 200, "success": True, "message": "Account created successfully", "data": new_user_model.model_dump()})
        return result

end_user_auth_service = EndUserAuthService()
