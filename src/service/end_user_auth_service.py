from ..common.meta.singleton_meta import SingletonMeta
from ..common.firebase.firebase_handler import FirebaseHandler
from ..common.db.model.end_user_model import EndUserModel
from ..repository.end_user_repository import EndUserRepository
from src.common.util.logger import get_logger


# TODO: After finishing firebase auth,
#       look up for email verification
#       and password reset

# TODO: Do not forget to implement mongodb hashing.
class EndUserAuthService(metaclass=SingletonMeta):
    def __init__(self):
        self._logger = get_logger(__name__)
        self._auth_handler = FirebaseHandler()
        self._end_user_repository = EndUserRepository()

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

        except Exception as e:
            print("Error: ", e)
            return False

        return True

    def validate_token(
            self,
            token: str
    ) -> bool:
        result: bool = self._auth_handler.validate_token(token)
        return result