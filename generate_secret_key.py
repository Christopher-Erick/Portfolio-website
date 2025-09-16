#!/usr/bin/env python3
"""
Generate a secure Django secret key.
"""

import secrets
import string

def generate_secret_key(length=50):
    """
    Generate a cryptographically secure random secret key for Django.
    
    Args:
        length (int): Length of the secret key (default: 50)
        
    Returns:
        str: Generated secret key
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    # Remove characters that might cause issues in environment variables
    chars = chars.replace('"', '').replace("'", '').replace('\\', '').replace('`', '')
    
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Generated secret key: {secret_key}")
    print("\nUpdate your .env file with this key:")
    print(f"SECRET_KEY={secret_key}")