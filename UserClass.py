import json

class User:
    def __init__(self,username,password , id):
        self.username = username
        self.password = password
        self.id = id

    def register_user(self, username, password, id):
        with open("user_data.json", "r") as read_file:
            data = json.load(read_file)

        new_user = {
            "user_id": id,
            "username": username,
            "password": password
        }

        user_exists = False

        for user in data["users"]:
            if user["user_id"] == id:
                user_exists = True
                break

        if not user_exists:
            data["users"].append(new_user)

            with open("user_data.json", "w") as write_file:
                json.dump(data, write_file, indent=4)

            print("User registered successfully")
        else:
            print("This user ID already exists")

        def Check_User_Exists(self, user_id):
            with open("user_data.json", "r") as read_file:
                data = json.load(read_file)

            for user in data["users"]:
                if user["user_id"] == user_id:
                    return True

            return False

