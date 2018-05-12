from googleplaces import GooglePlaces as Gp
from googleplaces import lang, ranking, _fetch_remote_json, _validate_response, GooglePlacesSearchResult


class GooglePlaces(Gp):
    def nearby_search(self, language=lang.ENGLISH, keyword=None, location=None,
               lat_lng=None, name=None, radius=3200, rankby=ranking.PROMINENCE,
               sensor=False, type=None, types=[], pagetoken=None):
        """Perform a nearby search using the Google Places API.

        One of either location, lat_lng or pagetoken are required, the rest of
        the keyword arguments are optional.

        keyword arguments:
        keyword  -- A term to be matched against all available fields, including
                    but not limited to name, type, and address (default None)
        location -- A human readable location, e.g 'London, England'
                    (default None)
        language -- The language code, indicating in which language the
                    results should be returned, if possible. (default lang.ENGLISH)
        lat_lng  -- A dict containing the following keys: lat, lng
                    (default None)
        name     -- A term to be matched against the names of the Places.
                    Results will be restricted to those containing the passed
                    name value. (default None)
        radius   -- The radius (in meters) around the location/lat_lng to
                    restrict the search to. The maximum is 50000 meters.
                    (default 3200)
        rankby   -- Specifies the order in which results are listed :
                    ranking.PROMINENCE (default) or ranking.DISTANCE
                    (imply no radius argument).
        sensor   -- Indicates whether or not the Place request came from a
                    device using a location sensor (default False).
        type     -- Optional type param used to indicate place category.
        types    -- An optional list of types, restricting the results to
                    Places (default []). If there is only one item the request
                    will be send as type param.
        pagetoken-- Optional parameter to force the search result to return the next
                    20 results from a previously run search. Setting this parameter
                    will execute a search with the same parameters used previously.
                    (default None)
        """
        if location is None and lat_lng is None and pagetoken is None:
            raise ValueError('One of location, lat_lng or pagetoken must be passed in.')
        if rankby == 'distance':
            # As per API docs rankby == distance:
            #  One or more of keyword, name, or types is required.
            if keyword is None and types == [] and name is None:
                raise ValueError('When rankby = googleplaces.ranking.DISTANCE, ' +
                                 'name, keyword or types kwargs ' +
                                 'must be specified.')
        self._sensor = sensor
        if pagetoken is None:
            radius = (radius if radius <= GooglePlaces.MAXIMUM_SEARCH_RADIUS
                      else GooglePlaces.MAXIMUM_SEARCH_RADIUS)
            lat_lng_str = self._generate_lat_lng_string(lat_lng, location)
            self._request_params = {'location': lat_lng_str}
            if rankby == 'prominence':
                self._request_params['radius'] = radius
            else:
                self._request_params['rankby'] = rankby
            if type:
                self._request_params['type'] = type
            elif types:
                if len(types) == 1:
                    self._request_params['type'] = types[0]
                elif len(types) > 1:
                    self._request_params['types'] = '|'.join(types)
            if keyword is not None:
                self._request_params['keyword'] = keyword
            if name is not None:
                self._request_params['name'] = name
            if language is not None:
                self._request_params['language'] = language
            self._add_required_param_keys()
            url, places_response = _fetch_remote_json(
                GooglePlaces.NEARBY_SEARCH_API_URL, self._request_params)
            _validate_response(url, places_response)
            return GooglePlacesSearchResult(self, places_response)
        if pagetoken is not None:
            _request_params = {'pagetoken': pagetoken}
            _request_params['key'] = self.api_key
            url, places_response = _fetch_remote_json(
                GooglePlaces.NEARBY_SEARCH_API_URL, _request_params)
            _validate_response(url, places_response)
            return GooglePlacesSearchResult(self, places_response)