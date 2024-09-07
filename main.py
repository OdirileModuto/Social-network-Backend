from sqlalchemy import create_engine, ForeignKey, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())

class users (Base):
    __tablename__ = "users"
    userID = Column("userID",String, primary_key= True, default= generate_uuid)
    firstName= Column("firstName", String)
    lastName= Column("lastName",String)
    profileName= Column("profileName",String)
    email = Column ("email", String)  


    def __init__ ( self,firstName,lastName,profileName,email):
        self.firstName = firstName
        self.lastName = lastName
        self.profileName = profileName
        self.email = email 

class post (Base):
    __tablename__ = "post"
    postId = Column ("postId", String, primary_key=True, default= generate_uuid)
    userId = Column ("userId", String, ForeignKey("users.userID"))
    postContent = Column ("postContent", String)

    def __init__(self,userId, postContent):
        self.userId = userId
        self.postContent = postContent

class likes (Base):
    __tablename__ = "likes"
    likeId = Column("likeId",String, primary_key= True, default= generate_uuid)
    userId = Column("userId", String, ForeignKey ("users.userID"))
    postId = Column("postId", String, ForeignKey ("post.postId"))

    def __init__ (self,userId,postId):
        self.userId = userId
        self.postId = postId
 

def addUser(firstName, lastName, profileName, email,session): 

    exist = session.query(users).filter(users.email==email).all()
    if len(exist)>0:
        print("Email Address already exist")
    else:
        user = users(firstName,lastName,profileName,email)
        session.add(user)
        session.commit()
    print ("User added to database")


def addPost( userId,postContent,session):
    newPost = post (userId,postContent)  
    session.add(newPost)
    session.commit()


def addLike(userId, postId):
    like= likes(userId,postId)
    session.add(like)
    session.commit()
    print("like was added")

    
            

db = "sqlite:///socialDB.db"   
engine = create_engine(db)
Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()


firstName = " Clark"
lastName = "Histon"
profileName = "Clark8741"
email = "Clark94@gmail.com"
addUser(firstName,lastName,profileName,email,session)

#  create a post    
userId ="1aedd157-f782-4159-a64a-d36779923416"
postId = "0b699f3c-a960-41f6-b405-11164eaae000"
postContent ="Finaly My code is Working"
addPost(userId,postContent,session)
allPost = session.query(post).filter(post.userId == userId).all()
userPost = []
for p in allPost:
    userPost.append(p.postContent)
    print(userPost)
addLike(userId, postId)
postLikes = session.query(likes).filter(likes.postId==postId).all()
print(len(postLikes))

usersLikedPost = session.query(users,likes).filter(likes.postId==postId).filter(likes.userId==users.userID)
for u, l in usersLikedPost:
    print(u.firstName,u.lastName)

