from collections import namedtuple
from math import sqrt
import random
import time
import urllib
import urllib2
try:
    import Image
except ImportError:
    from PIL import Image

urlForColor = 'http://192.168.0.100:5000/colorchange2/'
red = 0
green = 0
blue = 0

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))


def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(filename, n=1):
    img = Image.open(filename)
    img.thumbnail((10, 10))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters
    
i = 0
while True:
    i += 1
    colore = colorz(str(i)+ "image.jpg")[0]
    print colore
    red_hex = "0x" + str(colore[1:3])
    red = int((int(red_hex,0) / 255.0 )* 394.0)
    
    green_hex = "0x" + str(colore[3:5])
    green = int((int(green_hex,0) / 255.0 ) * 394.0)
    
    blue_hex = "0x" + str(colore[5:7])
    blue =  int((int(blue_hex,0) / 255.0) * 394.0)
    
    print red,green,blue
    indirizzo = urlForColor+str(red+3)+"/"+str(green+3)+"/"+str(blue+3) 
    print indirizzo
    response = urllib2.urlopen(indirizzo)
    #html = response.read()
    time.sleep(3.1)
    if i == 9:
        i = 0