#!/usr/bin/python3
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
secret_key = '.'.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    password_hash = Column(String(64), nullable=False)
    
    def hash_pass_word(self, password):
        self.password_hash = pwd_context.encrypt(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user_id = data['id']
        return user_id
    

class Shops(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    shoppingsite = Column(String, nullable=False)
    orderid = Column(String, nullable=False, unique=True)
    orderdate = Column(String, nullable=False)
    ordertime = Column(String, nullable=False)
    productname = Column(String, nullable=False)
    producttype = Column(String, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        return{
            'shoopingsite' : self.shoopingsite,
            'orderid' : self.orderid,
            'orderdate' : self.orderdate,
            'ordertime' : self.ordertime,
            'productname' : self.productname,
            'producttype' : self.producttype,
            'status' : self.status,
        }
    
    
    
    
engine = create_engine('sqlite:///mydb.db')

Base.metadata.create_all(engine)