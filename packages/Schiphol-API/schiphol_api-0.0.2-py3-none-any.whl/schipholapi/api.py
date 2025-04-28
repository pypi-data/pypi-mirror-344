import requests


class SchipholAPI:
    def __init__(self, app_id: str = None, app_key: str = None):
        self.base_url = 'https://api.schiphol.nl/public-flights/{endpoint}'
        self.headers = {
            'accept': 'application/json',
            'resourceversion': 'v4',
            'app_id': app_id,
            'app_key': app_key
        }

    def _make_request(self, endpoint, params=None):
        """Internal helper function to make the API request with dynamic endpoint."""
        url = self.base_url.format(endpoint=endpoint)
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as error:
            print(f"Error during API request: {error}")
            return None

    def get_flights(self, page=0, include_delays=False, sort_by="scheduleTime"):
        """Fetch flight information."""
        params = {
            'includedelays': str(include_delays).lower(),
            'page': page,
            'sort': f"+{sort_by}"
        }
        endpoint = 'flights'
        response = self._make_request(endpoint, params)

        if response and response.status_code == 200:
            flight_list = response.json()
            print(f'Found {len(flight_list["flights"])} flights on page {page}.')
            for flight in flight_list['flights']:
                print(f'Flight: {flight["flightName"]}, Scheduled: {flight["scheduleDate"]} at {flight["scheduleTime"]}')
            return flight_list
        else:
            print(f"Failed to fetch flights: {response.status_code if response else 'No response'}")
            return None

    def get_flight(self, flight_id):
        """Fetch specific details about a flight."""
        endpoint = f"flights/{flight_id}"
        response = self._make_request(endpoint)

        if response and response.status_code == 200:
            flight_details = response.json()
            print(f"Details for flight {flight_id}:")
            print(f"Flight Name: {flight_details['flightName']}")
            return flight_details
        else:
            print(f"Failed to fetch flight details: {response.status_code if response else 'No response'}")
            return None

    def get_destinations(self, page=0, sort_by="publicName.english"):
        """Fetch a list of destinations."""
        params = {
            'page': page,
            'sort': f"+{sort_by}"
        }
        endpoint = 'destinations'
        response = self._make_request(endpoint, params)

        if response and response.status_code == 200:
            destinations = response.json()
            print(f'Found {len(destinations["destinations"])} destinations on page {page}.')
            for destination in destinations['destinations']:
                if "iata" in destination:
                    print(f"Destination: {destination['publicName']['english']}, IATA: {destination['iata']}")
            return destinations
        else:
            print(f"Failed to fetch destinations: {response.status_code if response else 'No response'}")
            return None

    def get_destination(self, destination_id):
        """Fetch specific details about a destination."""
        endpoint = f"destinations/{destination_id}"
        response = self._make_request(endpoint)

        if response and response.status_code == 200:
            destination_details = response.json()
            print(f"Details for destination {destination_id}:")
            print(f"Public Name: {destination_details['publicName']['english']}")
            return destination_details
        else:
            print(f"Failed to fetch destination details: {response.status_code if response else 'No response'}")
            return None

    def get_airlines(self, page=0, sort_by="publicName"):
        """Fetch a list of airlines."""
        params = {
            'page': page,
            'sort': f"+{sort_by}"
        }
        endpoint = 'airlines'
        response = self._make_request(endpoint, params)

        if response and response.status_code == 200:
            airlines = response.json()
            print(f'Found {len(airlines["airlines"])} airlines on page {page}.')
            for airline in airlines['airlines']:
                if "iata" in airline:
                    print(f"Airline: {airline['publicName']}, IATA: {airline['iata']}")
            return airlines
        else:
            print(f"Failed to fetch airlines: {response.status_code if response else 'No response'}")
            return None

    def get_airline(self, airline_id):
        """Fetch specific details about an airline."""
        endpoint = f"airlines/{airline_id}"
        response = self._make_request(endpoint)

        if response and response.status_code == 200:
            airline_details = response.json()
            print(f"Details for airline {airline_id}:")
            print(f"Public Name: {airline_details['publicName']}")
            return airline_details
        else:
            print(f"Failed to fetch airline details: {response.status_code if response else 'No response'}")
            return None

    def get_aircraft_types(self, page=0, sort_by="longDescription"):
        """Fetch a list of aircraft types."""
        params = {
            'page': page,
            'sort': f"+{sort_by}"
        }
        endpoint = 'aircrafttypes'
        response = self._make_request(endpoint, params)

        if response and response.status_code == 200:
            aircraft_types = response.json()
            print(f'Found {len(aircraft_types["aircraftTypes"])} aircraft types on page {page}.')
            for aircraft in aircraft_types['aircraftTypes']:
                if 'iataMain' in aircraft:
                    print(f"Aircraft Type: {aircraft['longDescription']}, IATA Main: {aircraft['iataMain']}")
            return aircraft_types
        else:
            print(f"Failed to fetch aircraft types: {response.status_code if response else 'No response'}")
            return None

    def get_flight_ids(self, page=0):
        """Fetch a list of flight IDs."""
        params = {
            'page': page
        }
        endpoint = 'flightids'
        response = self._make_request(endpoint, params)

        if response and response.status_code == 200:
            flight_ids = response.json()
            print(f'Found {len(flight_ids["flightIds"])} flight IDs on page {page}.')
            for flight_id in flight_ids['flightIds']:
                print(f"Flight ID: {flight_id}")
            return flight_ids
        else:
            print(f"Failed to fetch flight IDs: {response.status_code if response else 'No response'}")
            return None
