class ConverterUtil:
    def user_helper(self, user):
        return {
            "id": user["_id"],
            "name": user["name"],
            "email": user["email"],
            "password": user["password"],
            "photo": user["photo"] if "photo" in user else "",
        }
