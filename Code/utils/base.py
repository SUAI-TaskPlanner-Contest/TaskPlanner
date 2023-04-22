from time import time
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///./test.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def local_to_utc(dt: datetime):
    return dt.astimezone(timezone.utc)


def utc_to_local(dt: datetime):
    now_timestamp = time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return dt + offset
