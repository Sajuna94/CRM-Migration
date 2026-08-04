class Resolver:

    def __init__(self, users):
        self.users = {
            row["name"]: row["id"]
            for row in users.rows
        }


    def user_id(self, name):
        if not name:
            return None

        if name not in self.users:
            raise ValueError(f"user not found: {name}")

        return self.users[name]