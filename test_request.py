import requests

r = requests.get("http://0.0.0.0:8080/list_apart")
print(r.content)

r = requests.get("http://0.0.0.0:8080/list_free_apart?beg_date=01.01.2023&end_date=02.01.2023")
print(r.content)

r = requests.post("http://0.0.0.0:8080/order_apart?apartment_name=apartment1&client_name=client1&beg_date=01.01.2023&end_date=02.01.2023&vip_status=1")
print(r.content)
r = requests.post("http://0.0.0.0:8080/order_apart?apartment_name=apartment2&client_name=client2&beg_date=15.01.2023&end_date=20.01.2023&vip_status=1")
print(r.content)
r = requests.post("http://0.0.0.0:8080/order_apart?apartment_name=apartment3&client_name=client3&beg_date=15.01.2023&end_date=20.01.2023&vip_status=1")
print(r.content)
r = requests.post("http://0.0.0.0:8080/order_apart?apartment_name=apartment3&client_name=client4&beg_date=10.01.2023&end_date=15.01.2023&vip_status=1")
print(r.content)

r = requests.get("http://0.0.0.0:8080/list_free_apart?beg_date=01.01.2023&end_date=02.01.2023")
print(r.content)

r = requests.put("http://0.0.0.0:8080/miss_order?order_id=163")
print(r.content)

r = requests.get("http://0.0.0.0:8080/vip_status?client_name=client1")
print(r.content)


