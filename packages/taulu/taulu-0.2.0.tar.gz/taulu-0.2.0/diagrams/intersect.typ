#import "@preview/cetz:0.3.4"

#set page(width: 100mm, height: 60mm, margin: 2mm)

#set align(horizon + center)
#set text(font: "JetBrainsMono NF", size: 9pt)

#cetz.canvas({
  import cetz.draw: *

  line((0, 40mm), (rel: (80mm, 0)), name: "h0")

  line((2mm, -2mm), (rel: (0, 45mm)), name: "v0")
  line((28mm, -2mm), (rel: (-1mm, 45mm)), name: "v2")
  line((78mm, -2mm), (rel: (1mm, 45mm)), name: "v3")

  line((0, 0mm), (rel: (80mm, 2mm)), stroke: red, name: "h1")
  line((12mm, -2mm), (rel: (1mm, 45mm)), stroke: red, name: "v1")

  circle((12.1mm, 0.3mm), stroke: blue, radius: 0.5mm, fill: blue, name: "ints")

  content("h0.start", padding: 0.1, anchor: "east", [0])
  content("h1.start", padding: 0.1, anchor: "east", [1])

  content("v0.end", padding: 0.1, anchor: "south", [0])
  content("v1.end", padding: 0.1, anchor: "south", [1])
  content("v2.end", padding: 0.1, anchor: "south", [2])
  content("v3.end", padding: 0.1, anchor: "south", [3])

  content("ints", padding: .1, anchor: "south-west", text(fill: blue, size: 7pt, "intersect"))

  let l = luma(0)
  let axis_style = (
    mark: (end: "straight", length: 0.1cm, stroke: 0.7pt),
    stroke: (paint: l, dash: "dotted"),
  )

  line((10mm, 50mm), (rel: (60mm, 0)), name: "cols", ..axis_style)
  line((-7mm, 43mm), (rel: (0mm, -43mm)), name: "rows", ..axis_style)

  content("cols", padding: .1, anchor: "south", [cols])
  content("rows", padding: .1, anchor: "east", [rows])
})
