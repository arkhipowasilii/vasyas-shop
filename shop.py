from typing import List, Optional, Union
from common import User, Product, Item
import json
from datetime import datetime

STATUES = ["created", "payed", "sent", "delivered"]
BACK_MESSAGE = "Наберите 0, чтобы вернуться назад.\n"
GET_PRODUCT_LIST = 0
AUTHORIZE = 1
GET_CART = 2
CHECKOUT = 3
LOGOUT = 4

class Shop:
    def __init__(self):
        self.users: List[User] = []
        self.products: List[Product] = []
        self.cart: List[Item] = []
        self.users_path = "data/users.json"
        self.products_path = "data/products.json"
        self.cart_path = "data/orders.json"
        self.order_id = 0
        self.authorized_user: Optional[User, None] = None
        self.action_lst = [self.get_product_list, self.authorize, self.open_cart, self.checkout, self.logout]
        self.get_users()
        self.get_products()
        self.action_str = f"Наберите {GET_PRODUCT_LIST}, чтобы посмотреть список товаров.\n"\
            f"Наберите {AUTHORIZE}, чтобы авторизоваться.\n"\
            f"Наберите {GET_CART}, чтобы посмотреть корзину.\n" \
            f"НАберите {CHECKOUT}, чтобы оформить закакз.\n" \
            f"Наберите {LOGOUT}, чтобы выйти из аккаунта.\n"

    def get_users(self):
        with open(self.users_path, "r") as read_file:
            raw = json.load(read_file)
        for login, user in raw.items():
            self.users.append(User(login, user["name"], user["password"], bool(user["is_admin"])))

    def get_products(self):
        with open(self.products_path, "r") as read_file:
            raw = json.load(read_file)
        for name, product in raw.items():
            self.products.append(Product(name, product["price"], product["amount"]))

    def get_cart(self):
        with open(self.cart_path, "r") as read_file:
            raw = json.load(read_file)

        is_older_order_find = False

        for name, order_data in raw.items():
            self.order_id = int(name)
            if order_data["login"] == self.authorized_user.login and order_data["status"] == STATUES[0]:
                is_older_order_find = True
                for item in order_data["item_lst"]:
                    self.cart.append(Item(self.find_product(item[0]), item[1]))

        if not is_older_order_find:
            self.order_id += 1
            raw[f"{self.order_id}"] = {
                    "login": f"{self.authorized_user.login}",
                    "status": "created",
                    "datetime": "",
                    "item_lst": []
                }
            with open(self.cart_path, "w") as jsonFile:
                json.dump(raw, jsonFile)

    def start(self):
        print("Привет")
        self.print_actions(self.action_str)
        return self

    def print_actions(self, actions: str = None):
        if actions is None:
            actions = self.action_str
        print(actions)
        self.get_response()

    def get_actions_menu_decorator(self, func):
        func()
        self.print_actions()

    def get_response(self):
        response = self.get_number(lambda number: 0 <= number < len(self.action_lst),
                                   f"Введите число от 0 до {len(self.action_lst) - 1}\n")
        if response >= 2 and self.authorized_user is None:
            print("Авторизуйтесь для этого действия.\n")
            self.print_actions()
        elif response >= 5 and self.authorized_user is not None and self.authorized_user.is_admin != 1:
            print("Авторизуйтесь как админ для этого действия.\n")
            self.print_actions()
        else:
            self.get_actions_menu_decorator(self.action_lst[response])

    def get_product_list(self):
        print(f'Наберите 0, чтобы выйти.')
        for index, product in enumerate(self.products):
            print(f'Наберите {index + 1}, чтобы добавиить товар {product.name} в корзину. Стоимость: {product.price}')
        self.add_product_to_cart()

    def add_product_to_cart(self):
        product_index = self.get_number(lambda x: 0 <= x <= (len(self.products)),
                                        f"Введите число от 1 до {len(self.products)}")
        if self.authorized_user is None:
            print("Авторизуйтесь, чтобы добавить товар в корзину.\n")
        elif product_index == 0:
            self.print_actions()
        else:
            result = self.add_products(self.products[product_index - 1], 1)
            if result:
                print("Поздравляю! Товар успешно довален в корзину.")
            else:
                pass
            self.get_product_list()

    def add_products(self, product: Product, number: int) -> bool:
        current_item = None
        for item in self.cart:
            if item.product == product:
                if not item.amount + number <= product.amount:
                    print("На складе нет столько товаров :(")
                    return False
                current_item = item

        if current_item is not None:
            current_item.amount += number
        else:
            current_item = Item(product, number)
            self.cart.append(current_item)

        self.update_order_data(product.name, current_item.amount)
        return True

    def update_order_data(self, product_name: str, amount: int):
        with open(self.cart_path, "r") as jsonFile:
            data = json.load(jsonFile)

        is_find = False
        for index, item in enumerate(data[str(self.order_id)]["item_lst"]):
            if item[0] == product_name:
                is_find = True
                data[str(self.order_id)]["item_lst"][index][1] = amount
                break

        if not is_find:
            data[str(self.order_id)]["item_lst"].append([product_name, amount])

        with open(self.cart_path, "w") as jsonFile:
            json.dump(data, jsonFile)

    def open_cart(self):
        order_sum = 0
        print(BACK_MESSAGE)
        for index, item in enumerate(self.cart):
            print(f"{item.product.name}, {item.amount} штук(и) по цене {item.product.price}. "
                  f"Наберите {index + 1}, чтобы редактировать позицию")
            order_sum += item.product.price
        print(f"Итого: {order_sum}.")
        item_num = self.get_number(lambda x: 0 <= x <= 3, f"Введите число от 0 до {len(self.cart)}.")
        if item_num == 0:
            self.print_actions()
        else:
            self.edit_item(item_num - 1)

    def edit_item(self, item_num: int):
        item = self.cart[item_num]
        print(f"У вас в корзине {item.product.name} в количестве {item.amount}.\n"
              f"{BACK_MESSAGE}"
              f"Наберите 1, чтобы удалить всё.\n"
              f"Наберите 2, чтобы увеличить количество товаров на 1.\n"
              f"Наберите 3, чтобы уменишить товаров количество на 1.\n")
        action_num = self.get_number(lambda x: 0 <= x <= 3, "Введите число от 0 до 3.")
        if action_num == 0:
            self.open_cart()
        elif action_num == 1:
            self.cart.pop(item_num)
            self.delete_product_json(item.product.name)
        elif action_num == 2:
            result = self.add_products(item.product, 1)
            if result:
                self.edit_order_json(item.product, item.amount + 1)
        elif action_num == 3:
            item.amount -= 1
            self.edit_order_json(item.product, item.amount - 1)
            if item.amount == 0:
                self.cart.pop(item_num)
                self.delete_product_json(item.product.name)
        self.open_cart()

    def delete_product_json(self, product_name):
        with open(self.cart_path, "r") as jsonFile:
            data = json.load(jsonFile)

        for index, item in enumerate(data[str(self.order_id)]["item_lst"]):
            if item[0] == product_name:
                data[str(self.order_id)]["item_lst"].pop(index)

        with open(self.cart_path, "w") as jsonFile:
            json.dump(data, jsonFile)

    def edit_order_json(self, product_name, amount: int):
        with open(self.cart_path, "r") as jsonFile:
            data = json.load(jsonFile)

        for index, item in enumerate(data[str(self.order_id)]["item_lst"]):
            if item[0] == product_name:
                data[str(self.order_id)]["item_lst"][index][1] = amount

        with open(self.cart_path, "w") as jsonFile:
            json.dump(data, jsonFile)

    def checkout(self):
        is_allowed = True
        print(BACK_MESSAGE)
        order_sum = 0
        for item in self.cart:
            order_sum += item.product.price
            if item.amount > item.product.amount:
                print(f"У вас в корзине {item.amount} штук {item.product.name}, а на складе всего {item.product.amount}."
                      f"Зайдите, пожалуйста, в корзину и уменьшите количество данного товара или удалите его.")
                is_allowed = False

        if is_allowed:
            print("Нажмите 1, чтобы оформитьзаказ и оплатить.")
            result = self.get_number(lambda x: 0 <= x <= 1, "Введите число от 0 до 1.")
            if result == 1:
                with open(self.cart_path, "r") as jsonFile:
                    data = json.load(jsonFile)

                data[str(self.order_id)]["status"] = "complete"
                data[str(self.order_id)]["datetime"] = datetime.now().__str__()
                self.cart = []

                with open(self.cart_path, "w") as jsonFile:
                    json.dump(data, jsonFile)
                print(f'Спасибо за покупку, с вас списано {order_sum}.')

    def authorize(self):
        while True:
            login = input("Введите логин или 0 для выхода.\n")
            if login == "0":
                break
            for user in self.users:
                if user.login == login:
                    self.ask_password(user)
                    return

    def ask_password(self, user: User):
        while True:
            password = input("Введите пароль или 0 для выхода.\n")
            if password == "0":
                break
            elif user.password == password:
                self.authorized_user = user
                self.get_cart()
                print(f"Успешная авторизация, {user.name}.\n")
                break

    def logout(self):
        print(f"До свидания, {self.authorized_user.name}!")
        self.authorized_user = None
        self.cart = []

    def find_product(self, name: str) -> Product:
        for product in self.products:
            if product.name == name:
                return product

    @staticmethod
    def change_data_json(path: str, name: str, key: str, value: Union[str, int]):
        with open(path, "r") as jsonFile:
            data = json.load(jsonFile)

        data[name][key] = value

        with open(path, "w") as jsonFile:
            json.dump(data, jsonFile)

    @staticmethod
    def get_number(condition, message: str) -> int:
        response = input()
        while not response.isnumeric() or not condition(int(response)):
            response = input(message)
        return int(response)


if __name__ == '__main__':
    s = Shop()
    s.start()
