import psycopg2
from connect_config import user,password,host,port,database
import datetime

def exec_sql(query):
    try:
        conn =  psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        cur = conn.cursor()        
        cur.execute(f"set datestyle = dmy;") 
        cur.execute(query)         
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        #conn.close()
    finally:
        conn.commit()
        #conn.close()
        return cur

def f_get_list_apart():   
    result = {}
    try:
        cur =  exec_sql('select * from hotel.apartment')
        result = {"apartment list": {x[0]:x[1] for x in cur}}
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return result


def f_get_client_id(client_name):
    result = None
    try:
        cur =  exec_sql(f"select id from hotel.client where client_name = '{client_name}' ")
        #result = {x[0] for x in cur}
        result = [x[0] for x in cur][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)            
    finally:
        return result
    
def f_get_apartment_id(apartment_name):
    result = None
    try:
        cur =  exec_sql(f"select id from hotel.apartment where apart_name = '{apartment_name}' ")
        result = [x[0] for x in cur][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return result 
       
def f_check_order(apart_id, beg_date, end_date):
    result = 0
    try:
        cur = exec_sql(f"""select count(1)
                             from hotel.orders where id_apartment = '{apart_id}'
                              and (beg_date between '{beg_date}' and '{end_date}' 
                               or end_date between '{beg_date}' and '{end_date}')
                              and dismiss_date is null 
                        """)
        result = [x[0] for x in cur][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return result 
    

def f_order_apart(apart,client, beg_date, end_date,vip_status):
    result = {}
    if beg_date > end_date:
         return {"error": "wrong date period" }
    apart_id = f_get_apartment_id(apart)
    if apart_id == None:
        return {"error": f"{apart} is not exist"}
    client_id = f_get_client_id(client)
    if client_id == None:
        return {"error": f"{client} is not exist"}
    temp = 0
    temp = f_check_order(apart_id,beg_date,end_date)
    if temp > 0:
         return {"ordered":{ "apart id =" : apart_id}}
    try:
        cur =  exec_sql(f"""insert into hotel.orders 
                        (id_apartment,id_client, beg_date, end_date, vip_status)
                        values('{apart_id}','{client_id}','{beg_date}','{end_date}','{vip_status}') returning id""")
        result = [x[0] for x in cur][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return {"order apart":{"order id": result, "beg_date": beg_date, "end_date": end_date}} 
    

def f_miss_order(order_id):
    result = None
    try:        
        cur = exec_sql(f""" update hotel.orders   
                               set dismiss_date = current_date 
                             where id = {order_id} 
                               and dismiss_date is null
                            returning id""")
        if cur.rowcount == 0:
            result = None
        else:    
            result = [x[0] for x in cur][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return {"order miss":{"order_id": result}}        
    

def f_get_vip_status(client_name):    
    result = None
    client_id = f_get_client_id(client_name)
    if client_id == None:
        return {"error": f"{client_name} is not exist"}
    try:
        cur = exec_sql(f"""select vip_status 
                             from hotel.orders
                            where id_client = {client_id}
                              and dismiss_date is null
                            order by id desc
                              """)   
        result = [x for x in cur][0][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return {"vip client":{"client_id": client_id, "vip_status":result}}       

def f_get_free_apartment_list(beg_date,end_date):
    result = None
    try:
        cur = exec_sql(f"""select a.id, a.apart_name 
                             from hotel.apartment a
                            where not exists (select 1 
                                                from hotel.orders o
                                               where o.dismiss_date is null
                                                 and (o.beg_date between '{beg_date}' and '{end_date}' 
                                                  or o.end_date between '{beg_date}' and '{end_date}')
                                                 and o.id_apartment = a.id) """)
        result = {"free apartment":{x[0]:x[1] for x in cur}}
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)   
    finally:
        return result 

"""print(f_get_list_apart()) #список номеров в отеле
print(f_get_free_apartment_list('01.01.2023','08.01.2023')) #список номеров в отеле на определенный период
print(f_order_apart("apartment1","client2", "18.02.2023", "20.02.2023",1)) #забронировать номер в отеле на определенный срок
#2 клиента не могут одновременно забронировать один и тот же номер в отеле на пересекающиеся периоды
print(f_miss_order(161)) #отменить бронь номера в отеле
print(f_get_vip_status("client1")) # может быть VIP а может и не быть (запрос удаленного api сервера для проверки"""

print(f_get_list_apart())