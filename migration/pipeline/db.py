from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_database_url(
    user: str = None,
    password: str = None,
    host: str = None,
    port: str = None,
    dbname: str = None
):
    # 本地預設值
    default_user = "postgres"
    default_password = "sajuna"
    default_host = "localhost"
    default_port = "5432"
    default_dbname = "crm"

    user = user or default_user
    password = password or default_password
    host = host or default_host
    port = port or default_port
    dbname = dbname or default_dbname

    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# 直接用預設值
DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
