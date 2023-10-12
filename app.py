from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
import datetime as dt

app = Flask(__name__)

# Keep track of the current option (entry or exit)
current_option = None

response_id_name = None


api_key = '031b2bd7255f167'

@app.route('/')
def home():
    return render_template('entry_exit.html')

@app.route('/scan/<option>', methods=['GET', 'POST'])
def scan(option):
    global current_option
    current_option = option

    if request.method == 'POST':
        # Handle the form submission here (e.g., start QR code scanning)
        # You can implement the QR code scanning logic in this section

        return redirect(url_for('result'))
    
    return render_template('scanqr.html', option=option)

@app.route('/result')
def result():
    decoded_data = request.args.get('data')
    api_url = f'http://127.0.0.1:8000/api/resource/housekeeping/{decoded_data}'
    params = {
    'fields': ['name_housekeeping', 'housekeeping_id'],  # Specify the fields you want to retrieve
        }
    # Authentication headers
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    data = {}  # Initialize data with an empty dictionary

    try:
        # Make a GET request to retrieve data
        response = requests.get(api_url, headers=headers,params=params)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            # Process and use the data as needed
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

    current_time_in_24_hours = datetime.now().strftime("%H:%M:%S")

    if data:
        for d in data.values():
            name = d['name_']
            id = d['housekeeping_id']
            phone_number = d['phone_number']
        time = current_time_in_24_hours

        if current_option == 'entry':

            api_url1 = "http://127.0.0.1:8000/api/resource/housekeeping_available"


            # Data to send to ERPNext
            data = {
                "data": {
                    "name_available": decoded_data,
                    # "available_id": id,
                    # "phonenumber": phone_number,
                }
            }
            headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            }

            response = requests.post(api_url1, json=data, headers=headers)
        

            if response.status_code == 200:
                print("Record created successfully.")
            else:
                print("Error:", response.status_code, response.text)
            
            api_url3 = f"http://127.0.0.1:8000/api/resource/houskeeping_attendance"

            today_date = dt.date.today()

            formatted_date = today_date.strftime("%d-%m-%Y")

             # Data to send to ERPNext
            data = {
                "data": {
                    "emp_id": decoded_data,
                    # "available_id": id,
                    # "phonenumber": phone_number,
                    "in_time" : current_time_in_24_hours,
                    "present_date" : formatted_date
                }
            }
            headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            }

            response = requests.post(api_url3, json=data, headers=headers)
        

            if response.status_code == 200:
                print("Record created successfully.")
            else:
                print("Error:", response.status_code, response.text)

            return render_template('result.html', decoded_data=decoded_data,name=name,id=decoded_data,time=time, option=current_option)
        else:
            api_url1 = f"http://127.0.0.1:8000/api/resource/housekeeping_available/{id}-{decoded_data}"

            # Data to send to ERPNext
            data = {
                "data": {
                    # "name_available": decoded_data,
                    # "available_id": id,
                    # "phonenumber": phone_number,
                    # "custom_availability_" : "Not Available"
                }
            }
            headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            }

            response = requests.delete(api_url1, json=data, headers=headers)

            if response.status_code == 200:
                print("Record created successfully.")
            else:
                print("Error:", response.status_code, response.text)

            today_date = dt.date.today()

            formatted_date = today_date.strftime("%d-%m-%Y")

            api_url3 = f"http://127.0.0.1:8000/api/resource/houskeeping_attendance/{decoded_data}-{id}-{formatted_date}"

             # Data to send to ERPNext
            data = {
                "data": {
                    # "name_available": decoded_data,
                    # "available_id": id,
                    # "phonenumber": phone_number,
                    # "in_time" : current_time_in_24_hours,
                    # "present_date" : formatted_date
                    "out_time" : current_time_in_24_hours
                }
            }
            

            headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            }

            response = requests.put(api_url3, json=data, headers=headers)
        

            if response.status_code == 200:
                print("Record created successfully.")
            else:
                print("Error:", response.status_code, response.text)

            return render_template('exit_result.html', decoded_data=decoded_data,name=name,id=id,time=time, option=current_option)
    else:
        return render_template('user_not_found.html')

@app.route('/end.html')
def end():
    return render_template('/end.html')

@app.route('/exit_end.html')
def exit_end():
    return render_template('/exit_end.html')

@app.route('/exit_result.html')
def exit_result():
    return render_template('/exit_result.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001)

