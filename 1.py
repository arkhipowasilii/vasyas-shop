def get_data(self, path, cls):
    with open(path, "r") as read_file:
        raw = json.load(read_file)
    lst = []
    for login, user in raw.items():
        u = list(user.values())

        print((login) + set(user.values()))
        lst.append(cls(x for x in [login] + list(user.values())))
    return lst
