import datetime as dt
import asyncio

from ..common.meta.singleton_meta import SingletonMeta
from ..common.firebase.firebase_handler import FirebaseHandler
from ..common.db.model.admin_user_model import AdminUserModel
from ..repository.admin_user_repository import AdminUserRepository
from ..common.util.logger import get_logger
from ..common.util.error_messages import get_error_message

from pprint import pprint


# TODO: After finishing firebase auth,
#       look up for email verification
#       and password reset

class AdminUserAuthService(metaclass=SingletonMeta):
    def __init__(self):
        self._logger = get_logger(__name__)
        self._auth_handler = FirebaseHandler()
        self._admin_user_repository = AdminUserRepository()

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
            user_info: AdminUserModel = asyncio.run(self._admin_user_repository.get_one(email))
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
    ):
        self._logger.info(f"Delete account request for {user_uid}")
        try:
            self._auth_handler.delete_user(user_uid)
            asyncio.run(self._admin_user_repository.delete_one_by_uid(user_uid))

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

    def add_admin_user(
            self,
            email: str,
            password: str
    ) -> dict:
        self._logger.info(f"Add admin user request for {email}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        response: dict = {}
        is_saved: bool

        try:
            response = self._auth_handler.create_admin_user(email, password)

        except Exception as e:
            self._logger.error(f"Failed to add admin user: {e}")
            result.update({"code": 500, "success": False, "message": "Failed to add admin user", "error": str(e)})

        if response:
            new_admin_user: AdminUserModel = AdminUserModel(
                uid=response.get("uid"),
                email=email,
                created_at=str(dt.datetime.now().isoformat()),
                last_active=str(dt.datetime.now().isoformat())
            )
            is_saved: bool = asyncio.run(self._admin_user_repository.insert_one(new_admin_user.model_dump()))
            result.update(
                {
                    "code": 200,
                    "success": True,
                    "message": "Admin user added",
                    "data": new_admin_user.model_dump()
                }
            )

        return result

    def remove_admin_user(
            self,
            user_uid: str
    ) -> dict:
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        firebase_response: bool

        try:
            firebase_response = self._auth_handler.delete_user(user_uid)
            is_deleted: bool = asyncio.run(self._admin_user_repository.delete_one_by_uid(user_uid))

        except Exception as e:
            self._logger.error(f"Failed to remove admin user: {e}")
            result.update({"code": 500, "success": False, "message": "Failed to remove admin user", "error": str(e)})

        if firebase_response and is_deleted:
            result.update(
                {
                    "code": 200,
                    "success": True,
                    "message": "Admin user removed"
                }
            )
        return result