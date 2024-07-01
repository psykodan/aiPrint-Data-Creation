
gcode = []
inp = ""
while inp != "STOP":
    inp = input("Enter gcode: ")
    gcode.append(inp)

extrusion_change_operation = input("Enter extrusion change operation")
extrusion_change_factor  = float(input("Enter extrusion change amount"))
if extrusion_change_operation == "/":
    for idx, g in enumerate(gcode[:-1]):
        gcode_split = g.split(" ")
        if "E" in gcode_split[-1]:
            extrusion = float(gcode_split[-1][1:])
            extrusion = extrusion / extrusion_change_factor
            gcode[idx]=gcode_split[0]+ " "+ gcode_split[1]+ " "+ gcode_split[2]+ f" E{extrusion}"
if extrusion_change_operation == "*":
    for idx, g in enumerate(gcode[:-1]):
        gcode_split = g.split(" ")
        if "E" in gcode_split[-1]:
            extrusion = float(gcode_split[-1][1:])
            extrusion = extrusion * extrusion_change_factor
            gcode[idx]=gcode_split[0]+ " "+ gcode_split[1]+ " "+ gcode_split[2]+ f" E{extrusion}"


for line in gcode:
    print(line)