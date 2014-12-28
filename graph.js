
window.onload = makeGraph()

function Relations() {

}

function makeGraph(){
var width = screen.width,
    height = screen.height;

var color = d3.scale.category20();
var fill = d3.scale.category10();

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(30)
    .size([width, height]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("similarity.json", function(error, graph) {
  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  var link = svg.selectAll(".link")
      .data(graph.links)
      .enter().append("line")
      .attr("class", "link");

  var node = svg.selectAll(".node")
      .data(graph.nodes)
      .enter().append("circle")
      .attr("class", "node")
      .attr("r", 5)
      .style("fill", function(d) { return color(d.group); })
      .call(force.drag);

  var groups = d3.nest().key(function(d) { return d.name.charAt(0); } ).entries(graph.nodes)
  var groupPath = function(d) {
    return "M" +
           d3.geom.hull(d.values.map(function(i) { return [i.x, i.y]; }))
             .join("L") + "Z";
  };

  var groupFill = function(d, i) { return fill(i & 3); };

  node.append("title")
      .text(function(d) { return d.name; });

  link.append("title")
      .text(function(d) { return d.source.name + ", " + d.target.name})

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

      svg.selectAll("path")
         .data(groups)
         .attr("d", groupPath)
         .enter().insert("path", "circle")
         .style("fill", groupFill)
         .style("stroke", groupFill)
         .style("stroke-width", 40)
         .style("stroke-linejoin", "round")
         .style("opacity", .2)
         .attr("d", groupPath);
  });
});
}