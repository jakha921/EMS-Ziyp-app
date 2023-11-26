from grands.models import Grands
from base.base_service import BaseServices


class GrandsServices(BaseServices):
    model = Grands
    search_fields = [
        "name_ru",
        "name_en",
        "name_uz",
        "description_ru",
        "description_en",
        "description_uz",
    ]
