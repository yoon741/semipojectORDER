from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.service.product import ProductService
from app.service.order import OrderService
from app.model.order import Order
from app.schema.order import OrderCreate, OrderRead


order_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@order_router.get("/order", response_class=HTMLResponse)
async def order(req: Request):
    return templates.TemplateResponse("order/order.html", {"request": req})

# # 주문 생성 API (일반 사용자 및 관리자 공통)
# @order_router.post("/order/", response_model=OrderRead)
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):
#     new_order = Order(**order.dict())
#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)
#     return new_order

@order_router.get("/orderok", response_class=HTMLResponse)
async def orderok(req: Request):
    return templates.TemplateResponse("order/orderok.html", {"request": req})

@order_router.get("/myorder", response_class=HTMLResponse)
async def myorder(req: Request):
    return templates.TemplateResponse("order/myorder.html", {"request": req})
