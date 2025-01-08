import json
import requests
import subprocess
from geopy.geocoders import Nominatim
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static\\'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
p1 = '/static/world-map.jpg'
@app.route('/', methods=['GET',"POST"])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data 
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) 

        expected_path = get_top_image_from_static()
        image_path = f"C:/Users/Saray/OneDrive/Desktop/MINI PROJECT2/static/{expected_path}" 
        metadata = exif_read(image_path)
        #print(metadata)
        latitude = metadata['GPS Latitude']
        longitude = metadata['GPS Longitude']
        if 'GPS Date/Time' in metadata:
            timestamp=metadata['GPS Date/Time']
        elif 'Date/Time Original' in metadata:
            timestamp = metadata['Date/Time Original']
        else:
            timestamp = metadata['GPS Time Stamp']
        lat = convert_to_decimal(latitude)
        long = convert_to_decimal(longitude)
        location_info = reverse_geocode(lat, long)
        pin=str(location_info['pin'])
        print(pin)
        ENDPOINT = "https://api.postalpincode.in/pincode/"
        response = requests.get(ENDPOINT+pin)
        pincode_info = json.loads(response.text)
        area=location_info['area_name']
        country=location_info['country']
        state = pincode_info[0]['PostOffice'][0]['State']
        district = pincode_info[0]['PostOffice'][0]['District']
        location=f"{pin}, {area}, {district}, {state}, {country}"
        path = f'/static/{expected_path}'
        return render_template("Geo.html", latitude=lat, longitude=long, path = path,timestamp=timestamp,location=location)
    return render_template('index.html', form = form, path = p1)

def get_top_image_from_static():
    static_dir = 'static'  
    for z in  os.listdir(static_dir):
        print(z)

    image_files = [f for f in os.listdir(static_dir) if os.path.isfile(os.path.join(static_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    dict = {}
    for i in image_files:
        var = os.path.getctime(f"static/{i}")
        dict[var] = i
    var = sorted(dict.keys())
    return dict[var[-1]]

def exif_read(img):
    com = r'C:\Program Files\EXIFTOOL\exiftool'
    command = [com, img]
    
    try:
        # Using subprocess.run() for better control and exception handling
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        
        # Check for any errors
        if result.stderr:
            return f"Error: {result.stderr.strip()}"
        
        output = result.stdout.strip()
        if not output:
            return "No output from ExifTool"
        
        # Parse the output into a dictionary
        data = {}
        for line in output.splitlines():
            if ':' in line:  # Checking if ':' exists to avoid any format issues
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
                
        return data

    except subprocess.TimeoutExpired:
        return "Process killed due to timeout"
    except FileNotFoundError:
        return "ExifTool not found. Please check the path."
    except Exception as e:
        return f"Error: {e}"

def convert_to_decimal(coord_str):
    parts = coord_str.split(' ')
    degrees = float(parts[0])
    minutes = float(parts[2][:-1]) 
    seconds = float(parts[3][:-1])  
    direction = parts[4]
    decimal_degrees = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    
    return decimal_degrees
def reverse_geocode(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="reverse_geocode")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        address = location.address.split(', ')
        print(address)
        pin = None
        area_name = None
        country = None
        for component in address:
            if component.isdigit():
                pin = component
            elif component.isalpha():
                country = component
            else:
                area_name = component
        
        return {
            'pin': pin,
            'area_name': area_name,
            'country': country
        }
    except Exception as e:
        print("Error:", e)
        return None

app.run()