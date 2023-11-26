#
# FastAPI is a framework and library for implementing REST web services in Python.
# https://fastapi.tiangolo.com/
#
from fastapi import FastAPI, Response, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from typing import Annotated, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from typing import List, Union

# I like to launch directly and not use the standard FastAPI startup process.
# So, I include uvicorn
import uvicorn

from resources.order_resource import OrdersResource
from resources.order_data_service import OrderDataService
from resources.order_models import OrderModel, OrderRspModel
import time
# from resources.schools.school_models import SchoolRspModel, SchoolModel
# from resources.schools.schools_resource import SchoolsResource
from jose import JWTError, jwt
from utils import *
import requests

JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRE_TIME = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("orderid")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/GETTIME")
def external_api():
    url = "https://www.timeapi.io/api/Time/current/zone?timeZone=America/New_York"
    res = requests.get(url).json()
    print("Year:",res['year'])
    print("Month:",res['month'])
    print("Day:",res['day'])
    print(f"Time:{res['hour']}:{res['minute']}:{res['seconds']}")
    return res
    

@app.post("/token")
def generate_jwt_token(user_id: int)->str:
    """根据用户id生成token"""
    payload = {'user_id': user_id, 'exp': int(time.time()) + JWT_TOKEN_EXPIRE_TIME}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# ******************************
#
# DFF TODO Show the class how to do this with a service factory instead of hard code.


def get_data_service():

    config = {
        "data_directory": "./data",
        "data_file": "orders.json"
    }

    ds = OrderDataService(config)
    return ds


def get_order_resource():
    ds = get_data_service()
    config = {
        "data_service": ds
    }
    res = OrdersResource(config)
    return res


orders_resource = get_order_resource()

# schools_resource = OrdersResource(config={"orders_resource": students_resource})


#
# END TODO
# **************************************


@app.get("/")
async def root():
    return 'Hello, from EC2! I am Tapioca Order Management Service.'
    # return RedirectResponse("/static/index.html")

@app.get("/ordercount")
async def count_orders():
    res = orders_resource.count_orders()
    return {"message": "%d Orders"% res}


@app.get("/orders", response_model=List[OrderRspModel])
async def get_orders(OrderID: Annotated[str, Depends(get_current_user)]):
    """
    Return a list of students matching a query string.

    - **uni**: student's UNI
    - **last_name**: student's last name
    - **school_code**: student's school.
    """
    result = orders_resource.get_orders(OrderID)
    return result

@app.get("/orders/{OrderID}", response_model=List[OrderRspModel])
async def get_orders(OrderID:str):
    """
    Return a list of students matching a query string.

    - **uni**: student's UNI
    - **last_name**: student's last name
    - **school_code**: student's school.
    """
    result = orders_resource.get_orders(OrderID)
    return result

@app.post("/orders", response_model=OrderModel)
async def post_orders(item: OrderModel):
    orders_resource.post_orders(item)
    topic_arn = 'arn:aws:sns:us-east-1:504795767363:sent'
    message = 'Hello, this is a test message!'
    subject = 'Test Subject'

    response = publish_to_sns(topic_arn, message, subject)
    print(response)

    return item

@app.put("/orders/{OrderID}", response_model=OrderModel)
async def put_orders(OrderID:str, item: OrderModel):
    orders_resource.put_orders(OrderID, item)
    return item

@app.delete("/orders/{OrderID}")
async def delete_orders(OrderID:str):
    orders_resource.delete_orders(OrderID)
    return {"message": "Item deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)
