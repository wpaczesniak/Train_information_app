import datetime
from sqlalchemy.orm import Session
from database_manager import DatabaseManager
from models import Locomotive, Train, Car, TrainRoute, TrainStop, Station, User, Ticket

def locomotive_exists(session: Session, side_number):
    return session.query(Locomotive).filter(Locomotive.side_number == side_number).first() is not None

def train_exists(session: Session, train_number):
    return session.query(Train).filter(Train.train_number == train_number).first() is not None

def car_exists(session: Session, car_id):
    return session.query(Car).filter(Car.car_id == car_id).first() is not None

def route_exists(session: Session, route_id):
    return session.query(TrainRoute).filter(TrainRoute.route_id == route_id).first() is not None

def stop_exists(session: Session, stop_id):
    return session.query(TrainStop).filter(TrainStop.stop_id == stop_id).first() is not None

def station_exists(session: Session, station_id):
    return session.query(Station).filter(Station.station_id == station_id).first() is not None

def user_exists(session: Session, email):
    return session.query(User).filter(User.email == email).first() is not None

def ticket_exists(session: Session, ticket_id):
    return session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first() is not None


db_manager = DatabaseManager('sqlite:///database.db')



def add_sample_data(session):
    # Adding Locomotives
    if not locomotive_exists(session, 1234):
        db_manager.add_locomotive(session, 1234, 'electric', 1)
    if not locomotive_exists(session, 2234):
        db_manager.add_locomotive(session, 2234, 'diesel', 2)
    if not locomotive_exists(session, 3234):
        db_manager.add_locomotive(session, 3234, 'electric', 3)


    if not train_exists(session, 1):
        db_manager.add_train(session, 1, 'Express', 10)
    if not train_exists(session, 2):
        db_manager.add_train(session, 2, 'Regional', 8)
    if not train_exists(session, 3):
        db_manager.add_train(session, 3, 'InterCity', 12)


    if not car_exists(session, 1):
        db_manager.add_car(session, 1, 1, 'first class', 20, 1, True)
    if not car_exists(session, 2):
        db_manager.add_car(session, 2, 2, 'first class', 30, 2, False)
    if not car_exists(session, 3):
        db_manager.add_car(session, 3, 3, 'second class', 40, 3, True)


    if not route_exists(session, 1):
        db_manager.add_train_route(session, 1, 1, 1)
    if not route_exists(session, 2):
        db_manager.add_train_route(session, 2, 2, 2)
    if not route_exists(session, 3):
        db_manager.add_train_route(session, 3, 3, 3)


    if not stop_exists(session, 1):
        arrival_time = datetime.datetime.now()
        departure_time = datetime.datetime.now()
        db_manager.add_train_stop(session, 1, 1, arrival_time, departure_time)
    if not stop_exists(session, 2):
        arrival_time_2 = datetime.datetime.now()
        departure_time_2 = datetime.datetime.now()
        db_manager.add_train_stop(session, 2, 2, arrival_time_2, departure_time_2)
    if not stop_exists(session, 3):
        arrival_time_3 = datetime.datetime.now()
        departure_time_3 = datetime.datetime.now()
        db_manager.add_train_stop(session, 3, 3, arrival_time_3, departure_time_3)


    if not station_exists(session, 1):
        db_manager.add_station(session, 1, 'Central', 1, 2)
    if not station_exists(session, 2):
        db_manager.add_station(session, 2, 'West', 2, 3)
    if not station_exists(session, 3):
        db_manager.add_station(session, 3, 'North', 1, 1)


    if not user_exists(session, 'jan.kowalski@example.com'):
        db_manager.add_user(session, 1, 'Jan', 'Kowalski', 'jan.kowalski@example.com')
    if not user_exists(session, 'anna.nowak@example.com'):
        db_manager.add_user(session, 2, 'Anna', 'Nowak', 'anna.nowak@example.com')
    if not user_exists(session, 'pawel.wisniewski@example.com'):
        db_manager.add_user(session, 3, 'Paweł', 'Wiśniewski', 'pawel.wisniewski@example.com')


    if not ticket_exists(session, 1):
        db_manager.add_ticket(session, 1, 1, 1)
    if not ticket_exists(session, 2):
        db_manager.add_ticket(session, 2, 2, 2)
    if not ticket_exists(session, 3):
        db_manager.add_ticket(session, 3, 3, 3)

    print("Sample data added.")
