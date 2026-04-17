import json

class User:
    def __init__(self, username, password, user_id):
        self.username = username
        self.password = password
        self.user_id = user_id
    @staticmethod
    def register_user(self, username, password, user_id):
        with open("user_data.json", "r") as read_file:
            data = json.load(read_file)

        new_user = {
            "user_id": user_id,
            "username": username,
            "password": password
        }

        user_exists = False

        for user in data["users"]:
            if user["user_id"] == user_id:
                user_exists = True
                break

        if not user_exists:
            data["users"].append(new_user)

            with open("user_data.json", "w") as write_file:
                json.dump(data, write_file, indent=4)

            print("User registered successfully")
        else:
            print("This user ID already exists")

    @staticmethod
    def check_user_exists(self, user_id):
        with open("user_data.json", "r") as read_file:
            data = json.load(read_file)

        for user in data["users"]:
            if user["user_id"] == user_id:
                return True

        return False

    @staticmethod
    def login(self, username, password):
        with open("user_data.json", "r") as read_file:
            data = json.load(read_file)

        for user in data["users"]:
            if user["username"] == username:
                if user["password"] == password:
                    return True
                else:
                    return False

        return False

