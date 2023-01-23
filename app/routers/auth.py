from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.settings import JWTSettings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@AuthJWT.load_config
def get_header_type_none():
    return JWTSettings()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/get_headers_access")
def get_headers_access(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return authorize.get_unverified_jwt_headers()


@app.get("/get_headers_refresh")
def get_headers_refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    return authorize.get_unverified_jwt_headers()
