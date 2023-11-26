from news.models import News
from base.base_service import BaseServices


class NewsServices(BaseServices):
    model = News
    search_fields = [
        "name_ru",
        "name_en",
        "name_uz",
        "description_ru",
        "description_en",
        "description_uz"
    ]
