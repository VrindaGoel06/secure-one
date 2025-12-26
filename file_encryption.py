import base64
import os

def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted = base64.b64encode(data)
    encrypted_path = file_path + '.enc'
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted)
    print(f"Encrypted: {encrypted_path}")
    return encrypted_path

def decrypt_file(encrypted_path, output_path):
    with open(encrypted_path, 'rb') as f:
        encrypted = f.read()
    decrypted = base64.b64decode(encrypted)
    with open(output_path, 'wb') as f:
        f.write(decrypted)
    print(f"Decrypted: {output_path}")
    return output_path

# Test
if __name__ == "__main__":
    # Create test file
    with open('test.txt', 'w') as f:
        f.write('My secret data')
    
    # Encrypt
    enc_file = encrypt_file('test.txt')
    
    # Decrypt
    dec_file = decrypt_file(enc_file, 'decrypted.txt')
    
    print("SUCCESS: Encryption working!")