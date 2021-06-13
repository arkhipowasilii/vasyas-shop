from typing import List
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

    def __eq__(self, other) -> bool:
        if self.name == other.name:
            return True
        return False


class Item:
    def __init__(self, product: Product, amount: int):
        self.product = product
        self.amount = amount


class Order:
    def __init__(self, lst_items: List[Item], status: str, id: str, datetime: str, login: str):
        self.login = login
        self.lst_items = lst_items
        self.status = status
        self.id: str = id
        self.datetime = datetime


if __name__ == '__main__':
    p = Product("ggg", 400, 79)
    pr_lst = [Item(p, 1)]
    if pr_lst[0].product == p:
        print(1)
