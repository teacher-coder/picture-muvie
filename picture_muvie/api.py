from ninja import NinjaAPI
from makedocx.api import router as makedocx_router

api = NinjaAPI()

api.add_router("/makedocx", makedocx_router)
