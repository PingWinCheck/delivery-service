from fastapi import FastAPI
import uvicorn
from core import conf
from authorization import router_authorization

app = FastAPI(title='Delivery service')

app.include_router(router_authorization)

def main():
    uvicorn.run(app=app,
                host=conf.app.host,
                port=conf.app.port)



if __name__ == '__main__':
    main()

