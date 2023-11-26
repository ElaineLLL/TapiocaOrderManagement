from __future__ import annotations
from pydantic import BaseModel
from typing import List

from resources.rest_models import Link


class OrderModel(BaseModel):
    OrderID: int = 0
    CustomerID: int = 0
    StaffID: int = 0
    OrderTime: str = ''
    TotalPrice: float = 0.0
    Status: str = ''

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



