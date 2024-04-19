db_URI='postgresql://localhost:5432/cwc'
secret='tobeornottobe'
if db_URI.startswith("postgres://"):
    db_URI = db_URI.replace("postgres://", "postgresql://", 1)