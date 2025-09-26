import os

print("Checking Cloudinary environment variables:")
print(f"CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME', 'Not set')}")
print(f"CLOUDINARY_API_KEY: {os.getenv('CLOUDINARY_API_KEY', 'Not set')}")
print(f"CLOUDINARY_API_SECRET: {'Set' if os.getenv('CLOUDINARY_API_SECRET') else 'Not set'}")

print("\nChecking if we're in DEBUG mode:")
print(f"DEBUG: {os.getenv('DEBUG', 'Not set')}")

print("\nChecking if we're on Render:")
print(f"RENDER: {os.getenv('RENDER', 'Not set')}")