from collections import Counter

class ResultData:

    def __init__(self,  open_file=None,):
        self.data = []
        if open_file:
            self.file = open_file

    def add_record(self, record_hash):
        self.data.append(record_hash)

    def sort_by_place(self):
        places = map((lambda x: x['place']), self.data)
        return dict(Counter(places))
