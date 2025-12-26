from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    def __init__(self):
        #  YAHAN APNA CONNECTION STRING DALO
        mongo_uri = "mongodb+srv://puneet_mongo:<db_password>@securedrive.qujemia.mongodb.net/?appName=SecureDrive"
        
        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client['cryvault']
            self.users = self.db['users']
            print("MongoDB Connected!")  #  Emoji hata diya
        except Exception as e:
            print(f"MongoDB Error: {e}")  # Emoji hata diya
    
    def register(self, name, email, password):
        try:
            if self.users.find_one({'email': email}):
                return False, "User already exists"
            
            self.users.insert_one({
                'name': name,
                'email': email,
                'password': generate_password_hash(password),
                'created_at': datetime.now()
            })
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Error: {e}"
    
    def login(self, email, password):
        try:
            user = self.users.find_one({'email': email})
            if user and check_password_hash(user['password'], password):
                return True, "Login successful", user
            return False, "Invalid email or password", None
        except Exception as e:
            return False, f"Error: {e}", None

# Test
if __name__ == "__main__":
    user = User()