#!/usr/bin/env python
"""
Generate a secure Django secret key
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print(f"SECRET_KEY={secret_key}")
