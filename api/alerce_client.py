import pyvo as vo
from models.dia_object import DiaObject
from models.dia_source import DiaSource
import pandas as pd
from alerce.core import Alerce
from typing import List

class AlerceClient:

    def __init__(self, url="https://tap.alerce.online/tap"):
        self.tap_srv = vo.dal.TAPService(url)
        self.py_client = Alerce()

    def fetch_detections(self, object_id: int) -> List[DiaSource]:
        dia_sources: List[DiaSource] = []
        
        detections = self.py_client.query_detections(oid=object_id, survey="lsst", format="json")
        for det in detections:
            dia_source = DiaSource.from_alerce(det, is_forced=False)
            dia_sources.append(dia_source)

        forced_photometry = self.py_client.query_forced_photometry(oid=object_id, survey="lsst", format="json")
        for fp in forced_photometry:
            dia_source = DiaSource.from_alerce(fp, is_forced=True)
            dia_sources.append(dia_source)

        return dia_sources

    
    def fetch_sn_object_ids(self) -> List[DiaObject]:
        query = '''
        SELECT 
            prob.oid, prob.class_id, prob.probability
        FROM 
            alerce_tap.probability AS prob
        WHERE
            (prob.class_id = 0 OR prob.class_id = 5)
            AND prob.probability > 0.5
        '''
        results: pd.DataFrame = self.tap_srv.search(query).to_table().to_pandas()
        dia_objects: List[DiaObject] = []
        for _, row in results.iterrows():
            dia_obj = DiaObject(
                diaObjectId=row['oid'],
                class_id=row['class_id'],
                probability=row['probability'],
            )
            dia_objects.append(dia_obj)
        return dia_objects
