from application_grands.models import ApplicationGrands
from base.base_service import BaseServices


class ApplicationGrandsServices(BaseServices):
    model = ApplicationGrands
    load_relations = ["users", "grands"]
