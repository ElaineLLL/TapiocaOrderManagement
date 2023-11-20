#
# FastAPI is a framework and library for implementing REST web services in Python.
# https://fastapi.tiangolo.com/
#
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from typing import List, Union

# I like to launch directly and not use the standard FastAPI startup process.
# So, I include uvicorn
import uvicorn


from resources.order_resource import OrdersResource
from resources.order_data_service import OrderDataService
from resources.order_models import OrderModel, OrderRspModel
# from resources.schools.school_models import SchoolRspModel, SchoolModel
# from resources.schools.schools_resource import SchoolsResource

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


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
async def get_orders(OrderID: str = None):
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
