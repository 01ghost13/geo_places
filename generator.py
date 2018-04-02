import json as j
import re
from result_data import ResultData
from googleplaces import GooglePlaces, types, lang


API_KEY = 'AIzaSyCv3hNhb0HDg8KpxLP0JNqxAPUfUpH-0qU'

hashTypes = {
                "еда": {"food", "cafe", "bar", "restaurant"},
                "развлечения": {"amusement_park", "museum", "park", "zoo"},
                "мода-красота": {"city_hall"},
                "ночная жизнь": {"night_club"},
                "спорт": {"gym", "stadium"},
                "отношения": {"park", "zoo"},
                "достопримечательности": {"museum"},
                "работа": {"establishment "},
                "учеба": {"school", "university"}
            }


class Generator:
    def __init__(self, name, kind):
        self.source_file = name
        self.source_json = {}
        self.target_file = re.sub(r'(.*?)(?=\..*)', '\1_new', name)
        self.target = None
        self.kind = kind

    def __query__(self, longitude, latitude, tag, hashtags):

        nameOfObject = ''

        #object PLACES NEAR
        google = GooglePlaces(API_KEY)

        #request
        query_result = google.nearby_search(
            lat_lng={'lat': latitude, 'lng': longitude},
            radius=150,
            language=lang.RUSSIAN
        )

        #request process
        for item in query_result.places:
            #сравнение types с тегами
            if checkTypesInTagsHashTags(item, hashTypes[tag], True):
                nameOfObject = item.places.name
            #сравнение types с хештегами
            elif checkTypesInTagsHashTags(item, hashtags, True):
                nameOfObject = item.places.name
            # сравнение types с хештегами
            elif checkTypesInTagsHashTags(item, hashtags, False):
                nameOfObject = item.places.name

        if nameOfObject == '':
            nameOfObject = query_result.places[0].name

        return nameOfObject

    def process(self, count):
        self.__open__()
        self.target = ResultData()
        for i in range(min(len(self.source_json), count)):
            record = self.source_json[i]
            record['tag'] = self.__converter__(record['tag'])
            record['hashtag'] = j.loads(record['hashtag'], 'unicode-escape')
            place = self.__query__(record['longitude'], record['latitude'], record['tag'], record['hashtag'])
            record['place'] = place
            self.target.add_record(record)
        self.__save__()

    def __open__(self):
        file = open(self.source_file)
        self.source_json = j.load(file)
        self.source_json = self.source_json[2]['data']

    def __save__(self):
        file = open(self.target_file)
        file.write(j.dumps(self.target.data))
        file.close()

    @staticmethod
    def __converter__(s):
        return s.encode().decode('unicode-escape')

#################################################################################
#сравнение types/name с тегами или хештегами записи
def checkTypesInTagsHashTags(itemForChaeck, arrayForCheck, flagTypeCheck):
    for itemArray in arrayForCheck:
        if flagTypeCheck:
            for type in itemForChaeck.places.types:
                if type == itemArray:
                    return True
        else:
            for name in itemForChaeck.places.name:
                if name == itemArray:
                    return True

    return False
