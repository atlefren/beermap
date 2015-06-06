/*global window:false, L:false*/
(function () {
    'use strict';

    function tabs(div, layers, map) {
        _.first(layers).selected = true;

        var onMap;

        var els = _.map(layers, function (layer) {
            var tab = $('<li role="presentation"><a href="#">' + layer.name + '</a></li>');
            if (layer.selected) {
                tab.addClass('active');
                onMap = layer.layer;
                map.addLayer(onMap);
            }
            tab.on('click', function (e) {
                e.preventDefault();
                if (!layer.selected) {
                    map.removeLayer(onMap);
                    onMap = layer.layer;
                    map.addLayer(onMap);
                    _.each(layers, function (l) {
                        l.selected = false;
                    });
                    div.find('li').removeClass('active');
                    tab.addClass('active');
                    layer.selected = true;
                }
            });
            return tab;
        });
        div.append(els);
    }

    window.renderHexmap = function (hexes) {
        function getHexLayer(geoJson) {
            var max = _.max(geoJson.features, function (feature) {
                return feature.properties.count;
            }).properties.count;

            var colors = [
                '#F7FBFF',
                '#C7DCEF',
                '#72B2D7',
                '#2878B8',
                '#08306B'
            ];

            function getColorFunc(max) {
                var step = max / 4;
                var steps = _.map(_.range(0, 4), function (i) {
                    return i * step;
                });
                return function (count) {
                    if (count > max) {
                        return _.last(colors);
                    }
                    var a = _.find(steps, function (step) {
                        return count <= step;
                    });
                    return colors[steps.indexOf(a)];
                };
            }

            var getColor = getColorFunc(max);

            return L.geoJson(geoJson, {
                style: function (feature) {
                    return {
                        weight: 1,
                        clickable: false,
                        color: '#000',
                        fillColor: getColor(feature.properties.count),
                        fillOpacity: 0.5
                    };
                }
            });
        }

        var layers = [
            {name: 'Puber', layer: getHexLayer(hexes.pubs)},
            {name: 'Pol', layer: getHexLayer(hexes.pol)},
            {name: 'Bryggerier', layer: getHexLayer(hexes.breweries)}
        ];

        var map = L.map('map').setView([65.5, 17.0], 4);

        tabs($('#layertabs'), layers, map);

        L.tileLayer.kartverket('norges_grunnkart').addTo(map);
    };
}());