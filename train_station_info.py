from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Train, TrainRoute, TrainStop, Station

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

def get_train_schedule_info(train_number, station_name):
    session = Session()
    try:
        stops = session.query(TrainStop, Station, TrainRoute).join(Station).join(TrainRoute).filter(Station.name == station_name, TrainRoute.train_number == train_number).all()

        for stop, station, route in stops:
            if stop.stop_id == route.stop_id:
                print(f"Train Number: {route.train_number}, Station: {station.name}, "
                      f"Arrival Time: {stop.arrival_time}, Departure Time: {stop.departure_time}, "
                      f"Platform: {station.platform}, Track: {station.track}")
    finally:
        session.close()

get_train_schedule_info(13100, 'Bochnia')