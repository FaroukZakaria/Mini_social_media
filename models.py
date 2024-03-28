#!/usr/bin/python3
"""
Created models are here
"""


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

# Define your SQLAlchemy models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    is_admin = False
    # Define the one-to-many relationship with Post
    user_posts = relationship('Post', back_populates='author')
    user_likes = relationship('Like', back_populates='user')

    user_comments = relationship("Comment", back_populates="author")
    user_comment_likes = relationship("CommentLike", back_populates="user")


    def __repr__(self):
        return "<User(id={}, first name={}, last name={}, email={})>".format(
                self.id,
                self.firstname,
                self.lastname,
                self.email
                )

class Post(Base):
     __tablename__ = 'posts'

     id = Column(Integer, primary_key=True)
     content = Column(String(60), nullable=False)
     author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
     author = relationship("User", back_populates="user_posts")
     likes = Column(Integer, default=0)
     post_likes = relationship('Like', back_populates="post")
     post_comments = relationship("Comment", back_populates="post")
     post_comment_likes = relationship("CommentLike", back_populates="post")


     def __repr__(self):
         return "<Post(id={}, content={}, author={})>".format(
                self.id,
                self.content,
                self.author
                )


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    user = relationship("User", back_populates="user_likes")
    post = relationship("Post", back_populates="post_likes")

    def __repr__(self):
        return "<Like(id={}, user={}, post={})>".format(
                self.id,
                self.user,
                self.post
                )


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String(60), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    likes = Column(Integer, default=0)

    author = relationship("User", back_populates="user_comments")
    post = relationship("Post", back_populates="post_comments")
    comment_likes = relationship("CommentLike", back_populates="comment")

    def __repr__(self):
        return "<Comment(id={}, content={}, author={}, post={})>".format(
                self.id,
                self.content,
                self.author,
                self.post
                )


class CommentLike(Base):
    __tablename__ = 'comment_likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    user = relationship("User", back_populates="user_comment_likes")
    post = relationship("Post", back_populates="post_comment_likes")
    comment = relationship("Comment", back_populates="comment_likes")

    def __repr__(self):
        return "<CommentLike(id={}, user={}, comment={}, post={})>".format(
                self.id,
                self.user,
                self.comment,
                self.post
                )
