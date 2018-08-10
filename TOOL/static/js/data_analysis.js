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

function updateImage() {
  console.log('---updateImage---');
  var equations = [];
  var panel=$('#bitvector');
  var inputs=panel.find('input');
  for (var i=0;i<inputs.length;i++) {
    if(inputs[i].value!='')
      equations.push(inputs[i].value);
  }
  equations = equations.join(',');
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
      //$("html").empty();
      //$("html").append(result);
    },
     error: function(error) {
                console.log('ERROR',error);
            } 
  });

}