
from fastapi import FastAPI, HTTPException, status
import uvicorn
from core import conf, rabbit_broker
from authorization import router_authorization
from shop import router_shop
from shop.exceptions import ShopNotFoundException
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_broker.start()
    yield
    await rabbit_broker.stop()

app = FastAPI(title='Delivery service',
              lifespan=lifespan)

app.include_router(router_authorization)
app.include_router(router_shop)



@app.exception_handler(ShopNotFoundException)
async def shop_not_found(request, exc):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=str(exc))


def main():
    uvicorn.run(app=app,
                host=conf.app.host,
                port=conf.app.port)



if __name__ == '__main__':
    main()

