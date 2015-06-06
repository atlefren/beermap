/*global d3:false */

function renderChart(data, element) {
    'use strict';

    var key = 'pop_by_num';

    var width = 420,
        barHeight = 20;

    var x = d3.scale.linear()
        .domain([0, d3.max(_.pluck(data, key))])
        .range([0, width - 40]);

    var chart = d3.select('.' + element)
        .attr('width', width)
        .attr('height', barHeight * data.length);

    var bar = chart.selectAll('g')
        .data(data)
        .enter().append('g')
        .attr('transform', function (d, i) { return 'translate(0,' + i * barHeight + ')'; });

    var g = bar.append('g')
        .attr('transform', 'translate(40, 0)');

    g.append('rect')
        .attr('width', function (d) { return x(d[key]); })
        .attr('height', barHeight - 1);

    g.append('text')
        .attr('class', 'number')
        .attr('x', function (d) { return x(d[key]) - 3; })
        .attr('y', barHeight / 2)
        .attr('dy', '.35em')
        .text(function (d) { return d3.round(d[key], 0); });

    bar.append('text')
        .attr('x', 2)
        .attr('class', 'text')
        .attr('y', barHeight / 2)
        .attr('dy', '.35em')
        .text(function (d) { return d.navn; });
}