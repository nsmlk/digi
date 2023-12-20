from itertools import product
from unittest import result
import requests
import json
from hashlib import sha256
import time


# получение токена
def get_token():
   headers = {
       'Content-Type': "application/json",
       'Accept': "application/json"
   }

   timestamp = time.time()

   sign = sha256(('api key' + str(round(timestamp))).encode('utf-8')).hexdigest()

   token_json_request = {
       "seller_id": id,
       "timestamp": timestamp,
       "sign": sign
   }

   req = requests.post(url=f'https://api.digiseller.ru/api/apilogin', json=token_json_request, headers=headers)

   return json.loads(req.text).get('token')

# плучение словаря с продуктами продавца
def get_products_list(tk):
   headers = {
       'Content-Type': "application/json",
       'Accept': "application/json"
   }

   products_json_request = {
       "id_seller": id,
       "order_col": "cntsell",
       "order_dir": "desc",
       "rows": 2000,
       "page": 1,
       "currency": "USD",
       "lang": "ru-RU",
       "show_hidden": 1,
       "token": tk
   }

   req = requests.post(url=f'https://api.digiseller.ru/api/seller-goods?token={tk}', json=products_json_request, headers=headers)
   return json.loads(req.text).get('rows')

products_list = get_products_list(get_token())
# print(products_list)
# with open("products_list.txt", "w") as file:
    # print(products_list, file=file)
# print(products_list)

# получение нужной информации по каждому продукту
def get_products_info(products_list):
 result = []
 for product in products_list:
    result.append(
       {
        'ID товара': product.get('id_goods'),
        'Название товара': product.get('name_goods'),
        'Площадка': 'Plati.Market',
        'Цена': product.get('price_usd'),
        'Продано': product.get('cnt_sell'),
        'В наличии': product.get('num_in_stock'),})
 return result

print(get_products_info(products_list))
# создание файла с информацией по каждому продукту 
# products = get_products_info(products_list)
# print(products)
# with open("clean_products.txt", "w") as file:
#         print(products, file=file)

# подсчет стоимости стока 
clean_products_list = get_products_info(products_list)

def calculate_total_sum(clean_products_list):
    total_sum = 0
    for product in clean_products_list:
        price_usd = product.get('Цена')
        num_in_stock = product.get('В наличии')
        product_sum = price_usd * num_in_stock
        total_sum += product_sum
    return total_sum

print(calculate_total_sum(clean_products_list))

def main():
   if __name__ == '__main__':
   main()
