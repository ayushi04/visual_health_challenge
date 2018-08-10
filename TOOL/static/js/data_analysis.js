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

function updateImage(datasetPath) {
  console.log('---updateImage---');
  var equations = [];
  //$(".dim:checked").each(function() {
  //  dimList.push($(this).val());
  //});
  //dimList = dimList.join(' ');
  $('#loading').html("<img src={{ url_for('static',filename='loading.gif') }}> loading...");
  $.ajax({
    url:"/image"
    data: {
      equation: equations,
      datasetpath: datasetPath
    },
    contentType: 'application/json; charset=utf-8',
    success: function(result) {
      console.log(result);
      //$("html").empty();
      $("html").append(result);
    },
     error: function(error) {
                console.log('ERROR',error);
            } 
  });

}