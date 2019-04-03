<html>
<!-- simple web based editor for adding info to an image set-->
<!-- part of the world museum digital asset management solution -->

<!-- list the images contained in the asset management system -->
<head>
<title>WM Digital Asset Manager</title>
</head>
<body>
<script src="adam.js" ></script>
<script src="wmview.js" ></script>
<?php
//$db = mysqli_connect('artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com','artmaster','ArtMaster51','artmaster');
$db = mysqli_connect('artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com','artmaster','ArtMaster51','artmaster');
if (!$db) {
   echo "Debugging errno: ". mysqli_connect_errno(). PHP_EOL;
}

if ( $result = mysqli_query( $db, 'SELECT * FROM images' ) ) {
	while ( $row = mysqli_fetch_row( $result ) ) {
		if ( ( $row[0] != "information_schema" ) && ( $row[0] != "mysql" ) ) {
			echo $row[0] ." ". $row[1] ." ". $row[2]. " ".$row[3]."<br>\n";
		}
	}
}
/*
if ( $result = mysqli_query( $db, 'SHOW DATABASES' ) ) {
	while ( $row = mysqli_fetch_row( $result ) ) {
		if ( ( $row[0] != "information_schema" ) && ( $row[0] != "mysql" ) ) {
			echo $row[0] . $row[1] . $row[2]. "<br>\n";
		}
	}
}
*/
?>
<div id="wmarea">
<div id="navbar" width="20%">
Prev Next
</div>
<div id="wmlist">
<table >
<tbody id="imgtable">
<tr>
<td>Filename</td><td>Tags</td><td>URI</td></tr>
<form id="wmrecs">
<tr><td>filename:</td><td> <input type="button" value="filename"></td></tr>
</form>
</tbody>
</table>
</div>
</body>
<script>
// create our handle for the museum
adam = new Adam("wmusuem");
// connect to the museum database
adam.connect("https://cs.boisestate.edu");

// now get the rows for the images
colnames = adam.getColNames("images");
somerows = adam.getRows("images");

// now create the selectable list
aplace = document.getElementById("imgtable");
addViewList(aplace,colnames,somerows);
</script>
</html>
