import uuid

from app.config import jwt_settings
from app.database import get_session
from app.models.ratings import Rating as m_Rating
from app.schemas.rating import CreateRating, Rating
from app.utils.exceptions import get_product_or_404, get_user_or_404
from app.utils.messages import messages
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/products/ratings",
    tags=["ratings"],
    responses={404: {"description": "Not found"}},
)
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.get(
    "/get/{product_id}/",
    status_code=status.HTTP_200_OK,
    summary="Получение всех оценок продуктов по guid",
)
async def get_product_ratings(product_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    product = await get_product_or_404(guid=product_id, session=session)
    ratings = await m_Rating.filter(product_id=product.guid, session=session)
    return [Rating.from_orm(rating).dict() for rating in ratings] if ratings else None


@router.get(
    "/get/avg/{product_id}/",
    status_code=status.HTTP_200_OK,
    summary="Получение среднего рейтинга продукта по guid",
)
async def get_product_avg_rating(product_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    product = await get_product_or_404(guid=product_id, session=session)
    return {"avg_rating": product.avg_rating}


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
    if await m_Rating.get(session=session, user_id=user.guid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.RATING_ALREADY_EXISTS,
        )
    product = await get_product_or_404(guid=create_rating.product_id, session=session)
    await m_Rating(product_id=product.guid, user_id=user.guid, stars=create_rating.stars).create(session=session)
    product.upgrade_rating(rating=create_rating.stars)
    await product.update(session=session)
    return {"detail": messages.RATING_CREATED}
