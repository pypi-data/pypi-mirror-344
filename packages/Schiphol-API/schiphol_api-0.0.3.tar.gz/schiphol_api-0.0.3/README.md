# Schiphol-API

A simple and lightweight Python client for interacting with the [Schiphol Airport Public Flights API](https://developer.schiphol.nl/).

This package allows you to easily fetch flight, destination, airline, and aircraft type information from Schiphol Airport.

---

## 📦 Installation

Install the package via pip:

```bash
pip install schiphol-api
```

---

## 🚀 Quick Start

```python
from schiphol_api import SchipholAPI

# Initialize the API client with your app_id and app_key
api = SchipholAPI(app_id="your_app_id", app_key="your_app_key")

# Fetch a list of flights
flights = api.get_flights(page=0)

# Fetch details for a specific flight
flight_details = api.get_flight(flight_id="your_flight_id")

# Fetch a list of destinations
destinations = api.get_destinations()

# Fetch details for a specific destination
destination_details = api.get_destination(destination_id="your_destination_id")

# Fetch a list of airlines
airlines = api.get_airlines()

# Fetch details for a specific airline
airline_details = api.get_airline(airline_id="your_airline_id")

# Fetch a list of aircraft types
aircraft_types = api.get_aircraft_types()

# Fetch a list of flight IDs
flight_ids = api.get_flight_ids()
```

---

## 🔧 Available Methods

| Method | Description |
|:-------|:------------|
| `get_flights(page=0, include_delays=False, sort_by="scheduleTime")` | Fetch a paginated list of flights |
| `get_flight(flight_id)` | Fetch details about a specific flight |
| `get_destinations(page=0, sort_by="publicName.english")` | Fetch a paginated list of destinations |
| `get_destination(destination_id)` | Fetch details about a specific destination |
| `get_airlines(page=0, sort_by="publicName")` | Fetch a paginated list of airlines |
| `get_airline(airline_id)` | Fetch details about a specific airline |
| `get_aircraft_types(page=0, sort_by="longDescription")` | Fetch a paginated list of aircraft types |
| `get_flight_ids(page=0)` | Fetch a paginated list of flight IDs |

---

## 🔑 Authentication

You need to register for an account at the [Schiphol Developer Center](https://developer.schiphol.nl/) to obtain your:

- `app_id`
- `app_key`

Use these credentials when initializing the `SchipholAPI` client.

---

## ✨ Future Improvements

- Retry mechanism for API failures
- Rate limit handling
- Async support

---

Made with ❤️ for developers using Schiphol's open data

---