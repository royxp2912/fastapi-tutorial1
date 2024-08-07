from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://root:root2912@localhost:3306/usertestdb"

engine = create_engine(URL_DATABASE)

SenssionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
