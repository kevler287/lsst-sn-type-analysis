from pydantic import BaseModel
from typing import List
from models.source import DiaSource

class SuperNovaDiaObject(BaseModel):
    diaObjectId: int
    sources: List[DiaSource]

    def get_sorted_sources(self):
        return sorted(self.sources, key=lambda source: source.midpointMjdTai)

    @classmethod
    def from_dict(cls, data):
        sources: List[DiaSource] = []

        for source_dict in data['diaSourcesList']:
            source = DiaSource(
                isForced=False,
                **source_dict
            )
            sources.append(source)

        for source_dict in data['diaForcedSourcesList']:
            source = DiaSource(
                diaSourceId=source_dict['diaForcedSourceId'],
                isForced=True,
                **source_dict
            )
            sources.append(source)

        return cls(
            diaObjectId=data['diaObjectId'],
            sources=sources
        )
