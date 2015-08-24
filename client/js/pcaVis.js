
//----> The Visualisation Plot

var pcaVis = function pcaVis(s) {

  // initialise as a container with children
  BasicVis.Container.call(this, s);

  // appends a div to use later to print the info about the net (params etc)
  this.info_meta = this.inner.append("div");
  this.info_vis = this.inner.append("div");

  // set tooltips function
  function tooltips (tooltype, appendage, labels) {
    // console.log("called");
    if (tooltype == "text") {
      console.log(tooltype);
      // creates a new tooltip, and binds to the new data!
      this.tooltext = new BasicVis.TextTooltip();
      this.tooltext._labels = labels;
      this.tooltext.bind(appendage.points);
      this.tooltext.bind_move(appendage.s);
      this.tooltext.div.style("font-size", "85%");
    } else if (tooltype == "img") {
      console.log(tooltype);
      this.toolimg = new BasicVis.ImgTooltip();
      this.toolimg.img_display.shape([28,28]);
      this.toolimg.img_display.imgs(mnist_xs);
      this.toolimg.bind(appendage.points);
      this.toolimg.bind_move(appendage.s);
    };
  }

  this.meta_display = this.new_child(BasicVis.ScatterPlot)
    .N(DATA.PCA.length/2)
    .xrange.fit(DATA.PCA)
    .yrange.fit(DATA.PCA)
    .x(function(i) {return DATA.PCA[2*i  ];})
    .y(function(i) {return DATA.PCA[2*i+1];})
    .color(function(i) {
      // set according to the label
      var hue = 180;//*DATA.EPOCH[i]/5;
      var saturation = DATA.EPOCH[i]/DATA.EPOCH.length;
      var lightness = 0.5;
      return d3.hsl(hue, saturation, lightness);
    });

  this.meta_display
    .enable_zoom()
    .bindToWindowResize()

  this.main_display = this.new_child(BasicVis.ScatterPlot)
    .N(0)
    .color( function(i) {
      var hue = 180*DATA.TSNE_LABELS[i]/10.0;
      var saturation = 0.5;
      var lightness = 0.5;
      return d3.hsl(hue, saturation, lightness);
    });

  var main_display = this.main_display;

  this.main_display.show = function show(i) {
    var coords = DATA.TSNE_DATA[i];
    var labels = DATA.TSNE_LABELS;

    var NO_POINTS = 0;

    if (sensible_number_of_points < DATA.TSNE_DATA.length/2) {
      NO_POINTS = sensible_number_of_points;
    } else {
      NO_POINTS = DATA.TSNE_DATA[i].length/2;
    }

    main_display
      .N(NO_POINTS)
      .xrange.fit(coords)
      .yrange.fit(coords)
      .x(function(i) {return coords[2*i  ];}) // gets the x-coords responding to the index
      .y(function(i) {return coords[2*i+1];});

    main_display
    .enable_zoom()
    .bindToWindowResize()

    tooltips("text", main_display, labels);
  }

  // javascript scoping, to ensure it is THIS function
  // not the this of the 'circle' i.e
  var this_ = this;

  this.meta_display.mouseover( function(i) {

    this_.info_meta.html("<center> Layer: " + DATA.LAYER[i] + " Epoch: " + DATA.EPOCH[i]
        + "</center");
    
    this_.main_display.show(i);
  });

}

pcaVis.prototype = Object.create(BasicVis.Container.prototype);

pcaVis.prototype.child_layout = function child_layout() {

 // gets the width of the main representation div 
  W = parseInt(this.s.style('width'));

  var gutter = W/16;
  var main = W - gutter*6;
  var main_box_size = (main/3) * 2;
  var nav_box_size = main/3;
  var dims = [main_box_size, main_box_size];
  var dims_nav = [nav_box_size, nav_box_size];
  var H = W/2;

  this.inner
    .style('width', W)
    .style('height', H); 

  this.meta_display.size(W/300);
  this.meta_display.div
    // .style('border', '1px solid #959595')
    .style('background-color', 'white')
    .pos([gutter*2,H/3])
    .size(dims_nav); 

  this.main_display.size(W/400);
  this.main_display.div
    // .style('border', '1px solid #959595')
    .style('background-color', 'white')
    .pos([nav_box_size+gutter*4,gutter])
    .size(dims); 

  this.info_meta
    .style('position', 'absolute')
    .style('font-size', '14px')
    .style('width', W)
    .style('height', box_size/3)
    .style('top', gutter)
    .style("fill", "red");
    // .style('color', 'blue');
    // .style('left', gutter*3)
    // .style('text-align', center);

  return this;
}

function pca_vis_space() {
  var pca_visd = new pcaVis("#pca_vis");
  return pca_visd;
}

pca_vis_space();