from sqlalchemy import create_engine, Column, Integer, String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Locomotive(Base):
    __tablename__ = 'locomotive'
    locomotive_id = Column(Integer, primary_key=True)
    side_number = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    train_number = Column(BigInteger, ForeignKey('train.train_number'))

    train = relationship("Train", back_populates="locomotive")

class Train(Base):
    __tablename__ = 'train'
    train_number = Column(Integer, primary_key=True)
    train_name = Column(String(50), nullable=False)
    number_of_cars = Column(Integer, nullable=False)

    locomotive = relationship("Locomotive", back_populates="train", uselist=False)
    cars = relationship("Car", back_populates="train")
    route = relationship("TrainRoute", back_populates="train")
    tickets = relationship("Ticket", back_populates="train")

class Car(Base):
    __tablename__ = 'car'
    car_id = Column(Integer, primary_key=True)
    train_number = Column(Integer, ForeignKey('train.train_number'))
    class_type = Column(String, nullable=False)
    number_of_seats = Column(Integer, nullable=False)
    car_number = Column(Integer, nullable=False)
    has_conductor = Column(Boolean, default=False)

    train = relationship("Train", back_populates="cars")

class TrainRoute(Base):
    __tablename__ = 'train_route'
    route_id = Column(Integer, primary_key=True)
    train_number = Column(Integer, ForeignKey('train.train_number'))
    stop_id = Column(Integer, ForeignKey('train_stop.stop_id'))

    stop = relationship("TrainStop", back_populates="route")
    train = relationship("Train", back_populates="route")

class TrainStop(Base):
    __tablename__ = 'train_stop'
    stop_id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey('station.station_id'))
    arrival_time = Column(DateTime, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    
    station = relationship("Station", back_populates="stops")
    route = relationship("TrainRoute", back_populates="stop")

class Station(Base):
    __tablename__ = 'station'
    station_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    platform = Column(Integer, nullable=False)
    track = Column(Integer, nullable=False)

    stops = relationship("TrainStop", back_populates="station")

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    tickets = relationship("Ticket", back_populates="user")

class Ticket(Base):
    __tablename__ = 'ticket'
    ticket_id = Column(Integer, primary_key=True)
    train_number = Column(Integer, ForeignKey('train.train_number'))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    train = relationship("Train", back_populates="tickets")
    user = relationship("User", back_populates="tickets")


engine = create_engine('sqlite:///database.db')

Base.metadata.create_all(engine)