var colNames;

//This method get the value of input parameter passed by backend (python code)
// and sends it to javascript variable
function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function dynamicallyLoadSelectList(divId,datasetPath) {
	console.log('----dynamicallyLoadSelectList---');
  var colNames;
	d3.csv(datasetPath, function(error, csv) {
      colNames = d3.values(csv)[0];
      console.log(colNames);
      
    var htmlstr = '';
    for (k in colNames) {
  		if (k != 'classLabel' && k != 'id') {
  		  htmlstr = htmlstr.concat('<input type="checkbox" class="dim" value="' + k + '">' + k + '<br>');
  	      }
  	}
  console.log(htmlstr);
	$(divId).html(htmlstr);
  });
}

function loadImg(url, w, h,mapid,parent,imgType) {
  var MIN_ZOOM = -1;
  var MAX_ZOOM = 5;
  var INITIAL_ZOOM = 1;
  var ACTUAL_SIZE_ZOOM = 3;
  var map = L.map(mapid, {
    minZoom: MIN_ZOOM,
    maxZoom: MAX_ZOOM,
    center: [0, 0],
    zoom: INITIAL_ZOOM,
    crs: L.CRS.Simple
  });
  //var imgType='_'+ $('#changeImgType').val();
  var southWest = map.unproject([0, h], ACTUAL_SIZE_ZOOM);
  var northEast = map.unproject([w, 0], ACTUAL_SIZE_ZOOM);
  console.log(southWest, northEast);
  var bounds = new L.LatLngBounds(southWest, northEast);

  L.imageOverlay(url, bounds).addTo(map);
  map.setMaxBounds(bounds);

  map.on('click', function(e) {
    var x = (e.latlng.lat) / (southWest.lat - northEast.lat);
    var y = (e.latlng.lng) / (-southWest.lng + northEast.lng);
    console.log(x + ':' + y);
    var gridPatterns = $("input[name=ptype]:checked").val();
    var grid = $("input[name=grid]:checked").val();
    console.log(gridPatterns+' '+grid);
    $('#loading').html('<img src="loading.gif"> loading...');
    $('#table2').html('-');
    $('#table3').html('-');
/*
    $.ajax({
      url: "/highlightPattern",
      data: {
        x: x,
        y: y,
        datasetPath: getParameterByName('datasetPath'),
        imgType: imgType,//$('#changeImgType').val(),
        id: '',
        gridPatterns:gridPatterns,
        grid: grid
      },
      contentType: 'application/json; charset=utf-8',
      success: function(result) {
        //$("#div1").html("<img src='static/output/img_bea.png'></img>");
        result = JSON.parse(result);
        subspace = result['dim'];
        var rowPoints = JSON.parse(result['rowPoints']);
        var colPoints = JSON.parse(result['colPoints']);
        var rowPoints_save = JSON.parse(result['rowPoints_save']);
        var colPoints_save = JSON.parse(result['colPoints_save']);
        var allFig= result['allFig'];
        console.log('subspace'+subspace);
        console.log(JSON.parse(result['rowPoints']));
        console.log(JSON.parse(result['colPoints']));
        console.log(JSON.parse(result['dist']), JSON.parse(result['pair']));
        $('#'+mapid).remove();
        $('#'+parent).append('<div id="'+mapid+'" style="width: 500px; height: 400px;"></div>')
        d = new Date();
        if(imgType=='closed') {
        loadImg("/static/output/temp_closed.png?" + d.getTime(),"/static/output/temp_closed_composite.png?" + d.getTime(), 2229, 2058,mapid,mapid2,parent,parent2,'closed');
        $('#loading').html('-');
        var fname = 'output/legend_'+imgType+'.html?' + d.getTime();
        $('#loading').html('-');
        }
        else {
          loadImg("/static/output/temp_heidi.png?" + d.getTime(),"/static/output/temp_heidi_composite.png?" + d.getTime(), 2229, 2058,mapid,mapid2,parent,parent2,'heidi');
          $('#loading').html('-');
          }
        $('#table2').html(convertJsonToTable(JSON.parse(result['rowPoints']),'col'));
        $('#table3').html(convertJsonToTable(JSON.parse(result['colPoints']),'row'));
        //drawGraph(JSON.parse(result['dist']), JSON.parse(result['pair']));
        drawParallelCoordinate('parallelPlot');
        drawGiantWheel('#windrose1');
        $('#pointsPlots').html('');
        console.log('adding crovhd visualization to gui!!');
        $('#crovhd').html('<img src="/static/output/rowColPoints.png?'+ d.getTime() +'">');
        drawPointsComparison('pointsPlots',rowPoints_save,colPoints_save,subspace);
        //uploadHistorgram();
       
      },
      error: function(result) {
        console.log(result);
      }
    });
    */
  });
}


function updateImage() {
  console.log('---updateImage---');
  var equations = [];
  var panel=$('#bitvector');
  var inputs=panel.find('input');
  for (var i=0;i<inputs.length;i++) {
    if(inputs[i].value!='')
      equations.push(inputs[i].value);
  }
  equations = equations.join(':');
  $('#loading').html("<img src={{ url_for('static',filename='loading.gif') }}> loading...");
  console.log(equations);
  $.ajax({
    url:"/image",
    data: {
      equations: equations,
      datasetPath: datasetPath
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
     console.log(result);
      var result1=JSON.parse(result);
      if(result1.hasOwnProperty('error')) {
        var message=result1['error'];
        $('.error_msg').html(message);
        $('.alert_msg').css("display", "inline-block");
      }
      else{
        $('#mapid').remove();
        $('#parent').append('<div id="mapid" style="width: 500px; height: 400px;"></div>')
        d = new Date();
        //(url, w, h,mapid,parent,imgType)
        loadImg("/static/output/consolidated_img.png?" + d.getTime(), 2229, 2058,'mapid','parent','heidi');
        $('#loading').html('-');
        var fname = '/static/output/legend_heidi.html?' + d.getTime();
        $('#legend').load(fname);
      }
    },
     error: function(error) {
                console.log('ERROR',error);
            } 
  });

}