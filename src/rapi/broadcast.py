import requests, json
import logging
logo=logging.getLogger("log_stdout")
loge=logging.getLogger("log_stderr")
from . import station

class broadcast:
    def __init__(self, pars):
        self.params = pars
        self.mock_url="https://mockservice.croapp.cz/mock"
        self.apidoc_url="https://rapidoc.croapp.cz"
        self.api_url="https://rapidev.croapp.cz"
        logo.info("broadcast class initialized")
        self.request_data=self.RequestData()
        self.fields=self.ParseFields()
    def params_debug(self):
        print(json.dumps(self.params.__dict__))
    def RequestData(self):
        url=self.api_url+'/stations'
        logo.info("requesitng url: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            loge.error("cannot get data from: {url}")
            return None
    def ParseFields(self):
        stations=[]
        data=self.request_data["data"]
        for k in data:
            attr=k["attributes"] 
            stdat=station.station_data(
                    id=k["id"],
                    title=attr["title"],
                    stitle=attr["shortTitle"],
                    priority=attr["priority"],
                    type=attr["stationType"],
                    )
            stations.append(stdat)
        return stations
    def GetStation(station_name: str):
        pass
