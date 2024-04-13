from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Locomotive, Train, Car, TrainRoute, TrainStop, Station, User, Ticket
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.Session()

    def add_locomotive(self, session, side_number, type, train_number):
        locomotive = Locomotive(side_number=side_number, type=type, train_number=train_number)
        session.add(locomotive)
        session.commit()

    def add_train(self, session, train_number, train_name, number_of_cars):
        train = Train(train_number=train_number, train_name=train_name, number_of_cars=number_of_cars)
        session.add(train)
        session.commit()

    def add_car(self, session, car_id, train_number, class_type, number_of_seats, car_number, has_conductor):
        car = Car(car_id=car_id, train_number=train_number, class_type=class_type, number_of_seats=number_of_seats, car_number=car_number, has_conductor=has_conductor)
        session.add(car)
        session.commit()

    def add_train_route(self, session, route_id, train_number, stop_id):
        route = TrainRoute(route_id=route_id, train_number=train_number, stop_id=stop_id)
        session.add(route)
        session.commit()

    def add_train_stop(self, session, stop_id, station_id, arrival_time, departure_time):
        stop = TrainStop(stop_id=stop_id, station_id=station_id, arrival_time=arrival_time, departure_time=departure_time)
        session.add(stop)
        session.commit()

    def add_station(self, session, station_id, name, platform, track):
        station = Station(station_id=station_id, name=name, platform=platform, track=track)
        session.add(station)
        session.commit()

    def add_user(self, session, user_id, first_name, last_name, email):
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, email=email)
        session.add(user)
        session.commit()

    def add_ticket(self, session, ticket_id, train_number, user_id):
        ticket = Ticket(ticket_id=ticket_id, train_number=train_number, user_id=user_id)
        session.add(ticket)
        session.commit()

