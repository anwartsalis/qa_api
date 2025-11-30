import requests
import os
from jsonschema import validate
from dotenv import load_dotenv
from faker import Faker
import allure

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
USER_ID = os.getenv("USER_ID")

PRODUCT_SCHEMA = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "price": {
      "type": "integer"
    },
    "stock": {
      "type": "integer"
    },
    "category": {
      "type": "string"
    },
    "user_id": {
      "type": "string"
    }
  },
  "required": [
    "name",
    "description",
    "price",
    "stock",
    "category",
    "user_id"
  ]
}

fake = Faker()
test_access_token = None

# allure title dll disini
@allure.epic("API Testing, Kelas Otomesyen")
@allure.feature("Autetikasi dan Manajemen Produk")
@allure.story("Test API dengan Credentials yang valid")
@allure.description("Test ini untuk memastikan bahwa API dapat melakukan autentikasi pengguna dan membuat produk dengan benar.")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_success():
    # step hitapi
    global test_access_token
    with allure.step("1. Menyiapkan payload utnuk login"):

      payload = {
      "email": "pyautoid@gmail.com",
      "password": "1234567890"
      }

      response = requests.post(f'{BASE_URL}/auth/v1/token?grant_type=password', headers={"apikey":API_KEY}, json=payload)
      data = response.json()
    # step assert
    with allure.step("2. Mengirim Post request ke endpoint authentication"):
      assert response.status_code == 200
      assert data['expires_in'] == 3600

      test_access_token = data['access_token']
@allure.epic("API Testing, Kelas Otomesyen")
@allure.feature("Autetikasi dan Manajemen Produk")
@allure.story("Test API dengan Credentials yang invalid")
@allure.description("Test ini untuk memastikan bahwa API dapat melakukan autentikasi pengguna dan membuat produk dengan benar.")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_unsuccess(): #without api key
    # step hitapi
    with allure.step("1. Unsuccess login"):
      payload = {
      "email": "pyautoid@gmail.com",
      "password": ""
      }
    with allure.step("2. Validasi unsuccess login"):
      response = requests.post(f'{BASE_URL}/auth/v1/token?grant_type=password', json=payload)
      # step assert
      assert response.status_code == 400

# CREATE PROD
@allure.epic("API Testing, Kelas Otomesyen")
@allure.feature("Post Create Product")
@allure.story("Test API Post Create Product")
@allure.description("Test ini untuk memastikan bahwa API dapat membuat produk dengan benar.")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_product_success():
    with allure.step("1. Menyiapkan data produk baru"):
      print(test_access_token)
      productnya = {
      "name": fake.catch_phrase(),
      "description": fake.text(max_nb_chars=200),
      "price": fake.random_number(digits=5),
      "stock": fake.random_int(min=1, max=100),
      "category": "Electronics",
      "user_id": USER_ID
      }

      headers = {"apikey":API_KEY,
              "Authorization": f"Bearer {test_access_token}",
              "Content-Type" : "application/json",
              "prefer":"return=representation"}

    with allure.step("2. Mengirim Post request ke endpoint produk untuk membuat produk baru"):
      response_prod = requests.post(f'{BASE_URL}/rest/v1/products',headers=headers, json=productnya)
      assert response_prod.status_code == 201
      data = response_prod.json()
    with allure.step("3. Memvalidasi data produk yang dibuat"):
      product = data[0]
      
      validate(instance=product, schema=PRODUCT_SCHEMA)
    