"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Josh Chapman

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}

Outline of API calls to server

1) Use TOP_API_URL to get the dictionary above
2) Add "6" to the end of the films endpoint to get film 6 details
3) Use as many threads possible to get the names of film 6 data (people, starships, ...)

"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class APIThread(threading.Thread):
    

    def __init__(self, url, result_list):
        threading.Thread.__init__(self)
        self.url = url
        self.result_list = result_list

    def run(self):
        global call_count
        try:
            response = requests.get(self.url)
            call_count += 1
            data = response.json()

            # Thread-safe addition to the result list
            with threading.Lock():
                self.result_list.append(data)
        except Exception as e:
            print(f'Error getting {self.url}: {e}')

# TODO Add any functions you need here

def fetch_data_concurrently(urls):
    result_list = []
    threads = []

    for url in urls:
        thread = APIThread(url, result_list)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result_list
def return_datetime():
    return f'{datetime.now().strftime("%H:%M:%S")}| '

def print_info(dictionary):
    print(return_datetime() + '----------------------------------------')
    # Print Title
    print(return_datetime() + 'Title   : ' + dictionary['title'])
    # Print Director
    print(return_datetime() + 'Director: ' + dictionary['director'])
    # Print Producer
    print(return_datetime() + 'Producer: ' + dictionary['producer'])
    # Released
    print(return_datetime() + 'Released: ' + dictionary['release_date'])
    print(return_datetime())

    # Character Count
    print(f'{return_datetime()}Characters: {len(dictionary['characters'])}')
    # Character List, , ,
    characters = fetch_data_concurrently(dictionary['characters'])
    print(return_datetime(),end='')
    name_list = [c['name'] for c in characters]
    name_list.sort()
    print(', '.join(name_list))
    print(return_datetime())

    
    # Planet Count
    print(f'{return_datetime()}Planets: {len(dictionary['planets'])}')
    # Planet List, , ,
    planets = fetch_data_concurrently(dictionary['planets'])
    print(return_datetime(),end='')
    planet_list = [c['name'] for c in planets]
    planet_list.sort()
    print(', '.join(planet_list))
    print(return_datetime())

    # Starships Count
    print(f'{return_datetime()}Starships: {len(dictionary['starships'])}')
    # Starships List, , ,
    starships = fetch_data_concurrently(dictionary['starships'])
    print(return_datetime(),end='')
    ship_list = [c['name'] for c in starships]
    ship_list.sort()
    print(', '.join(ship_list))
    print(return_datetime())

    # Vehicles Count
    print(f'{return_datetime()}Vehicles: {len(dictionary['vehicles'])}')
    # Vehicles List, , ,
    vehicles = fetch_data_concurrently(dictionary['vehicles'])
    print(return_datetime(),end='')
    vehicle_list = [c['name'] for c in vehicles]
    vehicle_list.sort()
    print(', '.join(vehicle_list))
    print(return_datetime())

    # Species Count
    print(f'{return_datetime()}Species: {len(dictionary['species'])}')
    # Species List, , ,
    species = fetch_data_concurrently(dictionary['species'])
    print(return_datetime(),end='')
    species_list = [c['name'] for c in species]
    species_list.sort()
    print(', '.join(species_list))
    print(return_datetime())

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    top_level_result = fetch_data_concurrently([TOP_API_URL])

    # TODO Retrieve Details on film 6
    film_6_url = f"{top_level_result[0]['films']}6"
    film_6_results  = fetch_data_concurrently([film_6_url])



    # TODO Display results
    print_info(film_6_results[0])

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()

    # response = requests.get(TOP_API_URL)

    # if response.status_code == 200:
    #     data = response.json()
    #     print(data)

    #     print('\nHere is the URL for person id = 1:', f'{data["people"]}1')
    # else:
    #     print('Error in requesting ID')