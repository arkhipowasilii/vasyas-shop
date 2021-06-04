from typing import List, Optional
from common import User, Product
import json

GET_PRODUCT_LIST = 0
AUTHORIZE = 1

class Shop:
    def __init__(self):
        self.users: List[User] = []
        self.products: List[Product] = []
        self.authorized_user: Optional[User, None] = None
        self.action_lst = [self.get_product_list, self.authorize]
        self.get_users()
        self.get_products()

    def get_users(self):
        with open("data/users.json", "r") as read_file:
            raw = json.load(read_file)
        for login, user in raw.items():
            self.users.append(User(login, user["name"], user["password"], bool(user["is_admin"])))

    def get_products(self):
        with open("data/products.json", "r") as read_file:
            raw = json.load(read_file)
        for name, product in raw.items():
            self.products.append(Product(name, product["price"], product["amount"]))

    def start(self):
        print("Привет")
        self.print_actions()
        return self

    def print_actions(self):
        print(f"Наберите {GET_PRODUCT_LIST}, чтобы посмотреть список товаров.\n"
              f"Наберите {AUTHORIZE}, авторизоваться.\n")
        self.get_response()


    def get_actions_menu_decorator(self, func):
        func()
        self.print_actions()

    def get_response(self):
        response = self.get_number(lambda number: 0 <= number < len(self.action_lst),
                                   f"Введите число от 0 до {len(self.action_lst) - 1}\n")
        self.get_actions_menu_decorator(self.action_lst[response])

    def get_product_list(self):
        print("gfhu")
        pass

    def authorize(self):
        while True:
            login = input("Введите логин или 0 для выхода.\n")
            if login == "0":
                break
            for user in self.users:
                if user.login == login:
                    self.ask_password(user)
                    break
            break
        self.print_actions()

    def ask_password(self, user: User):
        while True:
            password = input("Введите пароль или 0 для выхода.\n")
            if password == "0":
                break
            elif user.password == password:
                print(f"Успешная авторизация, {user.name}.\n")
                self.authorized_user = user
                break

    @staticmethod
    def get_number(condition, message: str) -> int:
        response = input()
        while not response.isnumeric() or not condition(int(response)):
            response = input(message)
        return int(response)


if __name__ == '__main__':
    s = Shop().start()
