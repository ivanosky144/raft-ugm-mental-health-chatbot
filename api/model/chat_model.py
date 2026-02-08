from bson import ObjectId
from datetime import datetime, timezone

class Chat:
    def __init__(self, summary="", excel_file_path="", start_time=None, end_time=None, valid=True, user_id=None, _id=None):
        self._id = _id or ObjectId()
        self.summary = summary
        self.excel_file_path = excel_file_path
        self.start_time = start_time or datetime.now(timezone.utc)
        self.end_time = end_time
        self.valid = valid
        self.user_id = user_id

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return Chat(**data)