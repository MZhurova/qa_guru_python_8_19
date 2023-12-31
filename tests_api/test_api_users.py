import jsonschema
import pytest
import requests
from requests import Response
from utils import load_schema


def test_get_single_user_successfully():
    url = "https://reqres.in/api/users/1"
    schema = load_schema("json_schemas/get_single_user.json")

    result: Response = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_get_list_users_successfully():
    url = "https://reqres.in/api/users?page=2"
    schema = load_schema("json_schemas/get_list_users.json")

    result: Response = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_post_crete_user():
    url = "https://reqres.in/api/users"
    schema = load_schema("json_schemas/post_create_user.json")
    data_user = {"name": "Mariya Zhurova", "job": "QA Engineer"}

    result: Response = requests.post(url, data=data_user)

    assert result.status_code == 201
    jsonschema.validate(result.json(), schema)


def test_put_update_user():
    url = "https://reqres.in/api/users/3"
    data_user = {"name": "Mariya Zhurova", "job": "QA Automation Engineer"}

    result: Response = requests.put(url, data_user)

    assert result.status_code == 200
    assert result.json()["name"] == "Mariya Zhurova"
    assert result.json()["job"] == "QA Automation Engineer"

@pytest.mark.parametrize('id_', [1, 2, 3])
def test_get_single_user_id(id_):
    url = f"https://reqres.in/api/users/{id_}"

    result = requests.get(url)
    assert result.json()['data']['id'] == id_


def test_list_of_users_pagination():
    page = 1
    url = "https://reqres.in/api/users"

    result = requests.get(url, params={"page": page})

    assert result.json()["page"] == page


def test_list_of_users_per_page():
    page = 4
    per_page = 3
    url = "https://reqres.in/api/users"

    result = requests.get(
        url=url,
        params={"page": page, "per_page": per_page}
    )

    assert result.json()["per_page"] == per_page
    assert len(result.json()['data']) == per_page
