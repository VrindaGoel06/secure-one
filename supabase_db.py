import requests
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import time
import urllib.parse  # Top mein import karo

print("Script starting...")

class SupabaseDB:
    def __init__(self):
        print("Initializing SupabaseDB...")
        self.url = "https://wskdnpgxyavvhbgftmqu.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indza2RucGd4eWF2dmhiZ2Z0bXF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2ODAwNzgsImV4cCI6MjA3ODI1NjA3OH0.IxuhveUqSXI6T5LXUwJ_MPGtoEEdL8VTaKdahVUpvvo"
        self.headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "apikey": self.key
        }
        print("SupabaseDB Initialized")
    
    def register(self, name, email, password):
        try:
            print(f"Registering user: {email}")
            
            # Check if user exists
            response = requests.get(
                f"{self.url}/rest/v1/users?email=eq.{email}",
                headers=self.headers
            )
            
            if response.status_code != 200:
                return False, f"Database error: {response.text}"
            
            if response.json():
                return False, "User already exists"
            
            # Create user
            hashed_password = generate_password_hash(password)
            data = {
                "name": name,
                "email": email,
                "password": hashed_password
            }
            
            response = requests.post(
                f"{self.url}/rest/v1/users",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 201:
                return True, "User registered successfully"
            else:
                return False, f"Registration failed: {response.text}"
            
        except Exception as e:
            return False, f"Error: {e}"
    
    def login(self, email, password):
        try:
            print(f"Logging in user: {email}")
            
            response = requests.get(
                f"{self.url}/rest/v1/users?email=eq.{email}",
                headers=self.headers
            )
            
            if response.status_code != 200:
                return False, f"Database error: {response.text}", None
            
            users = response.json()
            if not users:
                return False, "User not found", None
            
            user = users[0]
            if check_password_hash(user['password'], password):
                return True, "Login successful", user
            else:
                return False, "Invalid password", None
                
        except Exception as e:
            return False, f"Error: {e}", None

class SupabaseFileManager:
    def __init__(self):
        print("Initializing SupabaseFileManager...")
        self.url = "https://wskdnpgxyavvhbgftmqu.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indza2RucGd4eWF2dmhiZ2Z0bXF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2ODAwNzgsImV4cCI6MjA3ODI1NjA3OH0.IxuhveUqSXI6T5LXUwJ_MPGtoEEdL8VTaKdahVUpvvo"
        self.headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "apikey": self.key
        }
        self.bucket_name = "user-files"
        print("SupabaseFileManager Initialized")
    
    def upload_file(self, user_email, file, filename):
        try:
            print(f"Uploading file: {filename} for user: {user_email}")
            
            file_data = file.read()
            
            # Create unique file path
            timestamp = int(time.time())
            file_path = f"{user_email}/{timestamp}_{filename}"
            
            # Upload to Supabase Storage using storage class
            from supabase_storage import SupabaseStorage
            storage = SupabaseStorage()
            success, cloud_path, public_url = storage.upload_file(file_data, filename, user_email)
            
            if success:
                # Save file info to database
                file_info = {
                    "user_email": user_email,
                    "original_name": filename,
                    "cloud_path": cloud_path,
                    "public_url": public_url,
                    "file_size": len(file_data),
                    "file_type": "other",
                    "is_encrypted": True,
                    "file_id": str(uuid.uuid4())
                }
                
                response = requests.post(
                    f"{self.url}/rest/v1/files",
                    headers=self.headers,
                    json=file_info
                )
                
                if response.status_code == 201:
                    return True, "File uploaded successfully"
                else:
                    return False, f"Database error: {response.text}"
            else:
                return False, "Storage upload failed"
            
        except Exception as e:
            return False, f"Upload failed: {e}"
    
    def get_user_files(self, user_email):
        try:
            print(f" Getting files for user: {user_email}")
            
            # URL encode user email
            encoded_email = urllib.parse.quote(user_email)
            
            response = requests.get(
                f"{self.url}/rest/v1/files?user_email=eq.{encoded_email}",
                headers=self.headers
            )
            
            print(f" Response status: {response.status_code}")
            
            if response.status_code == 200:
                files = response.json()
                print(f"Found {len(files)} files")
                
                # Ensure each file has required fields
                for file in files:
                    file['file_id'] = file.get('file_id', '')
                    file['file_size'] = file.get('file_size', 0)
                    file['original_name'] = file.get('original_name', 'Unknown')
                    file['uploaded_at'] = file.get('uploaded_at', '')
                
                return True, files
            else:
                print(f" API Error: {response.text}")
                return True, []  # Return empty list instead of False
                
        except Exception as e:
            print(f"Exception in get_user_files: {e}")
            return True, []  # Return empty list instead of False
    
    def download_file(self, user_email, file_id):
        try:
            print(f"Downloading file: {file_id} for user: {user_email}")
            
            # Get file info from database
            response = requests.get(
                f"{self.url}/rest/v1/files?file_id=eq.{file_id}&user_email=eq.{user_email}",
                headers=self.headers
            )
            
            if response.status_code != 200 or not response.json():
                return False, "File not found", None, None
            
            file_info = response.json()[0]
            
            # Download file from storage using storage class
            from supabase_storage import SupabaseStorage
            storage = SupabaseStorage()
            success, file_data = storage.download_file(file_info['cloud_path'])
            
            if success:
                return True, "Download ready", file_data, file_info['original_name']
            else:
                return False, "Download failed", None, None
            
        except Exception as e:
            return False, f"Download failed: {e}", None, None

def test_database_connection():
    print("Testing database connection...")
    
    db = SupabaseDB()
    
    try:
        response = requests.get(
            f"{db.url}/rest/v1/users?limit=1",
            headers=db.headers
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("Database connection SUCCESS!")
            users = response.json()
            print(f"Found {len(users)} users in database")
        else:
            print(f"Database error: {response.status_code}")
            print(f"Error details: {response.text}")
            
    except Exception as e:
        print(f"Connection failed: {e}")

def test_user_registration():
    print("Testing user registration...")
    
    db = SupabaseDB()
    
    # Test registration
    success, message = db.register("Test User", "test@example.com", "test123")
    print(f"Registration: {message}")
    
    if success:
        # Test login
        success, message, user = db.login("test@example.com", "test123")
        print(f"Login: {message}")
        
        if success:
            print("User system working perfectly!")
        else:
            print("Login failed")
    else:
        print("Registration failed")

if __name__ == "__main__":
    print("Starting main execution...")
    test_database_connection()
    test_user_registration()
    print("Script finished")