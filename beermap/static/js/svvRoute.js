/*global proj4:false, esriConverter:false */
var SVVRoute = function (BASE_URL) {
    'use strict';

    proj4.defs([[
        'EPSG:32633',
        '+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs'
    ]]);

    function _transform(coordinates) {
        if (typeof proj4 === 'undefined') {
            throw new Error('Proj4js not found!');
        }
        return proj4('EPSG:32633', 'EPSG:4326', coordinates);
    }

    function _toLatLng(fc) {
        var features = _.map(fc.features, function (feature) {
            feature.geometry.coordinates = _.map(feature.geometry.coordinates, _transform);
            return feature;
        });
        fc.features = features;
        return fc;
    }

    var _createQueryParameterString = function (params) {
        return _.map(params, function (value, key) {
            return encodeURIComponent(key) + '=' + encodeURIComponent(value);
        }).join('&');
    };

    function _getStops(from, to) {
        var coord1 =  proj4('EPSG:4326', 'EPSG:32633', [from.lng, from.lat]);
        var coord2 =  proj4('EPSG:4326', 'EPSG:32633', [to.lng, to.lat]);
        return coord1.join(',') + ';' + coord2.join(',');
    }

    function getRoute(from, to, callback) {

        var params = {
            stops: _getStops(from, to),
            returnDirections: true,
            returnGeometry: true,
            format: 'json'
        };

        var jsonconverter = esriConverter();
        $.ajax({
            url: BASE_URL + '?' + _createQueryParameterString(params),
            type: 'GET',
            success: function (res) {
                callback(_toLatLng(jsonconverter.toGeoJson(res.routes)));
            }
        });
    }

    return {
        getRoute: getRoute
    };
};