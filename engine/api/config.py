import os
from dotenv import load_dotenv

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config():
    OC_URL: str = os.getenv("OC_URL")
    OC_TOKEN: str = os.getenv("OC_TOKEN")


try:
    config = Config()
except Exception:
    print(Exception)
