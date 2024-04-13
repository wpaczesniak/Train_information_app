import datetime
from sqlalchemy.orm import sessionmaker
from database_manager import DatabaseManager
from models import Train, TrainRoute, TrainStop, Station
from sqlalchemy import create_engine


db_manager = DatabaseManager('sqlite:///database.db')
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

def get_station_info(train_number):
    session = Session()
    try:

        routes = session.query(TrainRoute).filter(TrainRoute.train_number == train_number).all()

        for route in routes:
            stops = session.query(TrainStop).filter(TrainStop.stop_id == route.stop_id).all()

            for stop in stops:
                station = session.query(Station).filter(Station.station_id == stop.station_id).first()
                if station:
                    print(f"Station: {station.name}, Platform: {station.platform}, Track: {station.track}, "
                          f"Arrival Time: {stop.arrival_time}, Departure Time: {stop.departure_time}")
    finally:
        session.close()

get_station_info(13100)