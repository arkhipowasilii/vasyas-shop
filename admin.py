from shop import Shop, BACK_MESSAGE, STATUES
from common import Product, Item, User, Order
import json
from typing import List

GET_USERS_ORDERS = 5


class Admin(Shop):
    def __init__(self):
        super().__init__()
        self.action_lst += [self.get_order_list]
        self.action_str += f"Наберите {GET_USERS_ORDERS}, чтобы посмотреть список оплаченных заказов.\n"
        self.orders: List[Order] = []
        self.get_orders()

    def get_orders(self):
        with open(self.cart_path, "r") as read_file:
            raw = json.load(read_file)
        for id, order in raw.items():
            self.orders.append(Order([Item(self.find_product(product_name), amount)
                                      for product_name, amount in order["item_lst"]],
                                     order["status"],
                                     id,
                                     order["datetime"],
                                     order["login"]))

    def get_order_list(self):
        print(BACK_MESSAGE)
        for index, order in enumerate(self.orders):
            if order.status == "payed":
                print(f"Заказ №{order.id}. Пользователь {order.login}. Статус {order.status}. "
                      f"Наберите {index + 1}, чтобы изменить статус данного заказа")

        id = self.get_number(lambda x: 0 <= x <= len(self.orders), f"Наберите, число от 0 до {len(self.orders)}.")

        if id > 0:
            self.change_status(id - 1)

    def change_status(self, order_index: int):
        order = self.orders[order_index]
        print(BACK_MESSAGE)
        print(f"Наберите 1, чтобы изменить статус заказа №{order.id} на sent.\n"
              f"Наберите 2, чтобы изменить статус заказа №{order.id} на delivered.\n")

        action = self.get_number((lambda x: 0 <= x <= 2), f"Наберите, число от 0 до 2.")

        if action == 0:
            self.get_order_list()
        else:
            order.status = STATUES[action + 1]
            with open(self.cart_path, "r") as jsonFile:
                data = json.load(jsonFile)

            data[str(order.id)]["status"] = STATUES[action + 1]

            with open(self.cart_path, "w") as jsonFile:
                json.dump(data, jsonFile)

    def get_product_list(self):
        print(f'Наберите 0, чтобы выйти.')
        for index, product in enumerate(self.products):
            print(f'Наберите {index + 1}, чтобы редактировать товар {product.name} в корзину. '
                  f'Стоимость: {product.price}')
        product_num = self.get_number(lambda x: 0 <= x <= len(self.products),
                                      f"Введите число от 0 до {len(self.products)}")
        self.edit_product(product_num - 1)

    def edit_product(self, product_num):
        product = self.products[product_num]
        print(f"Товар: {product.name}. "
              f"Цена: {product.price}. "
              f"Количество на складе: {product.amount}.")
        print(f"{BACK_MESSAGE}"
              "1 - изменить цену.\n"
              "2 - изменить количество\n")
        action_num = self.get_number(lambda x: 0 <= x <= 2,
                                      f"Введите число от 0 до 2")
        actions = [self.get_product_list, self.change_price, self.change_amount]
        if action_num == 0:
            actions[action_num]()
        else:
            actions[action_num](product_num)

    def change_price(self, product_num: int):
        product = self.products[product_num]
        print(f"{BACK_MESSAGE}"
              "Установите новую цену.")
        new_price = self.get_number(lambda x: x >= 0, "Введите число больше 0.")
        if new_price == 0:
            self.edit_product(product_num)
        else:
            product.price = new_price
            self.change_data_json(self.products_path, product.name, "price", new_price)
            print(f"Теперь {product.name} стоит {new_price}.\n")

    def change_amount(self, product_num: int):
        product = self.products[product_num]
        print(f"{BACK_MESSAGE}"
              "Установите новое количество товара на складе.")
        new_amount = self.get_number(lambda x: x >= 0, "Введите число больше 0.")
        if new_amount == 0:
            self.edit_product(product_num)
        else:
            product.amount = new_amount
            self.change_data_json(self.products_path, product.name, "amount", new_amount)
            print(f"Теперь {product.name} на скалде в количестве {new_amount} штук.\n")


if __name__ == '__main__':
    s = Admin().start()
