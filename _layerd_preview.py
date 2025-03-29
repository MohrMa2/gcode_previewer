import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parse_gcode_by_layer(file_path):
    layers = {}
    current_z = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("G1"):  # Beinhaltet Bewegungsbefehle
                parts = line.split()
                x, y, z = None, None, None
                for part in parts:
                    if part.startswith("X"):
                        x = float(part[1:])
                    if part.startswith("Y"):
                        y = float(part[1:])
                    if part.startswith("Z"):
                        z = float(part[1:])
                if z is not None:
                    current_z = z  # Wechsel der Ebene
                if x is not None and y is not None:
                    if current_z not in layers:
                        layers[current_z] = []
                    layers[current_z].append((x, y, current_z))
    return layers

def gcode_to_layered_3d_jpeg(gcode_path, output_path):
    layers = parse_gcode_by_layer(gcode_path)
    if not layers:
        print("Keine gültigen Layer gefunden.")
        return

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Jede Ebene in einer anderen Farbe plotten
    colors = plt.cm.get_cmap('viridis', len(layers))
    for idx, (z, coordinates) in enumerate(sorted(layers.items())):
        x_coords, y_coords, z_coords = zip(*coordinates)
        ax.plot(x_coords, y_coords, z_coords, marker='o', label=f"Layer Z={z}", color=colors(idx))

    ax.set_title("G-Code Darstellung mit Layer-Wechseln")
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")
    ax.set_zlabel("Z-Achse")
    ax.view_init(elev=30, azim=45)  # Schräger Blickwinkel

    plt.legend()
    plt.savefig(output_path, format='jpeg')
    plt.close()

# Beispiel:
# Pfade für Eingabe-G-Code-Datei und Ausgabe-Bild anpassen
gcode_file = sys.argv[1] #"pfad_zur_gcode_datei.nc"
jpeg_output = sys.argv[1]+".jpg" # "3d_ausgabebild.jpeg"

gcode_to_layered_3d_jpeg(gcode_file, jpeg_output)
print(f"Layered 3D-JPEG wurde gespeichert unter: {jpeg_output}")

