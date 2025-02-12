import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from eralchemy import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comments', back_populates='author')
    followers = relationship('Follower', back_populates='user_from')
    following = relationship('Follower', back_populates='user_to')


class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    users = relationship('User', back_populates='posts')
    commets =relationship('Comment', back_populates='Post')
    media =relationship('Media', back_populates='Post')

class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')


class Media(Base):
    __tablename__= 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    post = relationship('Post', back_populates='media')
    

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    user_to_id: Mapped[int] = mapped_column(nullable=False, primary_key=True)

    user_from = relationship('User', back_populates='followers', foreign_keys=[user_from_id])
    user_to = relationship('User', back_populates='following', foreign_keys=[user_to_id])


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
