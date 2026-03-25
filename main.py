from api.mongo_client import LSSTMongoClient
from plotting import object_viewer

M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst")
sn_objects = M.get_all()

max_days = 0
max_sn_obj = None
for sn_obj in sn_objects:
    sources = [s for s in sn_obj.sources if not s.isForced]
    forced_sources = [s for s in sn_obj.sources if s.isForced]

    mjd_days = {int(s.midpointMjdTai) for s in forced_sources}
    if len(mjd_days) > max_days:
        max_days = len(mjd_days)
        max_sn_obj = sn_obj

print(f"Object with the most days of observations: {max_sn_obj.diaObjectId} with {max_days} days.")
object_viewer.plot_light_curve(max_sn_obj)

