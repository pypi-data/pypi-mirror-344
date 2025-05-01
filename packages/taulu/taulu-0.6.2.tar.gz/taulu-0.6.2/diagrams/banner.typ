#import "@preview/cetz:0.3.4"

#set page(width: 68mm, height: 35mm, margin: 4mm)
#set text(font: "IBM Plex Sans", size: 25mm)

#cetz.canvas({
  import cetz.draw: *

  let h = 25mm
  let start = -4mm

  // line((0mm, -3mm), (rel: (0mm, h)))
  line((9mm, start + 2mm), (rel: (0mm, h)))
  line((23mm, start + 1mm), (rel: (0mm, h)))
  line((36mm, start - 1mm), (rel: (0mm, h)))
  line((44mm, start), (rel: (0mm, h)))

  line((0mm, h - 7mm), (rel: (60mm, -2mm)))
  line((0mm, -1mm), (rel: (60mm, 1mm)))

  content((0mm, 0.3mm), anchor: "south-west", [taulu])

  circle((9mm, -0.9mm), fill: red, stroke: red, radius: 0.3mm)
  circle((23mm, -0.7mm), fill: red, stroke: red, radius: 0.3mm)
  circle((36mm, -0.4mm), fill: red, stroke: red, radius: 0.3mm)
  circle((44mm, -0.3mm), fill: red, stroke: red, radius: 0.3mm)

  circle((9mm, 17.7mm), fill: red, stroke: red, radius: 0.3mm)
  circle((23mm, 17.3mm), fill: red, stroke: red, radius: 0.3mm)
  circle((36mm, 16.8mm), fill: red, stroke: red, radius: 0.3mm)
  circle((44mm, 16.5mm), fill: red, stroke: red, radius: 0.3mm)
})
