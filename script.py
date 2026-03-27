from api.mongo_client import LSSTMongoClient
from models.tns_object import TNSObject
from typing import Tuple
from models.ztf_object import ZTFObject
from scripts.feature_analysis import lc_timeseries_variance

M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst-sn-type-analysis")
tuples: Tuple[TNSObject, ZTFObject] = M.get_tns_ztf_crossmatches()
ztf_objects = [t[1] for t in tuples]

frame = lc_timeseries_variance.analyze_lc_timeseries(ztf_objects=ztf_objects)
# lc_timeseries_variance.print_statistics(lc_frame=frame)
# lc_timeseries_variance.print_availability(lc_frame=frame)
lc_timeseries_variance.plot_lc_timeseries_density(lc_frame=frame)
lc_timeseries_variance.plot_lc_timeseries_span(lc_frame=frame)

M.close()
