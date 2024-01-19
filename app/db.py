from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースの設定
DB_USER = 'sikaku3'
DB_PASSWORD = 'Shikaku3'
DB_HOST = '192.168.54.231'
DB_NAME = 'sikaku3'

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String(4), index=True)
    item_name = Column(String(100), index=True)
    price = Column(Integer)


class Voucher(Base): 
    __tablename__ = "voucher"
    
    voucher_id = Column(String(4), ForeignKey("voucherType.voucher_id"), primary_key=True)
    user_id = Column(String(4), ForeignKey("user.user_id"))
    voucher_name = Column(String(100))
    deadline = Column(DateTime)


class VoucherType(Base): 

    __tablename__ = "voucherType" 

    voucher_id = Column(String(4), primary_key=True) 
    voucher_name = Column(String(100)) 


class User(Base): 
    __tablename__ ="user" 

    user_id =Column(String(4), primary_key=True) 
    user_name =Column(String(100)) 


class Exam(Base): 
    __tablename__="exam" 

    exam_id =Column(String(4), primary_key=True) 
    exam_name =Column(String(100)) 



class Sikaku(Base): 
    __tablename__ = "sikaku" 

    exam_id = Column(String(4), ForeignKey("exam.exam_id"), primary_key=True) 
    user_id = Column(String(4), ForeignKey("user.user_id")) 
    exam_name =Column(String(100)) 
    pass_date = Column(DateTime) 


# テーブルが存在しない場合は作成する
Base.metadata.create_all(bind=engine)
