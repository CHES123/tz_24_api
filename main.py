from fastapi import FastAPI
from db_execute import f_get_list_apart, f_get_free_apartment_list, f_order_apart,f_miss_order, f_get_vip_status

app = FastAPI()

@app.get("/list_apart")
async def get_list_apart():
    return f_get_list_apart()

@app.get("/list_free_apart")
async def get_free_apartment_list(beg_date : str, end_date: str):
    return f_get_free_apartment_list(beg_date, end_date)

@app.post("/order_apart")
async def order_apart(apartment_name: str, client_name: str, beg_date : str, end_date: str, vip_status: int):
    return f_order_apart(apartment_name, client_name, beg_date, end_date, vip_status)

@app.put("/miss_order")
async def miss_order(order_id: int):
    return f_miss_order(order_id)

@app.get("/vip_status")
async def get_vip_status(client_name: str):
    return f_get_vip_status(client_name)


#pip install uvicorn
#uvicorn main:app --host 0.0.0.0 --port 8080
#kill -9 $(ps -ef | grep uvicorn  | awk '{print $2}')