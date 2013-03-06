from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()


class User(Base):
    """ A Hackerspace User """
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    rfidkey = Column(String)

    def __init__(self, name, email, rfidkey):
        self.name = name
        self.email = email
        self.rfidkey = rfidkey


class UserDB(object):
    def __init__(self):
        echo = False  # Turn on to get debug sql on stdout
        self.engine = create_engine('sqlite:///users.db', echo=echo)
        Base.metadata.create_all(self.engine)

    def add_user(self, name, email, rfidkey):
        user = User(name, email, rfidkey)
        session = sessionmaker(bind=self.engine)()
        session.add(user)
        session.commit()

    def authenticate(self, rfidkey):
        session = sessionmaker(bind=self.engine)()
        res = session.query(User).filter(User.rfidkey == rfidkey)
        count = res.count()
        if count > 0:
            if count > 1:
                print "Internal error: More than one match!"
            return True
        else:
            return False


if __name__ == "__main__":
    db = UserDB()
#    db.add_user("Duncan Thomas", "duncan.thomas@gmail.com", "12345")
    print "Testing a valid key: %s" % db.authenticate("12345")
    print "Testing an invalid key: %s" % db.authenticate("00000")
