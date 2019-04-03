// code for manipulating the view in the DAM

function addViewTextList(aplace, colnames, rowinfo)
{
   console.log("addViewTextList");
   var arow = document.createElement("tr");
   for (i=0; i < colnames.length; i++)
   {
       var atd = document.createElement("td");
       var tname = document.createTextNode(colnames[i]);
       atd.appendChild(tname);
       arow.appendChild(atd);
   }
   aplace.appendChild(arow);

   for (j=0; j < rowinfo.length; j++)
   {
       var brow = document.createElement("tr");
       for (i=0; i < rowinfo[j].length; i++)
       {
           var atd = document.createElement("td");
           var tname = document.createTextNode(rowinfo[j][i]);
           atd.appendChild(tname);
           brow.appendChild(atd);
       }
       aplace.appendChild(brow);
   }
}


function addViewList(aplace, rowinfo)
{
   console.log("addViewList");
   console.log(rowinfo);
   var arow = document.createElement("tr");
   var keys = Object.keys(rowinfo.children[0]);
   for (i=0; i < keys.length; i++)
   {
       var atd = document.createElement("td");
       var tname = document.createTextNode(keys[i]);
       atd.appendChild(tname);
       arow.appendChild(atd);
   }
   aplace.appendChild(arow);

   for (j=0; j < rowinfo.children.length; j++)
   {
       var brow = document.createElement("tr");
       var arow = rowinfo.children[j];
       for (i=0; i < keys.length; i++)
       {
           var atd = document.createElement("td");
           var tname = document.createTextNode(arow[keys[i]]);
           if (keys[i] == "id")
           {
               var a = document.createElement('a');
               var linkText = document.createTextNode(arow[keys[i]]);
               a.appendChild(linkText);
               a.href = "wmedit.html?imgid="+arow[keys[i]];
               tname = a;
           }
           if (arow[keys[i]].startsWith("http:"))
           {
               var a = document.createElement('a');
               var linkText = document.createTextNode(arow[keys[i]]);
               a.appendChild(linkText);
               a.href = arow[keys[i]];
               tname = a;
           }
           atd.appendChild(tname);
           brow.appendChild(atd);
       }
       aplace.appendChild(brow);
   }
}

function deleteComment(commentid)
{
   console.log(commentid);  
   statDeleteComment(commentid);
}


function updateComment(commentid)
{
   console.log(commentid);  
   acomment = document.getElementById(commentid).value;
   statUpdateComment(commentid,acomment);
}

function newComment()
{
   console.log('newcomment');  
   statNewComment();
}
function addViewCommentList(aplace, rowinfo)
{
   console.log("addViewCommentList");
   console.log(rowinfo);

// handle navigation bar
   var arow = document.createElement("tr");
   var aprev = rowinfo["prev"];
   var anext = rowinfo["next"];
   var atd = document.createElement("td");
 
   var a = document.createElement('a');
   var linkText = document.createTextNode("prev");
   a.appendChild(linkText);
   a.href = "wmedit.html?imgid="+aprev;
   atd.appendChild(a);
   arow.appendChild(atd);

   var atd = document.createElement("td");
   var a = document.createElement('a');
   var linkText = document.createTextNode("next");
   a.appendChild(linkText);
   a.href = "wmedit.html?imgid="+anext;
   atd.appendChild(a);
   arow.appendChild(atd);

   aplace.appendChild(arow);

// put in the thumbnail
   var arow = document.createElement("tr");
   var thumburi = rowinfo["uri"];
   var atd = document.createElement("td");
   atd.setAttribute('colspan',2);
   var tname = document.createElement("IMG");
   console.log(thumburi);
   tname.setAttribute('src',thumburi);
   tname.setAttribute('width',320);
   atd.appendChild(tname);
   arow.appendChild(atd);
   aplace.appendChild(arow);

// lay out header information
  if (rowinfo.children.length != 0) {
   var arow = document.createElement("tr");
   var keys = Object.keys(rowinfo.children[0]);
   for (i=0; i < keys.length; i++)
   {
       var atd = document.createElement("td");
       var tname = document.createTextNode(keys[i]);
       atd.appendChild(tname);
       arow.appendChild(atd);
   }
   aplace.appendChild(arow);


// lay out the comments for the given image
   for (j=0; j < rowinfo.children.length; j++)
   {
       var brow = document.createElement("tr");
       var arow = rowinfo.children[j];

           var atd = document.createElement("td");
           var txtValue = document.createTextNode(arow["id"]);
           atd.appendChild(txtValue);
           brow.appendChild(atd);

           var atd = document.createElement("td");
           var txtValue = document.createTextNode(arow["comment"]);
           var tname = document.createElement('textarea')
           tname.setAttribute('rows','4');
           tname.setAttribute('cols','40');
           tname.setAttribute('maxlength','1024');
           tname.setAttribute('id',arow["id"]);
           tname.appendChild(txtValue);
           atd.appendChild(tname);
           brow.appendChild(atd);

       var atd = document.createElement("td");
       var tname = document.createElement('input')
       tname.setAttribute('type','button');
       tname.setAttribute('value','-');
       var stxt = 'deleteComment('+arow[keys[0]]+')';
       tname.setAttribute('onclick',stxt);
       atd.appendChild(tname);
       brow.appendChild(atd);

       var atd = document.createElement("td");
       var tname = document.createElement('input')
       tname.setAttribute('type','button');
       tname.setAttribute('value','U');
       var stxt = 'updateComment('+arow[keys[0]]+')';
       tname.setAttribute('onclick',stxt);
       atd.appendChild(tname);
       brow.appendChild(atd);

       aplace.appendChild(brow);
   }
  }

   // lay out the button to add comments for the image
   var crow = document.createElement("tr");
   var atd = document.createElement("td");
   var tname = document.createElement("input");
   tname.setAttribute('type','button');
   tname.setAttribute('value','+');
   tname.setAttribute('onclick','newComment()');
   atd.appendChild(tname);
   crow.appendChild(atd);
   aplace.appendChild(crow);
}
