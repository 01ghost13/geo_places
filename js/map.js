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

    document.getElementById('findData').onclick = function () {
        collection = new ymaps.GeoObjectCollection(null, { preset: 'islands#redIcon'});
        var gender = $('#gender_select')[0].value;
        var min_age = $('#min_age')[0].value;
        var max_age = $('#max_age')[0].value;
        var tag_select = $('#tag_select')[0].value;
        console.log(gender, min_age, max_age, tag_select);

        $.getJSON("insta_geo_new.json", function(json) {
            console.log(json.length)
            for(var i = 0; i < json.length; i++) {
                var rec = json[i];
                var long_lat = [rec['latitude'], rec['longitude']];
                var place = rec['place'];
                if(rec['sex'] == gender && rec['age'] >= min_age && rec['age'] <= max_age && rec['tag'] == tag_select) {
                    collection.add(new ymaps.Placemark(long_lat, {balloonContentHeader: place}));
                }
            }
    });

        myMap.geoObjects.add(collection);
    };
}