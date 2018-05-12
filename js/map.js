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
        zoom: 12,
        controls: ['zoomControl']
      }),
      objectManager = new ymaps.ObjectManager();
      myMap.geoObjects.add(objectManager);

    document.getElementById('findData').onclick = function () {
        collection = new ymaps.GeoObjectCollection(null, { preset: 'islands#redIcon'});
        var gender = $('#gender_select')[0].value;
        var min_age = $('#min_age')[0].value;
        var max_age = $('#max_age')[0].value;
        var tag_select = $('#tag_select')[0].value;

        $.getJSON("js/insta_geo_new.json", function(json) {
          var new_json = [];
          var found_obj = [];
          var max = 0;

            for(var i = 0; i < json.length; i++) {
                var rec = json[i];

                if(rec['sex'] == gender && rec['age'] >= min_age && rec['age'] <= max_age && rec['tag'] == tag_select) {
                    // проверка вхождения данной точки в лист найденных точек
                    record = {
                              'latitude': rec['latitude'],
                              'longitude': rec['longitude'],
                              'place': rec['place'],
                              'count': 1,
                              'rating' : 1
                    }
                    // определение уникальных точек
                    if (found_obj.length == 0)
                    {
                      found_obj[0] = record;
                    }
                    else {
                      var flag = false;
                      for (var j = 0; j < found_obj.length; j++){
                        if (record['latitude'] == found_obj[j]['latitude'] && record['longitude'] == found_obj[j]['longitude'])
                        {
                          found_obj[j]['count'] = found_obj[j]['count'] + 1;
                          flag = true;
                          if (found_obj[j]['count'] > max){
                            max = found_obj[j]['count'];
                          }
                          break;
                        }
                      }
                      if (flag == false){
                        found_obj[found_obj.length] = record;
                      }
                    }
                }

            }

            for (var i = 0; i < found_obj.length; i++)
            {
              //определение рейтинга по 5тибалльной шкале
              found_obj[i]['rating'] = Math.ceil(5*found_obj[i]['count']/max)
              //определение цвета метки
              var color = "#FF0000"; // для рейтинга 1 по умолчанию цвет - красный
              if (found_obj[i]['rating'] == 2)
              {
                color = "#FFA500";
              }
              else if (found_obj[i]['rating'] == 3)
              {
                color = "#FFFF00";
              }
              else if (found_obj[i]['rating'] == 4)
              {
                color = "#008000";
              }
              else if (found_obj[i]['rating'] == 5)
              {
                color = "#0000FF";
              }
              //сохранение объекта в коллекцию
              new_json[i] = {"type": "Feature", "id": i, "geometry": {"type": "Point", "coordinates": [found_obj[i]['latitude'],found_obj[i]['longitude']]}, "properties": {"balloonContent": found_obj[i]['place'], "clusterCaption": "Метка с iconContent", "hintContent": "Рейтинг места, " + found_obj[i]['rating'], "iconContent": found_obj[i]['rating']}, "options": {"iconColor": color, "preset": "islands#blueCircleIcon"}};
            }

            objectManager.add(new_json);
        });
    };
}
