import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    print(f"Setting {key.strip()} = {value.strip()}")
                    os.environ.setdefault(key.strip(), value.strip())

# Check current value
print("Before loading .env:", os.getenv('HACKTHEBOX_USERNAME'))

# Load .env file
load_env_file()

# Check after loading
print("After loading .env:", os.getenv('HACKTHEBOX_USERNAME'))