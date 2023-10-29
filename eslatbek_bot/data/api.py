import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/'

"""
create_user
"""


async def create_user(telegram_id, username, full_name, nick_name, phone_number, age, is_active):
    context = {
        "telegram_id": telegram_id,
        "username": username,
        "full_name": full_name,
        "nick_name": nick_name,
        "phone_number": phone_number,
        "age": age,
        "is_active": is_active
    }
    response = requests.post(BASE_URL + 'users/', data=context)
    return response


"""
get_me
"""


async def get_me(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/')
    data = json.loads(response.text)
    return data


"""
get_all_users
"""


async def get_all_users():
    response = requests.get(BASE_URL + 'users/')
    data = json.loads(response.text)
    return data


"""
create_target
"""


async def create_target(telegram_id, name, description, is_active, weekday, time, start_date, end_date):
    context = {
        "user": telegram_id,
        "name": name,
        "description": description,
        "weekday": weekday,
        "time": time,
        "start_date": start_date,
        "end_date": end_date,
        "is_active": is_active
    }
    response = requests.post(BASE_URL + 'targets/', data=context)
    return response


"""
get_my_targets
"""


async def get_my_targets(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/targets/')
    data = json.loads(response.text)
    return data


"""
get_my_current_target(s)
"""


async def get_my_current_target(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/targets/')
    data = json.loads(response.text)
    return data


"""
if target is failed then create fail plan model. If target is success then return success
"""


async def update_my_target_status(telegram_id, is_done):
    context = {
        'is_done': is_done
    }
    response = requests.patch(BASE_URL + f'')


async def get_weekdays():
    response = requests.get(BASE_URL + 'weekdays/')
    data = json.loads(response.text)
    return data

# print(get_weekdays())

#### create user test is successfuly complate
# a = create_user(telegram_id=123456789, username='test', full_name='test', nick_name='test', age=20, is_active=True, phone_number='123456789')
# print(a.text)


# #### create target
# a = create_target(telegram_id=1, name='test', description='test', is_active=True, weekday=[0,1,2], time='12:00', start_date='2021-09-01', end_date='2021-09-30')
# print(a.text)
