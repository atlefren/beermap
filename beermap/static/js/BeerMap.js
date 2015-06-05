/*global L:false */
function BeerMap(layers, templates, mappings, defaults) {

    'use strict';

    var menuElemTemplate = _.template($('#menu_element_template').html());

    var overlays;

    var map;

    function _toggleMenu(selectedItem) {
        $('.nav-sidebar-sub').children().each(function () {
            var el = $(this);
            var id = el.attr('id').replace('map_', '');
            if (id === selectedItem.id) {
                el.addClass('active');
            } else {
                el.removeClass('active');
            }
        });
    }

    function _showMap(item) {
        _toggleMenu(item);

        if (overlays) {
            map.removeLayer(overlays);
            overlays.off();
        }

        var template = templates[item.id];
        var defaultProps = defaults[item.id] || {};
        var mapping = mappings[item.id] || function (a) {return a; };
        var data = L.geoJson(
            item.data,
            {
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(template(_.extend(
                        {},
                        defaultProps,
                        mapping(feature.properties)
                    )));
                }
            }
        );
        overlays = new L.MarkerClusterGroup()
            .addLayers(data.getLayers())
            .addTo(map);
        overlays.on('click', function (a) {
            a.layer.openPopup();
        });
    }

    function _renderMenuItem(layer) {
        var li =  $(menuElemTemplate(layer));
        li.on('click', function () {
            _showMap(layer);
        });
        return li;
    }

    function setupMap(pos, zoom) {
        zoom = zoom || 4;

        map = L.map('map').setView(pos, zoom);
        L.tileLayer.kartverket('norges_grunnkart').addTo(map);
        L.control.adresseSok().addTo(map);

        var ul = $('<ul class="nav nav-sidebar nav-sidebar-sub"></ul>');

        ul.append(_.map(layers, _renderMenuItem));
        $('#link_map').append(ul);

        _showMap(layers[0]);
    }

    return {
        setupMap: setupMap
    };
}