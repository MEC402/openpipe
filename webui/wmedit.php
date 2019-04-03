<html>
<!-- simple web based editor for adding info to an image set-->
<!-- part of the world museum digital asset management solution -->

<!-- this is to let you add notes to a specific image -->
<!-- basic layout Image and properties at top -->
<!-- all notes listed below -->
<head>
<title>WM Digital Assets Editor</title>
</head>
<body>
<div id="oneimage">
<div id="image" width="20%">
Image Goes Here
</div>
<div id="props" width="60%">
URI:
Size:
Format:
</div>
<div id="textinfo">
<form id="imageform">
<ul>
<li><textarea name="comment" form="imageform" cols=80 rows="6">Example input</textarea>
<input type="button" name="remove" value="-">
</li>
<li><input type="button" name="add" value="+"></li>
</ul>
</form>
</div>
</div>
</body>
</html>
