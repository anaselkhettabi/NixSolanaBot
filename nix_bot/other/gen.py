from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Save the key to a file (optional)
with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("Generated key:", key.decode())
