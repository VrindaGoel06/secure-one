from user_model import User
from file_manager import FileManager

print("=== Testing MongoDB Connection & Creating Entries ===")

# Create systems
user_system = User()
file_system = FileManager()

# 1. User create karo
print("1. Creating test user...")
success, message = user_system.register("Test User", "test@example.com", "test123")
print(f"   {message}")

# 2. Login test karo
print("2. Testing login...")
success, message, user = user_system.login("test@example.com", "test123")
print(f"   {message}")

# 3. File upload test karo
print("3. Uploading test file...")

# Test file content
test_content = b"This is a test file for MongoDB connection test!"

class MockFile:
    def read(self): 
        return test_content

success, message = file_system.upload_file("test@example.com", MockFile(), "test_file.txt")
print(f"   {message}")

print("=== TEST COMPLETE ===")
print("Now check MongoDB Atlas for entries!")