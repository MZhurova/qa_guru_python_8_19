import jsonschema
import pytest
import requests
from requests import Response
from utils import load_schema

WEB_URL = "https://reqres.in/api"

def test_get_list_users_successfully():
    url = WEB_URL + "/users?page=2"
    schema = load_schema("get_list_users.json")

    result: Response = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_get_single_user_successfully():
    url = WEB_URL + "/users/1"
    schema = load_schema("get_single_user.json")

    result: Response = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_get_single_user_not_found():
    url = WEB_URL + "/users/13"

    result: Response = requests.get(url)

    assert result.status_code == 404
    assert result.reason == "Not Found"
    assert result.json() == {}


def test_post_crete_user():
    url = WEB_URL + "/users"
    schema = load_schema("post_create_user.json")
    data_user = {"name": "Mariya Zhurova", "job": "QA Engineer"}

    result: Response = requests.post(url, data=data_user)

    assert result.status_code == 201
    jsonschema.validate(result.json(), schema)


def test_put_update_user():
    url = WEB_URL + "/users/3"
    data_user = {"name": "Mariya Zhurova", "job": "QA Automation Engineer"}

    result: Response = requests.put(url, data_user)

    assert result.status_code == 200
    assert result.json()["name"] == "Mariya Zhurova"
    assert result.json()["job"] == "QA Automation Engineer"


def test_patch_user():
    url = WEB_URL + "/users/2"
    data_user = {"name": "Mariya Zhurova", "job": "QA Automation Engineer"}

    result: Response = requests.patch(url, data_user)

    assert result.status_code == 200
    assert result.json()["name"] == "Mariya Zhurova"
    assert result.json()["job"] == "QA Automation Engineer"


def test_delete():
    url = WEB_URL + "/users?page=2"

    result: Response = requests.delete(url)

    assert result.status_code == 204
    assert result.reason == 'No Content'
    assert result.text == ''


def test_post_register_successful():
    url = WEB_URL + "/register"
    schema = load_schema("register_successful.json")
    data_user = {"email": "eve.holt@reqres.in", "password": "pistol"}

    result: Response = requests.post(url, data_user)

    assert result.status_code == 200
    assert result.json()['id'] == 4
    assert result.json()['token'] == 'QpwL5tke4Pnpja7X4'
    jsonschema.validate(result.json(), schema)


def test_post_register_unsuccessful():
    url = WEB_URL + "/register"
    schema = load_schema("register_unsuccessful.json")
    data_user = {"email": "sydney@fife"}

    result: Response = requests.post(url, data_user)

    assert result.status_code == 400
    jsonschema.validate(result.json(), schema)

def test_get_delayed_response():
    url = WEB_URL + "/users?delay=3"
    schema = load_schema("delayed_response.json")

    result: Response = requests.get(url)

    assert result.status_code == 200
    assert result.json()['per_page'] == 6
    assert result.json()['total'] == 12
    jsonschema.validate(result.json(), schema)


@pytest.mark.parametrize('id_', [1, 2, 3])
def test_get_single_user_id(id_):
    url = f"https://reqres.in/api/users/{id_}"

    result = requests.get(url)
    assert result.json()['data']['id'] == id_


def test_list_of_users_pagination():
    page = 1
    url = WEB_URL + "/users"

    result = requests.get(url, params={"page": page})

    assert result.json()["page"] == page


def test_list_of_users_per_page():
    page = 4
    per_page = 3
    url = WEB_URL + "/users"

    result = requests.get(
        url=url,
        params={"page": page, "per_page": per_page},
        headers={"Content-Type": "application/json", "Connection": "keep-alive"}
    )

    assert result.json()["per_page"] == per_page
    assert len(result.json()['data']) == per_page
