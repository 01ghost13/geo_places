import json as j
import re
from result_data import ResultData


class Generator:
    def __init__(self, name, kind):
        self.source_file = name
        self.source_json = {}
        self.target_file = re.sub(r'(.*?)(?=\..*)', '\1_new', name)
        self.target = ResultData()
        self.kind = kind

    def __query__(self, kind, longitude, latitude, tags, hashtags):
        pass

    def process(self):
        pass

    def __open__(self):
        pass

    def __save__(self):
        pass

