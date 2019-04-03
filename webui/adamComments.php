<?php
/* this program responds to GET requests for database content
 * it returns SERVER content as JSON objects
 *
 * this is the prototype development version of the full ADAM implementation
 */
//first get our URL components

$imgid = $_GET['imgid'];
if ($imgid === null)
{
  $imgid = 1;
}
if ($imgid === "")
{
  $imgid = 1;
}

// connect to the sql server
$db = mysqli_connect('artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com','artmaster','ArtMaster51','artmaster');
if (!$db) {
   echo "Debugging errno: ". mysqli_connect_errno(). PHP_EOL;
}
$qstring = 'SELECT uri FROM images where id='.$imgid;
if ( $result = mysqli_query( $db, $qstring ) ) 
{
    while ( $row = mysqli_fetch_row( $result ) ) 
    {
         $auri= $row[0];
    }
}

$qstring = 'SELECT * FROM comments where imageid='.$imgid;
if ( $result = mysqli_query( $db, $qstring ) ) 
{
    $prev = $imgid -1;
    $next = $imgid +1;
    echo "{\n";
    echo "\"name\": \"images\",";
    echo "\"uri\": \"".$auri."\",";
    echo "\"prev\": \"".$prev."\",";
    echo "\"next\": \"".$next."\",";
    echo "\"children\": [";
    $gap ="";
    while ( $row = mysqli_fetch_row( $result ) ) 
    {
       echo $gap;
       echo "{\n";
       if ( ( $row[0] != "information_schema" ) && ( $row[0] != "mysql" ) ) 
       {
         echo "\"id\": \"". $row[0]."\"";
         echo ", ";
         echo "\"comment\": \"". $row[1]."\"";
         echo ", ";
         echo "\"collectionid\": \"". $row[2]."\"";
         echo ", ";
         echo "\"imageid\": \"".$row[3]."\"";
//         echo "\"uri\": \""."  findme  "."\"";
       }
       echo "}";
       $gap = ", ";
    }
    echo "]\n";
    echo "}";
}
else
{
    echo "database query failed";
}
?>
