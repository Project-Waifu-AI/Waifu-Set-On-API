import requests

def req_post():
    response = requests.post(
    url='https://c88b-103-105-55-169.ngrok-free.app/api/posts',
    json={
        'userId': '656c6e804059fb44c7ae27b4',
        'desc': 'hai test 2',
    },
    headers={"Content-Type": "application/json"}
    )
    print(response.json())