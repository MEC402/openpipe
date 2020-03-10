// const margin = {top: 20, right: 50, bottom: 50, left: 50};
// const cw1 = document.getElementById("ln").offsetWidth;
// const ch1 = document.getElementById("ln").offsetHeight;
// const width1 = cw1 - margin.left - margin.right;
// const height1 = ch1 - margin.top - margin.bottom;


var widthGlobe = document.getElementById("ln").offsetWidth,
    height = document.getElementById("ln").offsetHeight,
    sens = 0.25;

widthGlobe = 960;
height = 500;


const center = [widthGlobe/2, height/2];
var locations;

const svg1 = d3.select(".glob")
    .append("svg")
    .attr("width", widthGlobe)
    .attr("height", height);

var projection1 = d3.geoOrthographic()
    .scale(245)
    .rotate([0, 0])
    .translate([widthGlobe / 2, height / 3])
    .clipAngle(90);

var pathGenerator1 = d3.geoPath().projection(projection1);


const projection = d3.geoNaturalEarth1();


var g1 = svg1.append('g');


//**************************************************************************************************************************************************************
//****************************************************************  Render Functions  **************************************************************************
//**************************************************************************************************************************************************************

const render = countries => {

    console.log(countries)
    //drawLegend();


    g1.append("path")
        .datum({type: "Sphere"})
        .attr("class", "water")
        .attr("d", pathGenerator1);

    g1.selectAll('path').data(countries.features)
        .enter().append('path')
        .attr('class', 'country')
        .attr('d', pathGenerator1)
        .attr('fill','gray')
        .append('title')
        .text("hi");

    svg1.call(d3.drag()
        .subject(function() { var r = projection1.rotate();
            return {x: r[0] / sens, y: -r[1] / sens}; })
        .on("drag", function() {
            var rotate = projection1.rotate();
            projection1.rotate([d3.event.x * sens, -d3.event.y * sens, rotate[2]]);
            g1.selectAll("water").attr("d", pathGenerator1);
            g1.selectAll(".country").attr("d", pathGenerator1);
            g1.selectAll(".graticule").attr("d", pathGenerator1);
            drawMarkers();
        }));

    var zoom1=d3.zoom().on('zoom', () => {
        g1.attr('transform', d3.event.transform);});

    svg1.call(zoom1);

    drawGraticule();
    drawMarkers();


    d3.select('.button').on('click', (d,i) => {
        mounth=d3.select('input[name="month"]:checked').node().value;
        svg2.selectAll('.title')
            .text(monthNames[mounth]);
        reColorGlobe(countries);
        reColorCountries(countries);
    });




    d3.select('.reset-zoom-button').on('click', () => {
        console.log("hi");
        g1.transition().call(zoom1.transform, d3.zoomIdentity);
    });

    // d3.select('.start').on('click', () => {
    //     document.getElementById("s").disabled = true;
    //     document.getElementById("e").disabled = false;
    //
    // });



};

//**************************************************************************************************************************************************************
//***************************************************************  Other Functions  ****************************************************************************
//**************************************************************************************************************************************************************

function reColorGlobe(countries) {
    svg1.selectAll('.country')
        .attr('fill',d=>colorScale(d.properties[mounth]))
        .select('title')
        .text(d => d.properties.name+" : "+d.properties[mounth]+" C");
}

function reColorCountries(countries) {
    g.selectAll('.country')
        .attr('fill',d=>colorScale(d.properties[mounth]))
        .select('title')
        .text(d => d.properties.name+" : "+d.properties[mounth]+" C");
}

function drawGraticule() {
    const graticule = d3.geoGraticule()
        .step([10, 10]);

    g1.append("path")
        .datum(graticule)
        .attr("class", "graticule")
        .attr("d", pathGenerator1)
        .style("fill", "none")
        .style("stroke", "#ccc");
}

function drawMarkers() {
    const markers = g1.selectAll('circle')
        .data(locations);
    markers
        .enter()
        .append('circle')
        .merge(markers)
        .attr('cx', d => projection([d.openpipe_canonical_longitude[0], d.openpipe_canonical_latitude[0]])[0])
        .attr('cy', d => projection([d.openpipe_canonical_longitude[0], d.openpipe_canonical_latitude[0]])[1])
        .attr('fill', d => {
            const coordinate = [d.openpipe_canonical_longitude[0], d.openpipe_canonical_latitude[0]];
            gdistance = d3.geoDistance(coordinate, projection.invert(center));
            console.log(projection.invert(center))
            console.log(gdistance)
            return gdistance > 1.57 ? 'none' : 'red';
        })
        .attr('r', 5).on('click',(d,i)=>{
        console.log(d)
    });

    g1.each(function () {
        this.parentNode.appendChild(this);
    });

}

//**************************************************************************************************************************************************************
//****************************************************************  Main Functions  ****************************************************************************
//**************************************************************************************************************************************************************

    d3.queue()
        .defer(d3.json, 'https://unpkg.com/world-atlas@1.1.4/world/50m.json')
        .defer(d3.json, 'location.json')
        .await((error, worldData, locationData) => {
            const countries = topojson.feature(worldData, worldData.objects.countries);

            locations = locationData.data;
            render(countries)
        });





