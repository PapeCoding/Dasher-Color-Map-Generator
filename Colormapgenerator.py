import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from colorspacious import cspace_convert
import pandas as pd

# configuration
numColors = 26
usedColorMap = "turbo" # See https://matplotlib.org/stable/users/explain/colors/colormaps.html

# sample colormap
samples = np.linspace(0, 1, numColors)
data = pd.DataFrame(columns=["ColorUCS", "ColorLight", "ColorDark", "ColorOriginal", "LightnessOriginal", "LightnessLight", "LightnessDark"])
for color in mpl.colormaps["turbo"](samples):
    newColor = cspace_convert(color[0:3], "sRGB1", "CAM02-UCS")
    data.loc[len(data), ["ColorUCS", "LightnessOriginal"]] = [newColor, newColor[0]]

# Compute derived colors
data["LightnessLight"] = 0.2 * data["LightnessOriginal"] + 0.8 * data["LightnessOriginal"].max()
data["LightnessDark"] = data["LightnessLight"] - 5
data["ColorOriginal"] = data.apply(lambda x: cspace_convert([x["LightnessOriginal"], x["ColorUCS"][1], x["ColorUCS"][2]], "CAM02-UCS", "sRGB255").clip(min=0, max=255).astype(int).tolist(), axis=1)
data["ColorLight"] = data.apply(lambda x: cspace_convert([x["LightnessLight"], x["ColorUCS"][1], x["ColorUCS"][2]], "CAM02-UCS", "sRGB255").clip(min=0, max=255).astype(int).tolist(), axis=1)
data["ColorDark"] = data.apply(lambda x: cspace_convert([x["LightnessDark"], x["ColorUCS"][1], x["ColorUCS"][2]], "CAM02-UCS", "sRGB255").clip(min=0, max=255).astype(int).tolist(), axis=1)

# Create base plot
fig, ax = plt.subplots()
plt.plot(samples, data["LightnessOriginal"], label='Turbo LUT')
plt.plot(samples, data["LightnessLight"], ls='--', color='#d7d7d7', label='Light Colors')
plt.plot(samples, data["LightnessDark"], ls='--', color='#7b7b7b', label='Dark Colors')
plt.ylim(0,100)
plt.xlim(-0.019,1.019)
plt.xticks([], [])
plt.yticks([20,40,60,80,100])
plt.ylabel('Lightness in CAM02-UCS Color Space')

# reorder labels
handles, labels = plt.gca().get_legend_handles_labels()
order = [1,2,0]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc="lower right")

# color bars below
def AddLettersToAxis(ax):
    for j, lab in enumerate(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]):
        ax.text((j + 0.5) / numColors , .45, lab, ha='center', va='center', size="x-small")

divider = make_axes_locatable(ax)
for [label, data] in [["Light: ", "ColorLight"],["Dark: ", "ColorDark"],["Turbo: ", "ColorOriginal"]]:
    cax = divider.append_axes("bottom", size="5%", pad=0.05)
    plt.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1), cmap=mpl.colors.ListedColormap(np.vstack(data[data])/255)),
                ax=ax, orientation='horizontal', cax=cax).set_ticks([])
    cax.text(0, .45, label, ha='right', va='center', size="small")
    AddLettersToAxis(cax)

# plt.savefig("ColorMap.pdf", bbox_inches='tight')
plt.show()

# print resulting colorscheme:
print("Max: " + str(data["LightnessOriginal"].max()))
output = ""
for row in data["ColorOriginal"]:
    output += f"#{row[0]:02x}{row[1]:02x}{row[2]:02x},"
print("Turbo: " + output[:-1])

output = ""
for row in data["ColorLight"]:
    output += f"#{row[0]:02x}{row[1]:02x}{row[2]:02x},"
print("Light: " + output[:-1])

output = ""
for row in data["ColorDark"]:
    output += f"#{row[0]:02x}{row[1]:02x}{row[2]:02x},"
print("Dark: " + output[:-1])