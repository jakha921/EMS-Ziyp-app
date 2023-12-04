from fastapi import FastAPI, Request, status
from fastapi.exceptions import ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from cities.routers import router as cities_router
from users.routers import router as users_router
from volunteers.routers import router as volunteers_router
from categories.routers import router as categories_router
from products.routers import router as products_router
from orders.routers import router as orders_router
from events.routers import router as events_router
from application_events.routers import router as application_events_router
from grands.routers import router as grands_router
from application_grands.routers import router as application_grands_router
from news.routers import router as news_router
from faqs.routers import router as faqs_router
from aws_media.routers import router as aws_media_router

app = FastAPI(
    title="EMS API",
    version="1.0.0"
)

# CORS settings
origins = [
    "*"
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
]

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# exception handler ValidationError
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


# register routers
routers = [
    aws_media_router,
    cities_router,
    users_router,
    volunteers_router,
    categories_router,
    products_router,
    orders_router,
    events_router,
    application_events_router,
    grands_router,
    application_grands_router,
    news_router,
    faqs_router
]

for router in routers:
    app.include_router(router)
