from api.mongo_client import LSSTMongoClient
from models.tns_object import TNSObject
from typing import Tuple
from models.ztf_object import ZTFObject
from scripts.feature_analysis import lc_timeseries_variance

M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst-sn-type-analysis")
tuples: Tuple[TNSObject, ZTFObject] = M.get_tns_ztf_crossmatches()
ztf_objects = [t[1] for t in tuples]

lc_timeseries_variance.plot_lc_timeseries_length(ztf_objects=ztf_objects, fids=[1,2,3])

M.close()
