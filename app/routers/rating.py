import uuid

from app.config import jwt_settings
from app.database import get_session
from app.models.products import Product as m_Product
from app.models.rating import Rating as m_Rating
from app.schemas.rating import CreateRating, Rating
from app.utils.exceptions import get_user_or_404
from app.utils.messages import messages
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/products/rating",
    tags=["ratings"],
    responses={404: {"description": "Not found"}},
)
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.get(
    "/get/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Получение всех оценок продуктов по id",
)
async def get_product_ratings(product_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    if not (product := await m_Product.get(product_id=product_id, session=session)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.PRODUCT_NOT_FOUND)
    ratings = product.ratings
    return [Rating.from_orm(rating).dict() for rating in ratings] if ratings else None


@router.post("/new/", status_code=status.HTTP_201_CREATED, summary="Добавление новой оценки")
async def create_new_ratings(
    create_rating: CreateRating,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    if await m_Rating.get(session=session, author=user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.RATING_ALREADY_EXISTS,
        )
    if not (product := await m_Product.get(product_id=create_rating.product_id, session=session)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.PRODUCT_NOT_FOUND)
    await m_Rating(product=product, author=user, stars=create_rating.stars).create(session=session)
    return {"detail": messages.RATING_CREATED}
