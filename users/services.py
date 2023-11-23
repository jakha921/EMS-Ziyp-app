from users.models import Users
from base.base_service import BaseServices


class UserServices(BaseServices):
    model = Users
    load_relations = [
        "cities"
    ]
