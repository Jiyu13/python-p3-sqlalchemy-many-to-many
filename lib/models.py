from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///many_to_many.db')

Base = declarative_base()

# 4. build associate table - 
game_user = Table(
    'game_users',
    Base.metadata,
    Column('game_id', ForeignKey('games.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True,
)


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())

    reviews = relationship('Review', backref=backref('game'))

    # 3. build many-to-many relationship with User,
    # secondary => the intermediary table in m-m relationship
    # back_populates => be used on both side of a relationship
    users = relationship('User', secondary=game_user, back_populates='games')

    def __repr__(self):
        return f'Game(id={self.id}, ' + \
            f'title={self.title}, ' + \
            f'platform={self.platform})'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())
    
    game_id = Column(Integer(), ForeignKey('games.id'))

    # add fk to create relationship with User 
    user_id = Column(Integer(), ForeignKey('users.id'))

    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'score={self.score}, ' + \
            f'game_id={self.game_id})'



# 1. Create User model
class User(Base):

    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # 2. setup relationship with Review model
    reviews = relationship('Review', backref=backref('user'))

    # 3. build many-to-many relationship with Game
    games = relationship('Game', secondary=game_user, back_populates='users')

    def __repr__(self):
        return f'User(id={self.id}, ' + \
            f'name={self.name})'