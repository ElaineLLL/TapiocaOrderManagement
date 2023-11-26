from resources.abstract_base_data_service import BaseDataService
from resources.order_models import OrderModel,OrderRspModel
import json
import pymysql
from datetime import datetime
from utils import *


class OrderDataService(BaseDataService):

    def __init__(self, config: dict):
        """

        :param config: A dictionary of configuration parameters.
        """
        super().__init__()

        self.data_dir = config["data_directory"]
        self.data_file = config["data_file"]
        self.orders = {}

        self._load()

    def _get_data_file_name(self):
        # DFF TODO Using os.path is better than string concat
        result = self.data_dir + "/" + self.data_file
        return result

    def _load(self):
        fn = self._get_data_file_name()
        with open(fn, "r") as in_file:
            L = json.load(in_file)
            print(L)
            for i in L:
                self.orders[i["OrderID"]] = i

    def _save(self):
        fn = self._get_data_file_name()
        with open(fn, "w") as out_file:
            json.dump(list(self.orders.values()), out_file)

    def get_orders(self, OrderID: str) -> list:
        """

        Returns students with properties matching the values. Only non-None parameters apply to
        the filtering.

        :param uni: UNI to match.
        :param last_name: last_name to match.
        :param school_code: first_name to match.
        :return: A list of matching JSON records.
        """
        result = []
        oid = -1 if OrderID == None else int(OrderID)
        db = pymysql.connect(host = "database-1.caogqwqgw2no.us-east-1.rds.amazonaws.com", 
                    port = 3306,
                    user = "admin", 
                    passwd = "Stargod08122", 
                    db = "Tapioca"
                    )
        cursor = db.cursor()
        if oid == -1:
            sql = f"SELECT * FROM Orderr"
        else:
            sql = f"SELECT * FROM Orderr WHERE OrderID={oid}"
        print(sql)
        try:
            cursor.execute(sql)
            for l in cursor.fetchall():
                seg = {}
                oid,cid,sid,ct,tp,s = l
                seg["OrderID"],seg["CustomerID"],seg['StaffID'],seg["OrderTime"],seg['TotalPrice'],seg['Status'] = oid,cid,sid,str(ct),tp,s
                result.append(seg)
            print('Success')
        except:
            db.rollback()
            print('Error')
        db.close()
        return result
    
    def post_orders(self, item: OrderModel):
        db = pymysql.connect(host = "database-1.caogqwqgw2no.us-east-1.rds.amazonaws.com", 
                    port = 3306,
                    user = "admin", 
                    passwd = "Stargod08122", 
                    db = "Tapioca"
                    )
        ditem = dict(item)
        oid = Readdata("OrderID")
        Changedata("OrderID",oid+1)
        cid,sid,tp,s = ditem['CustomerID'],ditem['StaffID'],ditem['TotalPrice'],ditem['Status']
        ot = str(datetime.now().replace(microsecond=0))
        cursor = db.cursor()
        sql = f"INSERT INTO Orderr (OrderID,CustomerID,StaffID,OrderTime,TotalPrice,Status) VALUES ({oid},{cid},{sid},str_to_date('{ot}','%Y-%m-%d %H:%i:%s'),{tp},'{s}')"
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print('Success')
        except:
            db.rollback()
            print('Error')
        db.close()
        self.orders[oid] = ditem
        self._save()
        return item
    
    def put_orders(self, OrderID: str, item: OrderModel):
        # oid = int(OrderID)
        # if oid not in self.orders:
        #     print("Error!")
        #     return
        db = pymysql.connect(host = "database-1.caogqwqgw2no.us-east-1.rds.amazonaws.com", 
                    port = 3306,
                    user = "admin", 
                    passwd = "Stargod08122", 
                    db = "Tapioca"
                    )
        ditem = dict(item)
        oid,tp,s = int(OrderID),ditem['TotalPrice'],ditem['Status']
        cursor = db.cursor()
        sql = f"UPDATE Orderr Set TotalPrice={tp},Status='{s}' where OrderID={oid};"
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print('Success')
        except:
            db.rollback()
            print('Error')
        db.close()
        self.orders[oid] = dict(item)
        self._save()
        return
    
    def delete_orders(self, OrderID: str):
        oid = int(OrderID)
        if oid not in self.orders:
            print("Error!")
            return
        db = pymysql.connect(host = "database-1.caogqwqgw2no.us-east-1.rds.amazonaws.com", 
                    port = 3306,
                    user = "admin", 
                    passwd = "Stargod08122", 
                    db = "Tapioca"
                    )
        cursor = db.cursor()
        sql = f"delete from Orderr where OrderID={oid};"
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print('Success')
        except:
            db.rollback()
            print('Error')
        db.close()
        del self.orders[oid]
        self._save()
        return
    
    def count_orders(self):
        return len(self.orders)