from typing import List
from datetime import datetime
import json


class User:
    def __init__(self, login: str, name: str, password: str, is_admin: bool):
        self.login = login
        self.name = name
        self.password = password
        self.is_admin = is_admin


class Product:
    def __init__(self, name: str, price: int, amount: int):
        self.name = name
        self.price = price
        self.amount = amount


class Item:
    def __init__(self, product: Product, amount: int):
        self.product = product
        self.amount = amount


class Order:
    def __init__(self, lst_items: List[Item], status: int):
        self.lst_items = lst_items
        self.status = status
        self.number = self.get_number()
        self.date = datetime.now()

    def get_number(self):
        return


if __name__ == '__main__':
    pass
