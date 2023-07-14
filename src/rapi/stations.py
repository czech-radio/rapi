import requests, json
from .logger import log_stdout as logo
from .logger import log_stderr as loge

class stations:
    def __init__(self, pars):
        self.params = pars
        self.mock_url="https://mockservice.croapp.cz/mock"
        self.apidoc_url="https://rapidoc.croapp.cz"
        self.api_url="https://rapidev.croapp.cz"
        logo.info("stations class initialized")
    def params_debug(self):
        print(json.dumps(self.params.__dict__))
    def GetStations(self):
        url=self.api_url+'/stations'
        logo.info("requesitng url: {url}")
        r = requests.get(url)
        print(r.text)
