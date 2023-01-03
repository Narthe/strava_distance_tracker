from datetime import date
import calendar
import requests
import pprint
import json

# url to get the authorization code :
# https://www.strava.com/oauth/authorize?client_id=99446&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all
# - open that url
# - click authorize
# - in the next web page, copy the authorization code from the url
# - past that code below
# - run the script a first time letting only the authorize() function uncommented. this will create the strava_tokens.json file
# - comment the authorize function and uncomment the rest

host = "https://www.strava.com/api/v3"
athlete_url = f"{host}/athlete"
activities_url = f"{host}/activities"
access_token = "dc957b47d63349aee6dddb31cd8de96af48fdfe3"
client_id = "99446"
client_secret = "1535e9a29dc7f4a9381740c08010b708bda7cc9b"
authorization_code = "e9c5a85b795897ba684ea41cfaccf2b73949c76b"
my_headers = {'Authorization' : f'Bearer {access_token}'}

auth_url = f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={authorization_code}&grant_type=authorization_code"

def authorize():
    response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': client_id,
                            'client_secret': client_secret,
                            'code': authorization_code,
                            'grant_type': 'authorization_code'
                            }
                )
    #Save json response as a variable
    strava_tokens = response.json()
    # Save tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)
    # Open JSON file and print the file contents 
    # to check it's worked properly
    with open('strava_tokens.json') as check:
        data = json.load(check)
        pprint.pprint(data)

def get_current_year_activities():
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)
    access_token = strava_tokens['access_token']

    # first_day = date(date.today().year, 1, 1)
    # last_day = date(date.today().year, 12, 31)

    first_day = date(2022, 1, 1)
    last_day = date(2022, 12, 31)

    epoch_start = calendar.timegm(first_day.timetuple())
    epoch_end = calendar.timegm(last_day.timetuple())

    # Get first page of activities from Strava with all fields
    response = requests.get(activities_url + '?access_token=' + access_token + "&per_page=200" + f"&after={epoch_start}" + f"&before={epoch_end}")
    data = response.json()
    return data 

def get_distance(activities):
    distance = 0
    for activity in activities:
        if activity['type'] in ['Ride', 'VirtualRide']:
            dist = int(activity['distance'])
            # print(f"{dist} km")
            distance += dist
    return int(distance / 1000)

def main():
    # authorize() # Do this only once after you authorized from the web page
    # Get the tokens from file to connect to Strava
    activities = get_current_year_activities()
    print(f"Total distance = {get_distance(activities)} km")

main()