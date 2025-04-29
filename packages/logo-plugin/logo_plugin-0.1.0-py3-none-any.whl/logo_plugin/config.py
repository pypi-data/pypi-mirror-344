import os

MONGO_URI      = os.getenv('MONGO_URI', 'mongodb+srv://badalmahajan203152:qDs5r92TF5cZ0yPs@cluster0.7n3uur0.mongodb.net/')
DB_NAME        = os.getenv('DB_NAME', 'company_logos')
API_BASE_URL   = os.getenv('API_BASE_URL', 'https://img.logo.dev')
API_PATH_TOKEN = os.getenv('LOGO_API_PATH_TOKEN', 'pk_RTzaMq6OSCSNJBsqUSv9hA')
API_KEY        = os.getenv('API_KEY', 'sk_LQIYnGNzQMyVsnY8Plx7VQ')


