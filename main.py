import os
from models.sn_object import SuperNovaDiaObject
from api.lasair_client import LasairClient
import dotenv

dotenv.load_dotenv()

token = os.environ.get('LASAIR_API_TOKEN')
client = LasairClient(token=token)
# sn_ids = client.query(selected='sherlock_classifications.diaObjectId', tables='sherlock_classifications', conditions='classification LIKE "SN"')
result = client.get_object(object_id="170019695992242795", lasair_added=True)
print("no timeout")
sn_obj = SuperNovaDiaObject.from_dict(result)
# plotter.plot_object(sn_obj)
