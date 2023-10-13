import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/'

"""
create_user
"""


def create_user(telegram_id, username, first_name, last_name, age, is_active):
    context = {
        "telegram_id": telegram_id,
        "username": username,
        "full_name": f"{first_name} {last_name}",
        "age": age,
        "is_active": is_active
    }
    response = requests.post(BASE_URL + 'users/', data=context)
    return response.status_code


"""
get_me
"""


def get_me(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/')
    data = json.loads(response.text)
    return data


"""
get_all_users
"""


def get_all_users():
    response = requests.get(BASE_URL + 'users/')
    data = json.loads(response.text)
    return data


"""
create_target
"""


def create_target(telegram_id, name, description, is_active):
    context = {
        "user": telegram_id,
        "name": name,
        "description": description,
        "is_active": is_active
    }
    response = requests.post(BASE_URL + 'targets/', data=context)
    return response.status_code


"""
get_my_targets
"""


def get_my_targets(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/targets/')
    data = json.loads(response.text)
    return data


"""
get_my_current_target(s)
"""


def get_my_current_target(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/targets/')
    data = json.loads(response.text)
    return data


"""
update_my_target_status
"""


def update_my_target_status(telegram_id, is_done):
    context = {
        'is_done': is_done
    }
    response = requests.patch(BASE_URL + f'')
