from fastapi import FastAPI
import uvicorn
from core import conf


app = FastAPI(title='Delivery service')

def main():
    uvicorn.run(app=app,
                host=conf.app.host,
                port=conf.app.port)



if __name__ == '__main__':
    main()

