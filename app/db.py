
from db import Base
from sqlalchemy.orm import sessionmaker
from models import User, Post
from datetime import datetime

# Create an in-memory SQLite database
from sqlalchemy import create_engine

engine = create_engine("sqlite:///db.sqlite")
# Base.metadata.create_all(bind=engine)


# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# session = Session()


# # Create sample instances

# user1 = User(user_id=1, first_name="John", last_name="Doe")
# user2 = User(user_id=2, first_name="Alice", last_name="Smith")
# user3 = User(user_id=3, first_name="Bob", last_name="Johnson")
# post1 = Post(post_id=1, user_id=1, date=datetime(2023, 5, 17, 10, 30, 0))
# post2 = Post(post_id=2, user_id=2, date=datetime(2023, 5, 16, 15, 45, 0))
# post3 = Post(post_id=3, user_id=3, date=datetime(2023, 5, 15, 20, 0, 0))

# # Add instances to the session and commit
# session.add_all([user1, user2, user3, post1, post2, post3])
# session.commit()

# # Test querying the data
# print("Users:")
# users = session.query(User).all()
# for user in users:
#     print(user)

# print("\nPosts:")
# posts = session.query(Post).all()
# for post in posts:
#     print(post)


