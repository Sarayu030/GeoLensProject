import json
import requests
ENDPOINT = "https://api.postalpincode.in/pincode/"
pincode = input("Enter the code: ")
response = requests.get(ENDPOINT+pincode)
pincode_info = json.loads(response.text)

state = pincode_info[0]['PostOffice'][0]['State']
district = pincode_info[0]['PostOffice'][0]['District']
print(district)
print(state)
