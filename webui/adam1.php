<?php
/* this program responds to GET requests for database content
 * it returns SERVER content as JSON objects
 *
 * this is the prototype development version of the full ADAM implementation
 */

// connect to the sql server
$db = mysqli_connect('artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com','artmaster','ArtMaster51','artmaster');
if (!$db) {
   echo "Debugging errno: ". mysqli_connect_errno(). PHP_EOL;
}

if ( $result = mysqli_query( $db, 'SELECT * FROM images' ) ) 
{
    echo "{\n";
    echo "\"name\": \"images\",";
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
         echo "\"shortname\": \"". $row[1]."\"";
         echo ", ";
         echo "\"filename\": \"". $row[2]."\"";
         echo ", ";
         echo "\"uri\": \"".$row[3]."\"";
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
