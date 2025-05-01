#import "@preview/cetz:0.3.4"

#let size = 60mm

#set page(width: size + 20mm, height: size, margin: 2mm)

#set align(horizon + center)
#set text(font: "JetBrainsMono NF")

#cetz.canvas({
  import cetz.draw: *

  let k = 40mm
  let w = 7mm
  let h = 7mm
  let center = k / 2

  rect((0, 0), (rel: (k, k)), fill: black, stroke: black)

  rect((center - w / 2, 0), (rel: (w, k)), fill: white, stroke: white)

  rect((0, center - h / 2), (rel: (k, h)), fill: white, stroke: white)

  rect((0, 0), (rel: (k, k)), stroke: black)

  line((0, k + 3mm), (rel: (k, 0)), mark: (symbol: "straight"), name: "k")

  line((center - w / 2, -3mm), (rel: (w, 0)), mark: (symbol: "straight"), name: "w")
  line((k + 3mm, center - h / 2), (rel: (0, h)), mark: (symbol: "straight"), name: "h")

  content("k", padding: .1, anchor: "south", [kernel_size])
  content("w", padding: .1, anchor: "north", [cross_width])
  content("h", padding: .2, anchor: "west", [cross_height])
})
