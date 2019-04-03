<?php
/* Update a specific comment in the comments table
 * it returns SERVER content as JSON objects
 *
 * this is the prototype development version of the full ADAM implementation
 */
//first get our URL components

$commentid = $_GET['commentid'];
if ($commentid === null)
{
  exit(1);
}
if ($commentid === "")
{
  exit(1);
}
$comstring = $_GET['comment'];

// connect to the sql server
$db = mysqli_connect('artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com','artmaster','ArtMaster51','artmaster');
if (!$db) {
   echo "Debugging errno: ". mysqli_connect_errno(). PHP_EOL;
}

$qstring = 'UPDATE comments SET comment = \''.$comstring.'\' where id='.$commentid.';';
echo $qstring;
if ( $result = mysqli_query( $db, $qstring ) ) 
{
    echo $result;
}
else
{
    echo "database query failed";
}
?>
