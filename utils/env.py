import os
from dotenv import load_dotenv


def env (key, alternative = None):
    load_dotenv()
    
    try:
        return os.environ[key]
    except KeyError:
        return alternative