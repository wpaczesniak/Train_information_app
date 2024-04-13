from sqlalchemy.orm import sessionmaker
from database_manager import DatabaseManager
from models import Train, Locomotive, Car, TrainStop, Station
from sqlalchemy import create_engine


db_manager = DatabaseManager('sqlite:///database.db')
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

def get_train_details(train_number, station_name):
    session = Session()
    try:
        stop = session.query(TrainStop).join(Station).filter(Station.name == station_name).first()
        if stop:
            locomotive = session.query(Locomotive).filter(Locomotive.train_number == train_number).first()
            if locomotive:
                print(f"Locomotive Type: {locomotive.type}, Side Number: {locomotive.side_number}")

            cars = session.query(Car).filter(Car.train_number == train_number).all()
            if cars:
                print("List of Cars:")
                for car in cars:
                    print(f"Car Number {car.car_number}, Class: {car.class_type}")
            else:
                print("No cars in this train.")
        else:
            print("The train does not pass through the given station.")
    finally:
        session.close()


get_train_details(13100, 'Bochnia')