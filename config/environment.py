import os

db_URI=os.getenv('DATABASE_URL')
secret=os.getenv('SECRET')

if db_URI.startswith("postgres://"):
    db_URI = db_URI.replace("postgres://", "postgresql://", 1)