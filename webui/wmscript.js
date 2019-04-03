var maxwidth = screen.width;
var maxheight = screen.height;
//var centerx=maxwidth/2+maxwidth/64;
//var centery=maxheight/2+maxheight/64;
var centerx=maxwidth/2;
var centery=maxheight/2;
var vradius=Math.min(maxheight,maxwidth)/3;
var iwidth=maxwidth/40;

function project(x,y) {
  var angle = x*Math.PI/180, radius = y;
  console.log(x);
  console.log(angle);
  return [radius * Math.cos(angle), radius*Math.sin(angle)];
}

// Set the dimensions and margins of the diagram
var margin = {top: 20, right: 90, bottom: 30, left: 90},
    width = maxwidth - margin.left - margin.right,
    height = maxheight - margin.top - margin.bottom;

// append the svg object to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("body").append("svg")
    .attr("style","border: 1px solid black;")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate("
          + (centerx) + "," + (centery) + ")");

var i = 0,
    duration = 500,
    root;

// declares a tree layout and assigns the size
//var treemap = d3.tree().size([height, width]);
//var treemap = d3.tree().size([2*Math.PI,1]);
var treemap = d3.tree().size([360,vradius]);
//var treemap = d3.tree().size([2*Math.PI,5]).separation(function(a,b) { return (a.parent == b.parent ? 1: 2);});

// Assigns parent, children, height, depth
root = d3.hierarchy(treeData, function(d) { return d.children; });
//root.x0 = height / 2 ;
//root.y0 = 10;
root.x0 = 0;
root.y0 = 0;

// Collapse after the second level
//root.children.forEach(collapse);
//collapse(root);
  // Assigns the x and y position for the nodes

collapse(root);
update(root);

// Collapse the node and all it's children
function collapse(d) {
  if(d.children) {
    d._children = d.children
    d._children.forEach(collapse)
    d.children = null
  }
}

function update(source) {

   var  atreeData = treemap(root);

  // Compute the new tree layout.
  var nodes = atreeData.descendants(),
      links = atreeData.descendants().slice(1);

  // Normalize for fixed-depth.
//  nodes.forEach(function(d){  d.y = d.depth * 128});

  // ****************** Nodes section ***************************

  // Update the nodes...
  var node = svg.selectAll('g.node')
      .data(nodes, function(d) {return d.id || (d.id = ++i); });

  // Enter any new modes at the parent's previous position.
  var nodeEnter = node.enter().append('g')
      .attr('class', 'node')
      .attr("transform", function(d) {
        return "rotate(" + (d.x) + ") " + "translate(" + source.y0 +"," + 0 + ")";
    })
    .on('click', click);

  // Add Circle for the nodes
  nodeEnter.append('circle')
      .attr('class', 'node')
      .attr('r', 1e-6)
      .style("fill", "none");

  // Add Image for the nodes
  var images = nodeEnter.append('svg:image')
      .attr("xlink:href", function(d) {  return d.data.thumb; } )
      .attr("x", -iwidth)
      .attr("y", -iwidth)
      .attr("width", iwidth*2)
      .attr("height", iwidth*2)
      .attr("transform", function(d) {
          return "translate(" +(-0) +"," + 0 + ")" + "rotate(" + (-d.x) +") "
               + "translate(" +(0) +"," + 0 + ")";
      });

  // enlarge on hover
  var setEvents = images
//  var setEvents = nodeEnter
         .on('mouseenter', function() {
           // select element in current context
           d3.select(this)
           .transition()
           .attr("x", function(d) { return -iwidth*2; })
           .attr("y", function(d) { return -iwidth*2; })
           .attr("height", iwidth*4)
           .attr("width", iwidth*4);
         })
         .on('mouseleave', function() {
           // select element in current context
           d3.select(this)
           .transition()
           .attr("x", function(d) { return -iwidth; })
           .attr("y", function(d) { return -iwidth; })
           .attr("height", iwidth*2)
           .attr("width", iwidth*2);
         });


/*      .style("fill", function(d) {
          return d._children ? "lightsteelblue" : "#fff";
      });*/
  // Add labels for the nodes
  nodeEnter.append('text')
      .attr("dy", ".35em")
      .attr("class", "text")
      .attr("fill", "white")
      .attr("transform", function(d) {
          return "translate(" +(-0) +"," + 0 + ")" + "rotate(" + (-d.x) +") "
               + "translate(" +(0) +"," + 0 + ")";
      })
      .attr("x", function(d) {
          return d.children || d._children ? 13 : 13;
      })
      .attr("text-anchor", function(d) {
          return d.children || d._children ? "start" : "start";
      })
      .text(function(d) { return d.data.name; });

  // UPDATE
  var nodeUpdate = nodeEnter.merge(node);

  // Transition to the proper position for the node
  nodeUpdate.transition()
    .duration(duration)
    .attr("transform", function(d) { 
        return "rotate(" + (d.x) +") " + "translate(" + d.y +"," + 0 + ")";
     });

  // Update the node attributes and style
  nodeUpdate.select('circle.node')
    .attr('r', iwidth)
    .style("fill", "none") 
/*    .style("fill", function(d) {
        return d._children ? "lightsteelblue" : "#fff";
    })*/
    .attr('cursor', 'pointer');


  // Remove any exiting nodes
  var nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", function(d) {
          return "rotate(" + (d.x) +") " + "translate(" + source.y +"," + 0 + ")";
      })
      .remove();

  // On exit reduce the node circles size to 0
  nodeExit.select('circle')
    .attr('r', 1e-6);

  // On exit reduce the opacity of text labels
  nodeExit.select('text')
    .style('fill-opacity', 1e-6);

  // ****************** links section ***************************

  // Update the links...
  var link = svg.selectAll('path.link')
             .data(links, function(d) { return d.id});

  // Enter any new links at the parent's previous position.
  var linkEnter = link.enter().insert('path', "g")
      .attr("class", "link")
      .attr('d', function(d) {
        var o = {x: source.x0, y: source.y0}
        return diagonal(o, o)
       });

  // UPDATE
  var linkUpdate = linkEnter.merge(link);

  // Transition back to the parent element position
  linkUpdate.transition()
      .duration(duration)
      .attr('d', function(d){ return diagonal(d, d.parent) });

  // Remove any exiting links
  var linkExit = link.exit().transition()
      .duration(duration)
      .attr('d', function(d) {
        var o = {x: source.x, y: source.y}
        return diagonal(o, o)
      })
      .remove();

  // Store the old positions for transition.
  nodes.forEach(function(d){
    d.x0 = d.x;
    d.y0 = d.y;
  });

  // Creates a curved (diagonal) path from parent to the child nodes
  function diagonal(s, d) {
          var so = project(s.x,s.y);
          var ad = project(d.x,d.y);
          //console.log(so);
          //console.log(ad);

    path = `M ${so[0]} ${so[1]}
            C ${(so[0] + ad[0]) / 2} ${so[1]},
              ${(so[0] + ad[0]) / 2} ${ad[1]},
              ${ad[0]} ${ad[1]}`
/*
    path = `M ${s.y} ${s.x}
            C ${(s.y + d.y) / 2} ${s.x},
              ${(s.y + d.y) / 2} ${d.x},
              ${d.y} ${d.x}`
*/
    return path
  }

  // Toggle children on click.
  function click(d) {
    if (d.data.type == "file" ) {
    // lightbox functionality in here
      var link=document.createElement("a");
      link.class="fancybox";
      link.id="lightLink";
      link.href=d.data.thumb;
      link.rel="lightbox";
      this.appendChild(link);
      //document.getElementById("lightLink").click();
      //console.log(d.data.url);
      $.fancybox.open([
      {
        href: d.data.url,
        title: d.data.name
      }],  {padding: 0});
    }
    if (d.children) {
        d._children = d.children;
        d.children = null;
      } else {
        d.children = d._children;
        d._children = null;
      }
     
    update(d);
  }
}

