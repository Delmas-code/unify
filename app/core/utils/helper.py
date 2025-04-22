from app.core.utils.loggers import setup_logger
from bson import ObjectId, errors as bson_errors

logger = setup_logger("core/utils/helper", "logs/core_utils.log")

def stringify_id(obj_id: ObjectId) -> str:
    """
    Convert an ObjectId to a string.
    """
    try:
        return str(obj_id)
    except Exception as e:
        logger.error(f"Error converting ObjectId to string: {e}")
        return None

def parse_object_id(obj_id: str) -> ObjectId:
    """
    Convert a string to an ObjectId.
    """
    try:
        return ObjectId(obj_id)
    except bson_errors.InvalidId:
        logger.error(f"Error converting string to ObjectId: {obj_id}")
        return None