from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bleach
import os
from werkzeug.exceptions import BadRequest
from flask import Flask, render_template, request
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garden_journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')  # Change this to a strong, random value
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'note': self.note,
            'timestamp': self.timestamp.isoformat()
        }

@app.route('/', methods=['GET', 'POST'])
def home():
    current_weather = get_weather_data()
    historical_weather = get_weather_history('2022-09-15')
    notable_events = get_notable_events()

    return render_template('weather.html', weather=current_weather,
                               historical=historical_weather,
                               events=notable_events)

@app.route('/notes')
def hello_world():
    return render_template('index.html')

@app.route('/add_note', methods=['POST'])
def add_note():
    try:
        data = request.json
        note_text = bleach.clean(data.get('note', ''))
        timestamp = data.get('timestamp')
        
        if not note_text or not timestamp:
            raise BadRequest("Note and timestamp are required")
        
        new_note = Note(note=note_text, timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')))
        db.session.add(new_note)
        db.session.commit()
        return jsonify({"success": True, "message": "Note added successfully"})
    except BadRequest as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error adding note: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred while processing your request"}), 500

@app.route('/get_notes', methods=['GET'])
def get_notes():
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return jsonify({"success": True, "notes": [note.to_dict() for note in notes]})


def get_weather_data():
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Elizabeth%2C%20co?unitGroup=us&include=days&key=UXPDT232ETZ86LY2L8DD2G3JP&contentType=json"

    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        current_day = data['days'][0]  # Get the first day's data

        # Create an array of days with specified data
        days_array = [{
            'dow': datetime.strptime(day['datetime'], '%Y-%m-%d').strftime('%a'),
            'dom': datetime.strptime(day['datetime'], '%Y-%m-%d').strftime('%-d'),
            'tempmin': day['tempmin'],
            'tempmax': day['tempmax'],
            'precipprob': day['precipprob'],
            'icon': day['icon']
        } for day in data['days'][:15]]  # Limit to 7 days for a week's forecast

        print(current_day['icon'])
        return {
            'city': data['address'],
            'temperature': current_day['temp'],
            'description': current_day['description'],
            'icon': current_day['icon'],
            'humidity': current_day['humidity'],
            'wind_speed': current_day['windspeed'],
            'temp_max': current_day['tempmax'],
            'temp_min': current_day['tempmin'],
            'rain': current_day['precip'],
            'rain_prob': current_day['precipprob'],
            'snow': current_day['snow'],
            'snow_depth': current_day['snowdepth'],
            'cloud_cover': current_day['cloudcover'],
            'days': days_array
        }
    return None

def get_weather_history(date):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Elizabeth%2Cco/2023-09-16/2023-09-16?unitGroup=us&include=days%2Calerts%2Cevents%2Ccurrent&key=UXPDT232ETZ86LY2L8DD2G3JP&contentType=json"

    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        return {
            'description': data['days'][0]['description'],
            'icon': data['days'][0]['icon'],
            'temp_max': data['days'][0]['tempmax'],
            'temp_min': data['days'][0]['tempmin']
        }
    return None

def get_notable_events():
    from datetime import datetime, timedelta
    import json

    with open('events.json', 'r') as f:
        data = json.load(f)
    
    elizabeth_data = data.get("Elizabeth, CO", {})
    gardening_calendar = elizabeth_data.get("gardening_calendar", {})
    
    current_date = datetime.now().date()
    three_weeks = timedelta(weeks=3)
    start_date = current_date - three_weeks
    end_date = current_date + three_weeks
    
    print(f"Date range: {start_date} to {end_date}")

    notable_events = {}
    for event in gardening_calendar.get("notable_events", []):
        try:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            # Create comparison dates with the current year
            event_date_this_year = event_date.replace(year=current_date.year)
            if event_date_this_year < current_date:
                event_date_this_year = event_date_this_year.replace(year=current_date.year + 1)
            
            print(f"Checking event: {event['event']} on {event_date_this_year}")
            if start_date <= event_date_this_year <= end_date:
                notable_events[event["event"]] = event["date"]
                print(f"Added event: {event['event']}")
            #else:
                #print(f"Event out of range: {event['event']}")
        except ValueError as e:
            print(f"Error parsing date for event: {event['event']}")
            print(f"Date string: {event['date']}")
            print(f"Error message: {str(e)}")
    
    print(f"Total events in range: {len(notable_events)}")

    planting_schedule = {}
    for crop in gardening_calendar.get("planting_schedule", []):
        try:
            crop_events = {}
            for event_type in ["sow_indoors", "sow_in_greenhouse", "transplant_to_greenhouse", "transplant_outdoors", "direct_sow_outdoors", "plant_bare_root", "plant_bulbs", "plant_cloves"]:
                if event_type in crop:
                    print(event_type)
                    event_date = datetime.strptime(crop[event_type], "%Y-%m-%d").date()
                    event_date_this_year = event_date.replace(year=current_date.year)
                    if event_date_this_year < current_date:
                        event_date_this_year = event_date_this_year.replace(year=current_date.year + 1)
                    
                    if start_date <= event_date_this_year <= end_date:
                        crop_events["event_type"] = event_type.replace("_", " ").capitalize()
                        crop_events["event_date"] = event_date_this_year.strftime("%Y-%m-%d")
            
                        for key, value in crop.items():
                            if key not in ["crop"] and not isinstance(value, dict):
                                crop_events[key] = value
                        
                        if crop_events:
                            planting_schedule[crop["crop"]] = crop_events
                        #else:
                            #print(f"No relevant events for: {crop['crop']}")
        except ValueError as e:
            print(f"Error parsing date for crop: {crop['crop']}")
            print(f"Date string: {crop[event_type]}")
            print(f"Error message: {str(e)}")

    
    print(f"Total crops in planting schedule: {len(planting_schedule)}")
    return {
        "notable_events": notable_events,
        "planting_schedule": planting_schedule
    }


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=False)

