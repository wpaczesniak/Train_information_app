from flask import Flask, redirect, render_template, request, session, url_for
from models import Base, Train, Locomotive, TrainStop, TrainRoute, Car, Station
from add_sample_data import add_sample_data
from database_manager import DatabaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__, template_folder='templates')
app.secret_key = '5872399745248662' 
db_manager = DatabaseManager('sqlite:///database.db')
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def add_sample_data_to_db():
    with Session() as session:
        add_sample_data(session)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/results', methods=['GET', 'POST'], endpoint='results_get_post')
def results_get_post():
    if request.method == 'POST':
        session['train_number'] = request.form['train_number']
        session['station_name'] = request.form['station_name']
    train_number = session.get('train_number', '')
    station_name = session.get('station_name', '')
    train_details = get_detailed_train_info(train_number, station_name)
    return render_template('information.html', train_details=train_details)

@app.route('/results', methods=['POST'], endpoint='results_post')
def results_post():
    train_number = request.form['train_number']
    station_name = request.form['station_name']
    info = get_train_schedule_info(train_number, station_name)
    return render_template('information.html', info=info)
@app.route('/details/<train_number>/<station_name>')
def details(train_number, station_name):
    train_details = get_detailed_train_info(train_number, station_name)
    return render_template('details.html', train_details=train_details, locomotive=train_details.get('locomotive'), cars=train_details.get('cars'))

def get_detailed_train_info(train_number, station_name):
    train_info = {}
    db_session = Session()
    try:
        stop = db_session.query(TrainStop).join(Station).join(TrainRoute).join(Train).filter(Station.name == station_name, Train.train_number == train_number).first()
        if stop:
            locomotive_obj = db_session.query(Locomotive).filter(Locomotive.train_number == train_number).first()
            cars_obj = db_session.query(Car).filter(Car.train_number == train_number).all()

            locomotive = {
                'type': locomotive_obj.type,
                'side_number': locomotive_obj.side_number
            } if locomotive_obj else None

            cars = [{
                'car_number': car.car_number,
                'class_type': car.class_type
            } for car in cars_obj]

            train_info = {
                'train_number': train_number,
                'station_name': station_name,
                'locomotive': locomotive,
                'cars': cars
            }
    finally:
        Session.remove()
    return train_info

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        train_number = request.form['train_number']
        station = request.form['station']
        return redirect(url_for('home')) 
    return render_template('form.html')

@app.route('/informations', methods=['POST'])
def results():
    # train_number = request.form['train_number']
    # station_name = request.form['station_name']
    if request.method == 'POST':
        session['train_number'] = request.form['trainNumber']
        session['station_name'] = request.form['stationName']   
    train_number = session.get('train_number', '')
    station_name = session.get('station_name', '')
    info = get_train_schedule_info(train_number, station_name)
    return render_template('results.html', info=info)

def get_train_schedule_info(train_number, station_name):
    db_session = Session()
    try:

        stop = (db_session.query(TrainStop, Station)
                .join(Station)
                .join(TrainRoute, TrainStop.stop_id == TrainRoute.stop_id)
                .join(Train, TrainRoute.train_number == Train.train_number)
                .filter(Train.train_number == train_number, Station.name == station_name)
                .first())
        
        if stop:
            train_stop, station = stop
            return {
                "train_number": train_number,
                "station": station.name,
                "arrival_time": train_stop.arrival_time.strftime('%H:%M') if train_stop.arrival_time else None,
                "departure_time": train_stop.departure_time.strftime('%H:%M') if train_stop.departure_time else None,
                "platform": station.platform,
                "track": station.track
            }
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        db_session.close()

@app.route('/route')
def route():
    return render_template('route.html')  

@app.route('/route_results', methods=['POST'])
def route_results():
    train_number = request.form['train_number']
    route_info = get_station_info(train_number)
    return render_template('route_results.html', route_info=route_info)  # create new route_results.html template

def get_station_info(train_number):
    db_session = Session()
    route_info = []
    try:
        routes = db_session.query(TrainRoute).filter(TrainRoute.train_number == train_number).all()

        for route in routes:
            stops = db_session.query(TrainStop).filter(TrainStop.stop_id == route.stop_id).all()

            for stop in stops:
                station = db_session.query(Station).filter(Station.station_id == stop.station_id).first()
                if station:
                    route_info.append({
                        "station": station.name,
                        "platform": station.platform,
                        "track": station.track,
                        "arrival_time": stop.arrival_time.strftime('%H:%M') if stop.arrival_time else None,
                        "departure_time": stop.departure_time.strftime('%H:%M') if stop.departure_time else None
                    })
    finally:
        db_session.close()
    return route_info

if __name__ == '__main__':
    add_sample_data_to_db()
    app.run(debug=True, port=3941)