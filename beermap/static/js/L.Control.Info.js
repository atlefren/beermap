/*global L:false */

'use strict';

L.Control.Info = L.Control.extend({

    initialize: function (options) {
        L.setOptions(this, options);
    },

    _initLayout: function () {
        var className = 'leaflet-control-info';
        this._container = L.DomUtil.create('div', className);

        var closeBtn = L.DomUtil.create('button', 'close', this._container);
        L.DomEvent.on(closeBtn, 'click', function () {
            this.hide();
        }, this);
        var span = L.DomUtil.create('span', '', closeBtn);
        span.innerHTML = '&times;';
        this._content = L.DomUtil.create('div', '', this._container);
        this.hide();
    },

    hide: function () {
        this._container.style.display = 'none';
        this._content.innerHTML = '';
    },

    setContent: function (content) {
        this._container.style.display = 'block';
        this._content.innerHTML = content;
    },

    onAdd: function (map) {
        this._map = map;
        this._initLayout();
        return this._container;
    }
});