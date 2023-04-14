from app.config import jwt_settings
from app.database import get_session
from app.models.orders import Order as m_Order
from app.models.orders import OrderItem as m_OrderItem
from app.schemas.orders import ShowOrderItem
from app.utils.exceptions import get_user_or_404
from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/orders", tags=["orders"], responses={404: {"description": "Not found"}})
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.get(
    "/get/",
    status_code=status.HTTP_200_OK,
    summary="Получение заказов пользователя",
)
async def get_orders(
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    orders = await m_Order.filter(session=session, user_id=user.guid)
    order_guids = [order.guid for order in orders]
    orders = []
    for guid in order_guids:
        items = await m_OrderItem.get_items(session, order_id=guid)
        [ShowOrderItem.from_orm(order_item).dict() for order_item in items] if items else None
    # return [Product.from_orm(product).dict() for product in products] if products else None
