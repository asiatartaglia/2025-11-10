from database.DB_connect import DBConnect
from model.Arco import Arco
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllOrdini(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                    from stores s, orders o 
                    where s.store_id = o.store_id 
                    and s.store_name = %s"""

        cursor.execute(query, (store.store_name, ))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi(store, k, idMapO):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.order_id as id1, t2.order_id as id2, 
                    ((sum(t1.quantity + t2.quantity)) / datediff(t2.order_date, t1.order_date)) as peso
                    from(select o.order_date, oi.quantity, o.order_id 
                    from stores s, orders o, order_items oi 
                    where s.store_id = o.store_id 
                    and o.order_id = oi.order_id 
                    and s.store_name = %s)t1,
                    (select o.order_date, oi.quantity, o.order_id 
                    from stores s, orders o, order_items oi 
                    where s.store_id = o.store_id 
                    and o.order_id = oi.order_id 
                    and s.store_name = %s)t2
                    where t1.order_id <> t2.order_id 
                    and t1.order_date < t2.order_date 
                    and datediff(t2.order_date, t1.order_date) <= %s
                    group by t1.order_id, t2.order_id  
                    order by peso desc
                    """

        cursor.execute(query, (store.store_name, store.store_name, k ))

        for row in cursor:
            results.append(Arco(idMapO[row["id1"]], idMapO[row["id2"]], row["peso"]))



        cursor.close()
        conn.close()
        return results