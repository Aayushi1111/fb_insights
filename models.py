from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String) 
    username = Column(String, unique=True, index=True)
    page_name = Column(String)
    followers_count = Column(Integer)
    category = Column(String)
    posts = relationship("Post", back_populates="page")
    followers = relationship("Follower", back_populates="page")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    page_id = Column(Integer, ForeignKey('pages.id'))
    page = relationship("Page", back_populates="posts")

class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    page_id = Column(Integer, ForeignKey('pages.id'))
    page = relationship("Page", back_populates="followers")