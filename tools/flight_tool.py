import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY=os.getenv("AVIATIONSTACK_API_KEY")


def search_flights(query):

    try:

        logger.info(
            f"Flight Search Started | Query: {query}"
        )

        url = "http://api.aviationstack.com/v1/flights"

        params = {
            "access_key": API_KEY,
            "limit": 5
        }

        response = requests.get(url, params=params)

        logger.info(
            f"API Status Code: {response.status_code}"
        )

        data = response.json()

        flights = []

        if "data" in data:

            for flight in data["data"][:5]:

                airline = flight.get("airline", {}).get("name", "Unknown")

                departure = flight.get(
                    "departure", {}
                ).get("airport", "Unknown")

                arrival = flight.get(
                    "arrival", {}
                ).get("airport", "Unknown")

                status = flight.get("flight_status", "Unknown")

                flights.append(
                    f"""
Airline: {airline}
Departure: {departure}
Arrival: {arrival}
Status: {status}
"""
                )

        logger.info(
            f"Flights Found: {len(flights)}"
        )

        return "\n".join(flights)

    except Exception as e:

        logger.error(
            f"Flight API Error: {e}"
        )

        return "Flight API Failed"