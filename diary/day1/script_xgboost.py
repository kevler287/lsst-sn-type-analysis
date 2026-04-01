import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
from api.mongo_client import LSSTMongoClient
from models.tns_object import TNSObject
from typing import Tuple
import pandas as pd
from models.ztf_object import ZTFObject
from diary.day1.vector_v1 import ZTFVector
from enums.sn_type import SNType, SNLabel

M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst-sn-type-analysis")
tuples: Tuple[TNSObject, ZTFObject] = M.get_tns_ztf_crossmatches()
ztf_objects = [t[1] for t in tuples]

print(f"Number of TNS x ZTF crossmatches: {len(ztf_objects)}")

vectors = []
for tns_obj, ztf_obj in tuples:
    target = SNType.to_upper_group(s=tns_obj.type)
    if target is None:
        continue
    vector = ZTFVector.from_ztf_object(ztf_obj, sn_type=target)
    vectors.append(vector)

print(f"Number of feature vectors: {len(vectors)}")

df = pd.DataFrame([v.model_dump() for v in vectors])
X = df.drop(columns=["oid", "sn_type"])
y = df["sn_type"]

print(y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

class_counts = pd.Series(y).value_counts().sort_index()
class_weights = len(y) / (len(class_counts) * class_counts)
sample_weights = pd.Series(y).map(class_weights.to_dict()).values
sample_weights_train = sample_weights[:len(y_train)]

model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    random_state=42,
    eval_metric="mlogloss",
)

model.fit(
    X_train, y_train,
    sample_weight=sample_weights_train,
    eval_set=[(X_test, y_test)],
    verbose=50,
)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=[sn.name for sn in SNLabel]))

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[sn.name for sn in SNLabel])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()