
// Copyright (c) 2016 CanalTP
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

import * as L from "leaflet";
import * as d3fetch from "d3-fetch";
import * as tinycolor from "tinycolor2";
import * as sprintf from "sprintf";
import 'jquery';
import 'jquery-ui/ui/widgets/slider';
import 'jquery-datetimepicker';
import 'jquery-toggles';
import 'leaflet-providers';


/** Map generation section**/
var map;
var heatMapLayerId;
var starting_point_marker;
var default_starting_location = [32.073443, 34.790410];
var starting_location;
var default_starting_zoom = 13;

//Creating the grey icon
var geryIcon = new L.Icon({
    iconUrl: 'assets/images/marker-icon-grey.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

//TODO: remove me
var dateCounter;
var nextDateCounter;
var time_passed;

function createMap() {
    var mapboxTiles =
        L.tileLayer.provider('Stamen.TonerLite');

    map = L.map('map', {renderer: new L.canvas()})
        .setView([32.07050190954199,34.8427963256836], default_starting_zoom)
        .addLayer(mapboxTiles);

    //Fixing the grey tiles partial issue
    $(window).on("resize", function () { $("#map").height($(window).height()); map.invalidateSize(); }).trigger("resize");

    // setting for default path of images used by leaflet - otherwise marker only appear after first click
    delete L.Icon.Default.prototype._getIconUrl;

    L.Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    });

    //Creating the default marker with location
    starting_point_marker = createNewMarker(starting_point_marker, default_starting_location, false);
    return map;
}

function createNewMarker(marker, latLng, isDragged) {
    //Remove old marker from the map
    if (starting_point_marker) {
        starting_point_marker.removeFrom(map);
    }
    if (isDragged) {
        marker = new L.marker(latLng, {
            draggable: true,
            icon: geryIcon
        });
    } else {
        marker = new L.marker(latLng, {
            draggable: true,
        });
    }
    marker.on('dragend', function(event){
        handleMarkerDrag(event.target.getLatLng());
    });
    starting_location= marker._latlng;
    marker.addTo(map);
    return marker;
}
function handleMarkerDrag(latLng) {
    starting_location = latLng;
    //remove former starting marker point
    if (starting_point_marker !== undefined) {
        map.removeLayer(starting_point_marker);
    }
    starting_point_marker = createNewMarker(starting_point_marker, starting_location, true);
    invalidateRunButton();
}

function invalidateRunButton() {
    runButton.text("Re-run");
}
function addHeatMapLayer(features) {
    var heatMapLayer = new L.featureGroup(features);
    heatMapLayerId = heatMapLayer.getLayerId(heatMapLayer);
    heatMapLayer.addTo(map);
}

function addHeatMap(url) {
    //TODO: REMOVE ME
    dateCounter = new Date();
    //With the AWS API, the response is automatically gzipped. If a different deployment is used, make sure this
    //still works
    d3fetch.json(url).then(function (data) {
        //TODO: REMOVE ME
        nextDateCounter = new Date()
        time_passed = Math.abs(nextDateCounter - dateCounter)/1000;
        dateCounter = nextDateCounter;

        console.log ("Got Data from server after: " + time_passed + "sec from sending request");
        loadHeatMap(data)
    }).catch(function(error) { console.log(error); });
}

function getColorFromDuration (duration) {
    return toCssColor(computeColorFromDuration(duration));
};



//time map boundries
var boundry1 = 900;  //15min
var boundry2 = 1800; //30min
var boundry3 = 2700; //45min
var boundry4=3600; //60min
var boundry5=4500; //75min
var boundry6=5400; //90min
var boundry7=7200; //120min

//colors for the heat map
var colorMap = new Map ([
    [900 ,'rgb(199,199,199)'],
    [1800, 'rgb(160,206,160)'],
    [2700, 'rgb(163,163,207)'],
    [3600, 'rgb(207,207,163)'],
    [4500, 'rgb(206,160,160)'],
    [5400, 'rgb(207,168,207)'],
    [7200,'rgb(132, 132,132)']
]);


function computeColorFromDuration (duration) {
    var r, g, b, ratioForLuminace, hslColor, selectedRange;
    //select correct range
    if (duration < boundry1) {
        selectedRange = boundry1;
    } else if (duration >= boundry1 && duration < boundry2) {
        selectedRange = boundry2;
    } else if (duration >= boundry2 && duration < boundry3) {
        selectedRange = boundry3;
    } else if (duration >= boundry3 && duration < boundry4) {
        selectedRange = boundry4;
    } else if (duration >= boundry4 && duration < boundry5) {
        selectedRange = boundry5;
    } else if (duration >= boundry5 && duration < boundry6) {
        selectedRange = boundry6;
    } else {
        selectedRange = boundry7;
    }

    //compute color
    hslColor = new tinycolor(colorMap.get(selectedRange));
    ratioForLuminace = 50 - Math.round((duration / selectedRange) * 50 );
    hslColor.lighten(ratioForLuminace);
    hslColor.toRgb();
    r = Math.round(hslColor._r);
    g = Math.round(hslColor._g);
    b = Math.round(hslColor._b);
    return {red: r, green: g, blue: b};
};

function toCssColor (c, alpha) {
    if (alpha) {
        return sprintf('rgba(%s, %s, %s, %s)', c.red, c.green, c.blue, alpha);
    } else {
        return sprintf('#%02x%02x%02x', c.red, c.green, c.blue);
    }
};

function loadHeatMap(data) {
    var heatMatrix= data.heat_maps[0].heat_matrix;
    var startingProcessingJsonDate = new Date();
    data= [];
    var scale = 0;
    heatMatrix.lines.forEach(function(lines) {
        lines.duration.forEach(function(duration) {
            if (duration !== null) {
                scale = Math.max(duration, scale);
            }
        });
    });

    var heatMapPixels = [];
    heatMatrix.lines.forEach(function(lines/*, i*/) {
        lines.duration.forEach(function(duration, j) {
            var color;
            if (duration !== null) {
                color = getColorFromDuration(duration);
            } else {
                color = '#000000';
                // for the moment, we don't want to print the null duration squares because
                // it impacts the performances of the navigator.
                return;
            }
            var rectangle = [
                [heatMatrix.line_headers[j].cell_lat.max_lat, lines.cell_lon.max_lon],
                [heatMatrix.line_headers[j].cell_lat.min_lat, lines.cell_lon.min_lon]
            ];
            /*heatMapMarkersGroup.addLayer(makePixel(rectangle, color, duration));*/
            heatMapPixels.push(makePixel(rectangle, color, duration));
        });
    });
    //TODO: REMOVE ME
    nextDateCounter = new Date()
    time_passed = time_passed + Math.abs(nextDateCounter - dateCounter)/1000;
    dateCounter = nextDateCounter;
    console.log ("finished building heat map layer: " + time_passed  + "sec from sending request");
    addHeatMapLayer(heatMapPixels);
    //TODO: REMOVE ME
    nextDateCounter = new Date()
    time_passed = time_passed + Math.abs(nextDateCounter - dateCounter)/1000;
    console.log ("finished adding heat map layer: " + time_passed + "sec from sending request");
    dateCounter = nextDateCounter;
}

function makePixel (PolygonCoords, color, duration) {
    var sum = 'not accessible';
    if (duration !== null) {
        sum = sprintf('duration: %s', durationToString(duration));
    }
    return L.rectangle(PolygonCoords, {
        smoothFactor: 0,
        color:  '#555555',
        opacity: 0,
        weight: 0,
        fillColor: color,
        fillOpacity: 0.7
    }).bindPopup(sum);
};

function durationToString (duration) {
    var res = '';
    var seconds = duration % 60;
    var minutes = Math.floor(duration / 60) % 60;
    var hours = Math.floor(duration / (60 * 60)) % 24;
    var days = Math.floor(duration / (24 * 60 * 60));

    if (days !== 0) { res += sprintf('%sd', days); }
    if (hours !== 0) { res += sprintf('%sh', hours); }
    if (minutes !== 0) { res += sprintf('%smin', minutes); }
    if (seconds !== 0) { res += sprintf('%ss', seconds); }

    if (! res) {
        return '0s';
    } else {
        return res;
    }
};



var navitia_server_url= "http://localhost:9191/v1/coverage/default/heat_maps";
/*var navitia_server_url= "https://ll7ijshrc0.execute-api.eu-central-1.amazonaws.com/NavitiaTimeMap/heat_maps";*/
var resolution = "750";

var date_time_picker = $('#datetimepicker').datetimepicker({
    formatDate: 'd.m.Y',
    formatTime: 'H:i',
    minDate:'21.10.2018',
    maxDate:'27.10.2018',
    showSecond: false,
    step: 30,
});

//Default time
date_time_picker.val('2018/10/21 08:00');

/**Switch Button**/
//Setting the switch button and attaching it's style to a var
$('#switchButton').toggles({
    click: true, // allow clicking on the toggle
    text: {
        on: 'FROM', // text for the ON position
        off: 'TO' // and off
    },
    on:true,
    type: 'select',
    height: '30',
    width: '60'
});
var switchButton = $('#switchButton').data('toggles');
$('#switchButton').on("toggle", invalidateRunButton);

/**Transit Mode button and speed for overriding bike as walking with double speed**/
function setTransitModeAsDefault() {
    $('input:radio[name=transitMode]')[0].checked = true;
}
setTransitModeAsDefault();
//Invalidating the run button in case of change
$('input:radio').on("click",invalidateRunButton);

function getTransitMode(mode) {
    return $('input:radio[name=transitMode]:checked').val();
}
function getTransitModeUrl() {
    var mode = getTransitMode($('input:radio[name=transitMode]:checked').val());
    //At alpha version we consider bike to be walking in 4.1 ms speed,
    //so we set the frist and last walking modes to walking and we disallow use of transit (navitia hack).
    if (mode ==="walking" || mode === "bike") {
        return "&first_section_mode%5B%5D=walking&last_section_mode%5B%5D=walking" +
            "&allowed_id[]=physical_mode:Bus&forbidden_uri[]=physical_mode:Bus"
    }  else {
        return "";
    }
}

function getSpeed(mode) {
    if (mode=="bike") {
        return "&walking_speed=4.1";
    } else if (mode==="walking") {
        return "&walking_speed=1.2";
    } else  {
        return "";
    }
}
/**
 * RUN Button
 * **/
var runButton = $('#runButton').on("click", generateHeatMap);

/**
 * Time slider
 */

var handle = $( "#custom-handle" );
var selectedTimeRange;
var timeSlider = $('#timeSlider').slider({
    step: 15,
    min: 15,
    max: 120,
    value: 60,
    create: function() {
        var value = $( this ).slider( "value" );
        handle.text(value);
        selectedTimeRange = parseInt(value);
    },
    slide: function( event, ui ) {
        var value = ui.value;
        handle.text( value);
        selectedTimeRange = parseInt(value);
        invalidateRunButton();
    }
});



function generateHeatMap() {
    runButton.text("Run");
    if (starting_point_marker === undefined) {
        alert("Please select a starting point on the map");
        return;
    }

    //resetting the marker to blue
    if (starting_point_marker) {
        starting_point_marker = createNewMarker(starting_point_marker, starting_location, false);
    }

    //Getting the time from the Date & time picker
    var dt = new Date(date_time_picker.val());
    var dateTimeString = sprintf('%s%s%sT%s%s00', dt.getFullYear(),
        ("0" + (dt.getMonth() + 1)).slice(-2),
        ("0" + (dt.getDate())).slice(-2),
        ("0" + (dt.getHours())).slice(-2),
        ("0" + (dt.getMinutes())).slice(-2));

    //Select from or to according to user's selection
    var from_to = switchButton.active ? "&from=" : "&to=";

    //Get mode, transit by default
    var mode = getTransitMode()

    //get Speed for simulating bike as walking in 4.1 mps
    var speed = getSpeed(mode);

    //calcualte max duration in seconds
    var max_duration = selectedTimeRange*60;

    var heatMapJsonUrl = navitia_server_url +
        "?max_duration=" + max_duration +
        from_to + starting_location.lng +
        "%3B" + starting_location.lat +
        "&datetime=" + dateTimeString +
        getTransitModeUrl() +
        speed +
        "&resolution=" + resolution;


    //TODO: REMOVE ME
    console.log(heatMapJsonUrl);


    //remove current heat map - Couldn't find how to get the layerId as a map method
    // as long as we don't have many layers, this is ok
    map.eachLayer(function(layer){
        if (layer._leaflet_id === heatMapLayerId) {
            map.removeLayer(layer);
        }
    });

    //add new heat map
    addHeatMap(heatMapJsonUrl)

}

createMap();
map.on('click', function (e) {
    handleMarkerDrag(e.latlng);
});

//Crating the default map
generateHeatMap();

//Legend
var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'legend'),
        time_intervals  = [0, 15, 30, 45, 60, 75, 90, 120],
        labels = [];
    div.innerHTML = "<p>Minutes to arrive</p>"
    // loop through our time intervals and generate a label with a colored square for each interval
    for (var i = 0; i < time_intervals.length-1; i++) {
        div.innerHTML +=
            '<i style="background:' + colorMap.get(time_intervals[i+1]*60) + '"></i> ' +
            time_intervals[i] + (time_intervals[i + 2] ? '&ndash;' + time_intervals[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);




