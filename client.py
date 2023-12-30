import requests

BASE_URL = r'http://127.0.0.1:5000/ads/'

# создали объявление

response = requests.post(
    f"{BASE_URL}",
    json={'title': 'Продам вещи', 'description': 'Вещи очень крутые', 'owner_ad': 3},
)
print(response.status_code)
print(response.json())

# получение объявления

response = requests.get(
    f"{BASE_URL}{1}"
)
print(response.status_code)
print(response.json())

# удаление

response_for_delete = requests.post(
    f"{BASE_URL}",
    json={'title': 'Продам вещи', 'description': 'Вещи очень крутые', 'owner_ad': 3},
)
print(response_for_delete.status_code)
print(response_for_delete.json())

id_ad_for_delete = response_for_delete.json()['id']

response = requests.delete(
    f"{BASE_URL}{id_ad_for_delete}"
)

print(response.status_code)
print(response.json())

response = requests.get(
    f"{BASE_URL}{id_ad_for_delete}"
)
print(response.status_code)
print(response.json())

# изменение объявления

response = requests.patch(
    f"{BASE_URL}{1}",
    json={"description": "изменили описание"}
)
print(response.status_code)
print(response.json())

response = requests.get(
    f"{BASE_URL}{1}"
)
print(response.status_code)
print(response.json())
