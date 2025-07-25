from turbo_colormap import turbo_colormap_data, interpolate
from colorspacious import cspace_convert
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

def AddLettersToAxis(ax):
    for j, lab in enumerate(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]):
        ax.text((j + 0.5) / 26.0 , .45, lab, ha='center', va='center', size="x-small")

numSamples = 26
plotDataNormal = []
plotDataLight = []
plotDataDark = []
samples = np.linspace(0, 1, num=numSamples)
colors = []
lightnessAccumulated = 0
lightnessMax = -1
for i in samples:
    # colors.append(np.floor(np.array(interpolate(turbo_colormap_data, i))*255))
    newColor = cspace_convert(interpolate(turbo_colormap_data, i), "sRGB1", "CAM02-UCS")
    colors.append(newColor)
    lightnessAccumulated += newColor[0]
    lightnessMax = max(lightnessMax, newColor[0])
lightnessAccumulated /= numSamples

print("Max: " + str(lightnessMax))

LightColors = []
DarkColors = []
OriginalColors = []
for c in colors:
    
    lightnessOriginal = c[0]
    lightnessLight = lerp(lightnessOriginal,lightnessMax,0.80)
    lightnessDark = lightnessLight-5
    
    plotDataNormal.append(lightnessOriginal)
    plotDataLight.append(lightnessLight)
    plotDataDark.append(lightnessDark)
    
    OriginalColors.append(cspace_convert([lightnessOriginal, c[1], c[2]], "CAM02-UCS", "sRGB255").clip(min=0, max=255).astype(int).tolist())
    LightColors.append(cspace_convert([lightnessLight, c[1], c[2]], "CAM02-UCS", "sRGB255").clip(min=0, max=255).astype(int).tolist())
    DarkColors.append(cspace_convert([lightnessDark, c[1], c[2]], "CAM02-UCS", "sRGB255").clip(min=0, max=255).astype(int).tolist())

# print(brightnessAdjustedColors)

# print(f"Brightest: {lightnessMax}")
# print(f"AverageBrightness: {lightnessAccumulated}")
print("Turbo:")
for c in OriginalColors:
    print("<colour r=\"{r}\"     g=\"{g}\"     b=\"{b}\" />".format(r=c[0], g=c[1], b=c[2]))
print("Light:")
for c in LightColors:
    print("<colour r=\"{r}\"     g=\"{g}\"     b=\"{b}\" />".format(r=c[0], g=c[1], b=c[2]))
print("Dark:")
for c in DarkColors:
    print("<colour r=\"{r}\"     g=\"{g}\"     b=\"{b}\" />".format(r=c[0], g=c[1], b=c[2]))


fig, ax = plt.subplots()
plt.plot(samples, plotDataNormal, label='Turbo LUT')
plt.plot(samples, plotDataLight, ls='--', color='#d7d7d7', label='Light Colors')
plt.plot(samples, plotDataDark, ls='--', color='#7b7b7b', label='Dark Colors')
plt.ylim(0,100)
plt.xlim(-0.019,1.019)
plt.xticks([], [])
plt.yticks([20,40,60,80,100])
plt.ylabel('Lightness in CAM02-UCS Color Space')

handles, labels = plt.gca().get_legend_handles_labels()
order = [1,2,0]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc="lower right")

divider = make_axes_locatable(ax)
cax1 = divider.append_axes("bottom", size="5%", pad=0.05)
cax2 = divider.append_axes("bottom", size="5%", pad=0.05)
cax3 = divider.append_axes("bottom", size="5%", pad=0.05)

plt.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1), cmap=mpl.colors.ListedColormap(np.array(LightColors)/255)),
             ax=ax, orientation='horizontal', cax=cax1).set_ticks([])
cax1.text(0, .45, "Light: ", ha='right', va='center', size="small")
plt.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1), cmap=mpl.colors.ListedColormap(np.array(DarkColors)/255)),
             ax=ax, orientation='horizontal', cax=cax2).set_ticks([])
cax2.text(0, .45, "Dark: ", ha='right', va='center', size="small")
plt.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1), cmap=mpl.colors.ListedColormap(np.array(OriginalColors)/255)),
             ax=ax, orientation='horizontal', cax=cax3).set_ticks([])
cax3.text(0, .45, "Turbo: ", ha='right', va='center', size="small")

AddLettersToAxis(cax1)
AddLettersToAxis(cax2)
AddLettersToAxis(cax3)

# plt.savefig("ColorMap.pdf", bbox_inches='tight')
plt.show()
# print(interpolate(turbo_colormap_data, 0.5))
# print()