import os
from supabase import create_client, Client
import base64
from datetime import datetime

class SupabaseStorage:
    def __init__(self):
        # Supabase credentials
        self.url = "https://wskdnpgxyavvhbgftmqu.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indza2RucGd4eWF2dmhiZ2Z0bXF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2ODAwNzgsImV4cCI6MjA3ODI1NjA3OH0.IxuhveUqSXI6T5LXUwJ_MPGtoEEdL8VTaKdahVUpvvo"
        
        try:
            self.supabase: Client = create_client(self.url, self.key)
            self.bucket_name = "user-files"
            print("Supabase Storage Connected")
        except Exception as e:
            print(f"Supabase Connection Error: {e}")
            raise e
    
    def upload_file(self, file_data, file_name, user_email):
        """File upload to Supabase Storage"""
        try:
            # Create unique file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_email = user_email.replace('@', '_at_').replace('.', '_dot_')
            cloud_filename = f"{safe_email}/{timestamp}_{file_name}"
            
            # Upload file to Supabase
            response = self.supabase.storage.from_(self.bucket_name).upload(
                cloud_filename,
                file_data
            )
            
            if response:
                # Get public URL
                public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(cloud_filename)
                print(f"File uploaded to Supabase: {file_name}")
                return True, cloud_filename, public_url
            else:
                return False, "Upload failed", None
                
        except Exception as e:
            print(f"Supabase Upload Failed: {e}")
            return False, str(e), None
    
    def download_file(self, cloud_filename):
        """Download file from Supabase Storage"""
        try:
            # Download file
            response = self.supabase.storage.from_(self.bucket_name).download(cloud_filename)
            
            if response:
                print(f"File downloaded from Supabase: {cloud_filename}")
                return True, response
            else:
                return False, None
                
        except Exception as e:
            print(f"Supabase Download Failed: {e}")
            return False, None
    
    def delete_file(self, cloud_filename):
        """Delete file from Supabase Storage"""
        try:
            response = self.supabase.storage.from_(self.bucket_name).remove([cloud_filename])
            
            if response:
                print(f"File deleted from Supabase: {cloud_filename}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Supabase Delete Failed: {e}")
            return False

# Test function
def test_supabase():
    print("=== Testing Supabase Storage ===")
    
    supabase = SupabaseStorage()
    
    # Test data
    test_content = b"Hello, this is Supabase cloud storage test!"
    test_email = "test@example.com"
    
    # Upload test
    success, cloud_path, public_url = supabase.upload_file(
        test_content, 
        "test_supabase.txt", 
        test_email
    )
    
    if success:
        print(f"Upload successful!")
        print(f"Cloud Path: {cloud_path}")
        print(f"Public URL: {public_url}")
        
        # Download test
        success, downloaded_data = supabase.download_file(cloud_path)
        
        if success and downloaded_data == test_content:
            print(" Download test passed!")
            print("Supabase Storage is working perfectly! ")
        else:
            print(" Download test failed")
    else:
        print("Upload test failed")

if __name__ == "__main__":
    test_supabase()