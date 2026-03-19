import os
from lasair_client import LasairClient
import dotenv

dotenv.load_dotenv()

token = os.environ.get('LASAIR_API_TOKEN')
client = LasairClient(token=token)
results = client.cone_search(ra=120, dec=1.5, radius=500.0)
print(results)