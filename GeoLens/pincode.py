import requests

def get_district_and_state(pin_code):
    try:
        # Make request to Zippopotam API
        response = requests.get(f"https://api.zippopotam.us/IN/{pin_code}")
        data = response.json()
        
        # Extract district and state from the response
        places = data.get('places', [])
        if places:
            district = places[0].get('place name')
            state = places[0].get('state')
            return district, state
        else:
            print("Location not found for the given PIN code.")
            return None, None
    except Exception as e:
        print("Error:", e)
        return None, None

# Example usage
pin_code = '506370'
district, state = get_district_and_state(pin_code)
if district and state:
    print("District:", district)
    print("State:", state)
