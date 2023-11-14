from flask import Flask, request, jsonify
from xml.etree import ElementTree as ET
import requests

app = Flask(__name__)

def get_weather_data(city):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": city}
    headers = {
        "X-RapidAPI-Key": "YOUR_API_KEY",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def format_response(data, output_format):
    if output_format == "json":
        return jsonify({
            "Weather": f"{data['current']['temp_c']} C",
            "Latitude": str(data['location']['lat']),
            "Longitude": str(data['location']['lon']),
            "City": f"{data['location']['name']} {data['location']['country']}"
        })
    elif output_format == "xml":
        root = ET.Element("root")
        ET.SubElement(root, "Temperature").text = str(data['current']['temp_c'])
        ET.SubElement(root, "City").text = data['location']['name']
        ET.SubElement(root, "Latitude").text = str(data['location']['lat'])
        ET.SubElement(root, "Longitude").text = str(data['location']['lon'])
        return ET.tostring(root, encoding="unicode", method="xml")
    else:
        return jsonify({"error": "Invalid output_format. Use 'json' or 'xml'."})

@app.route('/getCurrentWeather', methods=['POST'])
def get_current_weather():
    print(request.get_json())
    try:
        req_data = request.get_json()
        city = req_data['city']
        output_format = req_data['output_format']
        weather_data = get_weather_data(city)
        if weather_data:
            return format_response(weather_data, output_format)
        else:
            return jsonify({"error": "Error retrieving weather data."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
