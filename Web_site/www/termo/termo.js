 this.CurrentExample = function(operation) {
var format = $("#image-download input:radio[name=format]:checked").val();
if (Flotr.isIE && Flotr.isIE < 9) {
alert("Your browser doesn't allow you to get a bitmap image from the plot, " + "you can only get a VML image that you can use in Microsoft Office.<br />");
}
if (operation == "to-image") {
graph.download.saveImage(format, null, null, true);
} else if (operation == "download") {
graph.download.saveImage(format);
} else if (operation == "reset") {
graph.download.restoreCanvas();
}
}; 

var
// Container div:
container = document.getElementById("chart"),
	  // First data series:
	  d1 = [],
	  // Second data series:
	  d2 = [],
	  // A couple flotr configuration options:
	  d3 = [],
	  d4 = [],
	  d5 = [],
	  d6 = [],
	  d7 = [],
	  options = {
grid: {
minorVerticalLines: true
      },
      //mouse: {track: true, relative: true},
mouse: {
track: true,
       //trackAll : true,
       relative: true,
       trackFormatter: function(point) {
	       var xval = new Date(Number(point.x) * 1000);
	       // should look into momentjs library (http://momentjs.com/) for some date functions
	       return xval.getHours().toString() + ":" + xval.getMinutes() + ", " + point.y.toString();
       }
       },
xaxis: {
title: "Ora",
       mode: 'time',
       timeFormat: "%H:%M",
       timeUnit: 'second',
       timeMode:'locale',
       labelsAngle: 45,
       showLabels: true,  
       showMinorLabels: true
       },
yaxis: {min: 18, max:25,title: "Temperatura",},
       spreadsheet: {
show:true},
       HtmlText: false,
       colors: ['#00A8F0', '#C0D800', '#CB4B4B', '#4DA74D','#0000FF', '#000000']
	  },
	  i, graph;

// Generated second data set:
//  for (i = 0; i < 14; i += 0.5) {
//    d2.push([i, Math.sin(i)]);
//  }

// Draw the graph:
//  graph = Flotr.draw(
//    container,  // Container element
//    [ d1, d2 ], // Array of data series
//    options     // Configuration options
//  );
