/*global L:false */

'use strict';

L.Control.AdresseSok = L.Control.extend({

    options: {
        zoom: 5
    },


    initialize: function (options) {
        L.setOptions(this, options);
    },

    onAdd: function (map) {
        this._map = map;
        this._initLayout();
        return this._container;
    },

    _showResult: function (adresse) {
        this._map.setView([adresse.nord, adresse.aust], this.options.zoom);
        this._results.innerHTML = '';
        if (this.options.callback) {
            this.options.callback(L.latLng(adresse.nord, adresse.aust), adresse);
        }
    },

    _gotResults: function (res) {
        res = JSON.parse(res);
        this._results.innerHTML = '';
        var lg = L.DomUtil.create('ul', 'list-group', this._results);
        if (!res.adresser) {
            this._results.innerHTML = 'Ingen treff';
        }
        _.each(res.adresser, function (adresse) {
            var link = L.DomUtil.create('a', 'list-group-item', lg);
            var value = adresse.kortadressenavn + ' ' + (adresse.husnr || '')  + ' ' + (adresse.bokstav || '');
            link.innerHTML = value;
            link.href = '#';
            L.DomEvent.on(link, 'click', function (e) {
                L.DomEvent.preventDefault(e);
                this._input.value = value;
                this._showResult(adresse);
            }, this);
        }, this);
    },

    _search: function () {
        var value = this._input.value;
        if (value !== '') {
            var url = 'http://crossorigin.me/http://ws.geonorge.no/AdresseWS/adresse/sok?sokestreng=' + encodeURIComponent(value) + '&side=0';
            $.get(url, this._gotResults.bind(this));
        } else {
            this._results.innerHTML = '';
        }
    },

    _initLayout: function () {
        var className = 'leaflet-control-sok';
        this._container = L.DomUtil.create('div', className);
        L.DomEvent.on(this._container, 'click', L.DomEvent.stopPropagation);
        L.DomEvent.on(this._container, 'mousedown', L.DomEvent.stopPropagation);

        var div = L.DomUtil.create('div', 'input-group mapsearch');
        this._input = L.DomUtil.create('input', 'form-control', div);
        this._input.placeholder = 'Adressesøk..';
        this._input.type = 'text';
        var span = L.DomUtil.create('span', 'input-group-btn', div);
        var button = L.DomUtil.create('button', 'btn btn-default', span);
        button.innerHTML = 'SØK';
        button.type = 'button';
        L.DomEvent.on(button, 'click', function () {
            this._search();
        }, this);

        this._container.appendChild(div);
        this._results = L.DomUtil.create('div', 'searchresults');
        this._container.appendChild(this._results);
    }

});

L.control.adresseSok = function (options) {
    return new L.Control.AdresseSok(options);
};