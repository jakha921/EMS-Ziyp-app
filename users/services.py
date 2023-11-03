from users.models import Users
from services.base_service import BaseServices


class UserServices(BaseServices):
    model = Users
