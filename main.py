from sqlalchemy import create_engine, ForeignKey, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import os
import logging
from dotenv import load_dotenv


load_dotenv(".env", verbose=True)

db_user = os.environ['PGUSER']
db_password = os.environ['PGPASSWORD']
db_host = os.environ['PGHOST']
db_port = os.environ['PGPORT']
db_name = os.environ['PGDATABASE']
url = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'  
)

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class users(Base):
    __tablename__ = "users"
    userID = Column(String, primary_key=True, default=generate_uuid)
    firstName = Column(String)
    lastName = Column(String)
    profileName = Column(String)
    email = Column(String)

    def __init__(self, firstName, lastName, profileName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.profileName = profileName
        self.email = email

class post(Base):
    __tablename__ = "post"
    postId = Column(String, primary_key=True, default=generate_uuid)
    userId = Column(String, ForeignKey("users.userID"))
    postContent = Column(String)

    def __init__(self, userId, postContent):
        self.userId = userId
        self.postContent = postContent

class likes(Base):
    __tablename__ = "likes"
    likeId = Column(String, primary_key=True, default=generate_uuid)
    userId = Column(String, ForeignKey("users.userID"))
    postId = Column(String, ForeignKey("post.postId"))

    def __init__(self, userId, postId):
        self.userId = userId
        self.postId = postId

def addUser(firstName, lastName, profileName, email, session):
    exist = session.query(users).filter(users.email == email).all()
    if len(exist) > 0:
        print("Email Address already exists")
    else:
        user = users(firstName, lastName, profileName, email)
        session.add(user)
        session.commit()
    logging.info("User added to database")

def addPost(userId, postContent, session):
    newPost = post(userId, postContent)
    session.add(newPost)
    session.commit()

def addLike(userId, postId, session):  # Added session argument here
    like = likes(userId, postId)
    session.add(like)
    session.commit()
    logging.info("Like was added")

# Connect to the PostgreSQL database
engine = create_engine(url)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

firstName = "Kyle"
lastName = "Jackson"
profileName = "kayJ86"
email = "kyle@gmail.com"
addUser(firstName, lastName, profileName, email, session)

userId = "270788d2-6a1a-496a-a845-7e26e16c64aa"
postId = "c1a4292a-c51d-4aa4-8d2c-500aee3cb933"
postContent = "Summer Season is upon us"
addPost(userId, postContent, session)

# Retrieve and print all posts for the user
allPost = session.query(post).filter(post.userId == userId).all()
userPost = [p.postContent for p in allPost]
print(userPost)

# Add a like and check post likes
addLike(userId, postId, session)
postLikes = session.query(likes).filter(likes.postId == postId).all()
print(len(postLikes))

# Retrieve users who liked the post
usersLikedPost = session.query(users, likes).filter(likes.postId == postId).filter(likes.userId == users.userID)
for u, l in usersLikedPost:
    logging.info(f'{u.firstName} {u.lastName}')  # Proper logging format
