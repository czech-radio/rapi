from dataclasses import asdict, dataclass


@dataclass
class station_data:
    code: str
    id: str
    title: str
    stitle: str
    priority: int
    type: str

    def Print(self):
        print("hello")