import os

import lasair
from lasair_client import LasairClient
import dotenv

dotenv.load_dotenv()

token = os.environ.get('LASAIR_API_TOKEN')
client = LasairClient(token=token)
results = client.query(selected='sherlock_classifications.diaObjectId', tables='sherlock_classifications', conditions='classification LIKE "SN"')
print(results)