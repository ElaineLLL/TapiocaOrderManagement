from __future__ import annotations
from pydantic import BaseModel
from typing import List

from resources.rest_models import Link


class OrderModel(BaseModel):
    OrderID: int
    CustomerID: int
    StaffID: int
    OrderTime: str
    TotalPrice: float
    Status: str

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "OrderID": "0023",
    #                 "CustomerID": "yl5363",
    #                 "StaffID": "yl6353",
    #                 "OrderTime": "14:18",
    #                 "TotalPrice": "12",
    #                 "Status": "Pending"
    #             }
    #         ]
    #     }
    # }


class OrderRspModel(OrderModel):
    links: List[Link] = None



