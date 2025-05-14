from ..common.base.repository_base_class import RepositoryBaseClass
from ..common.db.model.bus_location_model import BusLocationModel
from ..common.db.model.end_user_model import EndUserModel
from ..common.db.model.journal_model import JournalModel
from ..common.db.model.driver_user_model import DriverUserModel
from ..common.db.model.route_model import RouteModel
from ..repository.end_user_repository import end_user_repository
from ..repository.journal_repository import journal_repository
from ..repository.route_repository import route_repository
from ..common.util.logger import get_logger


class EndUserService:
    def __init__(self):
        self._logger = get_logger(__name__)
        self._end_user_repository = end_user_repository
        self._journal_repository = journal_repository
        self._route_repository = route_repository

    async def get_passenger_information(
            self,
            uid: str
    ) -> dict:
        self._logger.info(f"Get passenger information for {uid}")
        result: dict = {"code": 200, "success": False, "message": "", "data": {}, "error": ""}
        user_data: EndUserModel = await self._end_user_repository.get_one_by_uid(uid)
        saved_routes: list = []
        refined_data: dict
        if not user_data:
            result.update({"code": 404, "message": "Böyle bir kullanıcı bulunmamakta", "error": ""})
            return result
        # Check if saved routes is not empty:
        if len(user_data.saved_routes) != 0:
            for i in user_data.saved_routes:
                _: RouteModel = await self._route_repository.get_one_by_uuid(i)
                if _:
                    saved_routes.append(_.model_dump())
        refined_data = {"email": user_data.email, "first_name": user_data.first_name,
                        "last_name": user_data.last_name, "saved_routes": saved_routes}
        result.update({"success": True, "message": "Kullanıcı bilgileri başarıyla alındı", "data": refined_data})
        return result

    async def get_all_routes(self) -> dict:
        self._logger.info("Getting all routes")
        result: dict = {"code": 0, "success": False, "message": "", "error": "", "data": {}}
        routes: list[RouteModel] = await self._route_repository.get_all()
        if not routes:
            result.update({"code": 200, "success": True, "message": "Herhangi bir rota bulunmamakta",
                           "data": {"routes": []}})
            return result
        result.update({"code": 200, "success": True, "message": "Routes retrieved successfully",
                       "data": {"routes": [route.model_dump() for route in routes]}})
        return result
    
    async def get_all_active_journeys(self) -> dict:
        self._logger.info("Getting all active journeys")
        result: dict = {"code": 0, "success": False, "message": "", "error": "", "data": {}}
        active_journeys: list[JournalModel] = await self._journal_repository.get_all_active_journeys()
        refined_data: list[dict] = []
        if len(active_journeys) == 0:
            result.update({"code": 200, "success": True, "message": "Herhangi bir aktif yolculuk bulunmamakta",
                           "data": {"active_journeys": []}})
            return result
        result.update({"code": 200, "success": True, "message": "Aktif yolculuklar başarıyla alındı",
                       "data": {"active_journeys": [journey.model_dump(exclude={"locations"}) for journey in active_journeys]}})
        return result

    # TODO: Bu demo için, buraya daha sonra google distance servisi eklenecek
    # TODO: Hem bundaki hem de şoförün konum gönderdiği yerlerde web socket disconnect
    #       olması için bazı koşullarda exception raise edebilirsin.
    async def fetch_vehicle_location(
            self,
            journal_uuid: str,
    ) -> dict:
        self._logger.info(f"Fetching vehicle location for journal_uuid: {journal_uuid}")
        result: dict = {"code": 0, "success": False, "message": "", "error": "", "data": {}}
        journal: JournalModel = await self._journal_repository.get_active_one_by_uuid(journal_uuid)
        if not journal:
            result.update({"code": 404, "success": False, "message": "Böyle bir yolculuk bulunmamakta", "error": ""})
            return result
        if len(journal.locations) == 0:
            result.update({"code": 404, "success": False, "message": "There isn't any location yet.", "error": ""})
            return result
        last_location: BusLocationModel = journal.locations[-1]
        result.update({"code": 200, "success": True, "message": "Konum başarıyla alındı",
                       "data": {"current_location": last_location.model_dump()}})
        return result


end_user_service = EndUserService()