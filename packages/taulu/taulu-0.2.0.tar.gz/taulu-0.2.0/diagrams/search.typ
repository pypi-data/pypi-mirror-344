#import "@preview/cetz:0.3.4"

#let size = 60mm

#set page(width: 100mm, height: size, margin: 2mm)

#set align(horizon + center)
#set text(font: "JetBrainsMono NF")

#cetz.canvas({
  import cetz.draw: *

  let k = 40mm

  rect((k, 0), (rel: (k, k)), stroke: black)

  line((0, k/2), (rel: (k + k / 2, 0)), mark: (end: ">", fill: black), name: "jump")
  circle("jump.start", radius: 0.4mm, stroke: red, fill: red, name: "start")
  circle("jump.end", radius: 0.4mm, stroke: blue, fill: blue, name: "end")

  line((k, k + 2mm), (rel: (k, 0)), stroke: black, mark: (symbol: "straight"), name: "region")

  content("start", padding: .2, anchor: "north", [current])
  content("jump", padding: .1, anchor: "south", [jump])
  content("end", padding: .2, anchor: "north", [search center])
  content("region", padding: .1, anchor: "south", [region])
})
