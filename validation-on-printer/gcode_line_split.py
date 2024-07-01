gcode1 = input("Enter gcode point 1: ")
gcode2 = input("Enter gcode point 2: ")
axis = input("Enter axis to split on: ")
split_val = int(input("Enter number of divisions to make"))

gcode1 = gcode1.split(" ")
gcode2 = gcode2.split(" ")
if axis == "X":
    distance = float(gcode2[1].split("X")[-1]) - float(gcode1[1].split("X")[-1]) 
    pos = float(gcode1[1].split("X")[-1])
elif axis == "Y":
    distance = float(gcode2[2].split("Y")[-1]) - float(gcode1[2].split("Y")[-1]) 
    pos = float(gcode1[2].split("Y")[-1])


new_gcode = []

axis_incr = distance/split_val
new_e_val = float(gcode2[3].split("E")[-1])/split_val

for s in range(split_val+1):
    if axis == "X":
        new_gcode.append(f"{gcode2[0]} X{pos:.2f} {gcode2[2]} E{new_e_val:.2f}")
    elif axis == "Y":
        new_gcode.append(f"{gcode2[0]} {gcode2[1]} Y{pos:.2f} E{new_e_val:.2f}")
    pos += axis_incr


for g in new_gcode:
    print(g)