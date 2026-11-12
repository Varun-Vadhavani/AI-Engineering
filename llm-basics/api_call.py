import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/todos/1",
    timeout=10,
)

print(response.status_code)   # 200 means success
data = response.json()        # parse the JSON body into a dict
print(data["title"])

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json={"title": "hello", "body": "world", "userId": 1},
    timeout=10,
)
print(response.status_code)   # 201 means created
print(response.json())