
function loadJSON(file, callback) {

    var xobj = new XMLHttpRequest();
    //xobj.overrideMimeType("application/json");
    xobj.open('GET', file, true); // Replace 'my_data' with the path to your file
    xobj.responseType = 'json';
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.response);
          }
    };
    xobj.send();
 }

/*
function loadPanoJSON(fileurl)
{
  var response;
    loadJSON(fileurl, function(response) {

        //actual_JSON = JSON.parse(response);
        console.log(response);
    });
    console.log(response);
    return response;
}
*/

function findIdIndex(slist,aid)
{

//console.log(slist[0]);
//console.log(slist.length);
  for (i=0; i < slist.length; i++)
  {
    //console.log(slist[i].data.id);console.log("mark" + aid);
    if (slist[i].data.id == aid) return i;
  }
  return 0;
}
var QueryString = function () {
  // This function is anonymous, is executed immediately and
  // the return value is assigned to QueryString!
  var query_string = {};
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
        // If first entry with this name
    if (typeof query_string[pair[0]] === "undefined") {
      query_string[pair[0]] = decodeURIComponent(pair[1]);
        // If second entry with this name
    } else if (typeof query_string[pair[0]] === "string") {
      var arr = [ query_string[pair[0]],decodeURIComponent(pair[1]) ];
      query_string[pair[0]] = arr;
        // If third or later entry with this name
    } else {
      query_string[pair[0]].push(decodeURIComponent(pair[1]));
    }
  }
  return query_string;
}();

//console.log(QueryString);

function createLevels()
{
  var reslevels = { "levels": [
    {
      "tileSize": 256,
      "size": 256,
      "fallbackOnly": true
    },
    {
      "tileSize": 512,
      "size": 512
    },
    {
      "tileSize": 512,
      "size": 1024
    },
    {
      "tileSize": 512,
      "size": 2048
    },
    {
      "tileSize": 512,
      "size": 4096
    }
  ],
  "faceSize": 4096,
  "initialViewParameters": {
    "pitch": 0,
    "yaw": 0,
    "fov": 1.5707963267948966
  },
  "linkHotspots": [],
  "infoHotspots": []
};
  return reslevels;
}
