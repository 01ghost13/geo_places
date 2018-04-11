var myMap;

// Дождёмся загрузки API и готовности DOM.
ymaps.ready(init);

function init () {
    // Создание экземпляра карты и его привязка к контейнеру с
    // заданным id ("map").
    myMap = new ymaps.Map('map', {
        // При инициализации карты обязательно нужно указать
        // её центр и коэффициент масштабирования.
        center: [48.707103, 44.516939], // Волгоград
        zoom: 12
        }),
        collection = new ymaps.GeoObjectCollection(null, { preset: 'islands#redIcon'});

     document.getElementById('findData').onclick = function () {
//        var coordinates = [[48.703987, 44.523502],
//                            [48.760937, 44.542988],
//                            [48.511863, 44.583832],
//                            [48.512745, 44.584537],
//                            [48.559014, 44.440722]];
//
//        var places = ["8 причал, Волгоградский речной порт",
//                      "Парковка",
//                      "Бистро",
//                      "Бистро",
//                      "Строймаг"];
//
//        for (var i = 0; i < places.length; i++)
//            collection.add(new ymaps.Placemark(coordinates[i], {balloonContentHeader: places[i]}));
        $.getJSON("insta_geo_new.json", function(json) {
            console.log(json.length)
            for(var i = 0; i < json.length; i++) {
                long_lat = [json[i]['latitude'], json[i]['longitude']]
                place = json[i]['place']
                collection.add(new ymaps.Placemark(long_lat, {balloonContentHeader: place}));
            }
        });

        myMap.geoObjects.add(collection);
    };
}