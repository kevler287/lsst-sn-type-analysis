import requests

class LasairClient:
    """
    A custom API client for the Rubin Observatory / Lasair Alert Broker.
    
    This client replaces the official 'lasair' Python package (v0.1.2) due to 
    authentication issues caused by the library's forced use of HTTP POST 
    requests. This custom implementation uses HTTP GET requests to ensure 
    compatibility with the Lasair REST API endpoints.

    Attributes:
        token (str): The Lasair API access token.
        base_url (str): The base URL for the Lasair API (default: https://lasair.lsst.ac.uk/api).
    """

    def __init__(self, token, base_url="https://lasair.lsst.ac.uk/api"):
        self.token = token
        self.base_url = base_url.rstrip('/')
        self.headers = {'Authorization': f'Token {self.token}'}

    def cone_search(self, ra, dec, radius=100, request_type='all'):
        """
        Perform a cone search to find astronomical transients near specific coordinates.

        Args:
            ra (float): Right Ascension in decimal degrees (0 to 360).
            dec (float): Declination in decimal degrees (-90 to +90).
            radius (float): Search radius in arcseconds (max 1000).
            request_type (str): Type of data to return ('all' or 'count').

        Returns:
            list: A list of dictionaries containing alert data or object IDs.
        
        Raises:
            Exception: If the server returns a non-200 status code.
        """
        endpoint = f"{self.base_url}/cone/"
        params = {
            'ra': ra,
            'dec': dec,
            'radius': radius,
            'requestType': request_type
        }
        
        response = requests.get(endpoint, params=params, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception("Unauthorized: Check if your token is valid and active.")
        else:
            raise Exception(f"API Error {response.status_code}: {response.text}")
