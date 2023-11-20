from resources.abstract_base_resource import BaseResource
from resources.order_models import OrderRspModel, OrderModel
from resources.rest_models import Link
from typing import List


class OrdersResource(BaseResource):
    #
    # This code is just to get us started.
    # It is also pretty sloppy code.
    #

    def __init__(self, config):
        super().__init__()

        self.data_service = config["data_service"]

    @staticmethod
    def _generate_links(s: dict) -> OrderRspModel:

        self_link = Link(**{
            "rel": "self",
            "href": "/students/" + str(s['OrderID'])
        })

        links = [
            self_link
        ]
        rsp = OrderRspModel(**s, links=links)
        return rsp

    def get_orders(self, OrderID: str = None) -> List[OrderRspModel]:
        result = self.data_service.get_orders(OrderID)
        final_result = []
        for s in result:
            m = self._generate_links(s)
            final_result.append(m)

        return final_result

    def post_orders(self,item: OrderModel) -> OrderModel:
        self.data_service.post_orders(item)
        return item
    
    def put_orders(self,OrderID: str, item: OrderModel):
        self.data_service.put_orders(OrderID, item)
        return item

    def delete_orders(self,OrderID: str):
        self.data_service.delete_orders(OrderID)
        return
    
    def count_orders(self):
        res = self.data_service.count_orders()
        return res