#Code qui prend une image en argument et qui trouve le pas de l'hélice associé à la couleur 
# (supposant bien sur que c'est un cristal liquide)

from PIL import Image
import numpy as np
import math


#fonction qui renvoie RGB, XYZ et (x,y) d'une image sous forme de p-uplet
def tout(filename):

    #conversion en RGB moyen
    def conversionRGB(file):

        image = Image.open(file)
        image_numpy = np.array(image)
        raw_rgb = image_numpy.mean(axis=(0, 1))

        RGB = [round(float(value), 2) for value in raw_rgb]
        #RGB = [round((float(raw_rgb[0])/255), 2), round((float(raw_rgb[0])/255), 2), round((float(raw_rgb[0])/255), 2)]

        return RGB

    #variables des matrices
    rgb = conversionRGB(filename)
    rgb_pour_conversion = [round(value/255, 3) for value in rgb]
    M_sRGB = [[0.4124, 0.3576, 0.1805],
              [0.2126, 0.7152, 0.0722],
              [0.0193, 0.1192, 0.9505]]
    M_CIERGB = [[0.49, 0.31, 0.2],
                [0.17697, 0.8134, 0.010630],
                [0, 0.01, 0.99]]

    #conversion RGB vers XYZ
    def conversionXYZ(valeursrgb):

        XYZ = [0, 0, 0]

        for j in range(3):
            for i in range(3):
                XYZ[j] += valeursrgb[i]*M_CIERGB[j][i]
            XYZ[j] = round(XYZ[j], 2)

        return XYZ

    xyz = conversionXYZ(rgb_pour_conversion)

    #conversion XYZ vers (x, y)
    x = round((xyz[0]/(xyz[0]+xyz[1]+xyz[2])), 4)
    y = round((xyz[1]/(xyz[0]+xyz[1]+xyz[2])), 4)
    coordonnees = (x, y)

    return rgb, xyz, coordonnees

def rgblongeurdonde(a, b, c):

    #conversion RGB vers XYZ
    def conversionXYZ(a, b, c):

        XYZ = [0, 0, 0]
        valeursrgb = [a, b, c]

        M_CIERGB = [[0.49, 0.31, 0.2],
                    [0.17697, 0.8134, 0.010630],
                    [0, 0.01, 0.99]]

        for j in range(3):
            for i in range(3):
                XYZ[j] += valeursrgb[i]*M_CIERGB[j][i]
            XYZ[j] = round(XYZ[j], 2)

        return XYZ
    XYZ = conversionXYZ(a, b, c)

    #conversion XYZ vers (x, y)
    x = round((XYZ[0]/(XYZ[0]+XYZ[1]+XYZ[2])), 4)
    y = round((XYZ[1]/(XYZ[0]+XYZ[1]+XYZ[2])), 4)
    coordonnees = (x, y)

    return coordonnees

dico = {380: (0.17, 0.01), 390: (0.166, 0.052), 400: (0.162, 0.095),
        410: (0.158, 0.138), 420: (0.154, 0.18), 430: (0.15, 0.223),
        440: (0.147, 0.265), 450: (0.144, 0.307), 460: (0.14, 0.35),
        470: (0.13, 0.06), 480: (0.09, 0.14), 490: (0.05, 0.3),
        500: (0.01, 0.54), 510: (0.04, 0.685), 520: (0.07, 0.83),
        530: (0.15, 0.79), 540: (0.23, 0.75), 550: (0.3, 0.69),
        560: (0.37, 0.63), 570: (0.44, 0.56), 580: (0.51, 0.49),
        590: (0.57, 0.43), 600: (0.63, 0.37), 610: (0.66, 0.34),
        620: (0.69, 0.31), 630: (0.696, 0.304), 640: (0.702, 0.298),
        650: (0.708, 0.292), 660: (0.714, 0.286), 670: (0.72, 0.279),
        680: (0.727, 0.273), 690: (0.734, 0.267), 700: (0.74, 0.26)}


# Fonction de distance Euclidienne
def distance_euclidienne(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Algorithme de Nearest Neighbor Search
def algo_NNS(x, y, helices):
    min_distance = float('inf')  # Initialisation à l'infini pour comparer
    nearest_step = None

    for step, (hx, hy) in helices.items():
        # Calcul de la distance Euclidienne entre le point donné (x, y) et chaque point dans le dictionnaire
        distance = distance_euclidienne((x, y), (hx, hy))

        # Si la distance est plus petite, on met à jour la plus petite distance et le pas associé
        if distance < min_distance:
            min_distance = distance
            nearest_step = step

    return nearest_step

# Exemple d'utilisation

# Dictionnaire avec les pas de l'hélice et les coordonnées associées
helices = {380: (0.17, 0.01), 390: (0.166, 0.052), 400: (0.162, 0.095),
        410: (0.158, 0.138), 420: (0.154, 0.18), 430: (0.15, 0.223),
        440: (0.147, 0.265), 450: (0.144, 0.307), 460: (0.14, 0.35),
        470: (0.13, 0.06), 480: (0.09, 0.14), 490: (0.05, 0.3),
        500: (0.01, 0.54), 510: (0.04, 0.685), 520: (0.07, 0.83),
        530: (0.15, 0.79), 540: (0.23, 0.75), 550: (0.3, 0.69),
        560: (0.37, 0.63), 570: (0.44, 0.56), 580: (0.51, 0.49),
        590: (0.57, 0.43), 600: (0.63, 0.37), 610: (0.66, 0.34),
        620: (0.69, 0.31), 630: (0.696, 0.304), 640: (0.702, 0.298),
        650: (0.708, 0.292), 660: (0.714, 0.286), 670: (0.72, 0.279),
        680: (0.727, 0.273), 690: (0.734, 0.267), 700: (0.74, 0.26)}

# Point (x, y) à tester
filename = "images/beau-orange-codepython.jpeg"
x = tout(filename)[2][0]
y = tout(filename)[2][1]

# Appel de la fonction pour trouver le pas le plus proche
nearest_step = algo_NNS(x, y, helices)

# Affichage du résultat
print(f"La longueur d'onde la plus proche de ({x}, {y}) est {nearest_step}.")
print((round(nearest_step/(2*1.5*math.sin(90)), 2), "nm"))

print(nearest_step,(round(nearest_step/(2*1.5*math.sin(90)), 2)))
