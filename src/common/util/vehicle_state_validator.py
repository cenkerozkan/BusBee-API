from ...repository.journal_repository import journal_repository
from .logger import get_logger

logger = get_logger(__name__)

async def validate_vehicle_state(
        vehicle_uuid: str = None,
        driver_uid: str = None,
        plate_number: str = None
) -> bool:
    is_vehicle_on_route: bool = False
    logger.info(f"Checking vehicle state for vehicle_uuid: {vehicle_uuid}")
    if driver_uid is not None:
        is_vehicle_on_route = await journal_repository.is_vehicle_active(driver_uid=driver_uid)
    if vehicle_uuid is not None:
        is_vehicle_on_route = await journal_repository.is_vehicle_active(vehicle_uuid=vehicle_uuid)
    if plate_number is not None:
        is_vehicle_on_route = await journal_repository.is_vehicle_active(plate_number=plate_number)
    if vehicle_uuid is None and driver_uid is None and plate_number is None:
        raise ValueError("Either vehicle_uuid or driver_uid must be provided, not both.")
    return is_vehicle_on_route