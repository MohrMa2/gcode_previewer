import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

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

def set_axes_equal(ax):
    """ Setzt die Skalierung der Achsen auf gleich, damit X, Y und Z maßstabsgetreu sind. """
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])

    max_range = max(x_range, y_range, z_range)

    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)

    ax.set_xlim3d([x_middle - max_range / 2, x_middle + max_range / 2])
    ax.set_ylim3d([y_middle - max_range / 2, y_middle + max_range / 2])
    ax.set_zlim3d([z_middle - max_range / 2, z_middle + max_range / 2])

def gcode_to_scaled_3d_jpeg(gcode_path, output_path):
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

    ax.set_title(gcode_path)
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")
    ax.set_zlabel("Z-Achse")
    ax.view_init(elev=30, azim=45)  # Schräger Blickwinkel

    # Maßstabsgetreue Achsen setzen
    set_axes_equal(ax)

#    plt.legend()
    plt.savefig(output_path, format='jpeg')
    plt.close()

# Beispiel:
# Pfade für Eingabe-G-Code-Datei und Ausgabe-Bild anpassen
gcode_file = sys.argv[1] #"pfad_zur_gcode_datei.nc"
jpeg_output = sys.argv[1]+".jpg" # "3d_ausgabebild.jpeg"

gcode_to_scaled_3d_jpeg(gcode_file, jpeg_output)
print(f"Scaled 3D-JPEG wurde gespeichert unter: {jpeg_output}")

