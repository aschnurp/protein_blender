file = open("1mlz.pdb","r")

for line in file:
    if (line.startswith("ENDMDL") or line.startswith("TER")):
        break
    if line.startswith("ATOM"):
        atomname = line[12:16]
        x = float(line[30:38])
        y = float(line[38:46])
        z = float(line[46:54])
        print(atomname, x, y, z)

file.close()

