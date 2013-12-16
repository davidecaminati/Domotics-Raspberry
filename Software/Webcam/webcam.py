import pygame.camera
import pygame.image
import time
from collections import namedtuple
from math import sqrt
import random
import urllib
import urllib2
try:
    import Image
except ImportError:
    from PIL import Image

red = 0
green = 0
blue = 0   
pygame.camera.init()
#cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
#cam.start()
#img = cam.get_image()
#pygame.image.save(img, "image.jpg")
#pygame.camera.quit()
print "1"

urlForColor = 'http://192.168.0.100:5000/colorchange2/'

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
    img.thumbnail((50, 50))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

    
def colorzimg(img, n=1):
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


def aggiustacolore(colore10,colore20,r,g,b):

    
    red_hex10 = "0x" + str(colore10[1:3])
    red10 = int((int(red_hex10,0) / 255.0 )* 394.0)
    
    green_hex10 = "0x" + str(colore10[3:5])
    green10 = int((int(green_hex10,0) / 255.0 ) * 394.0)
    
    blue_hex10 = "0x" + str(colore10[5:7])
    blue10 =  int((int(blue_hex10,0) / 255.0) * 394.0)
    
    
    red_hex20 = "0x" + str(colore20[1:3])
    red20 = int((int(red_hex20,0) / 255.0 )* 394.0)
    
    green_hex20 = "0x" + str(colore20[3:5])
    green20 = int((int(green_hex20,0) / 255.0 ) * 394.0)
    
    blue_hex20 = "0x" + str(colore20[5:7])
    blue20 =  int((int(blue_hex20,0) / 255.0) * 394.0)
    print "red10 %s " % red10
    print "red20 %s " % red20
    print "--"
    print "green10 %s " % green10
    print "green20 %s " % green20
    print "--"
    print "blue10 %s " % blue10
    print "blue20 %s " % blue20
    print "--"
    if red10 > red20 and r < 390 :
        print "red +5"
        r += 5
    else:
    
        if  r > 8:
            print "red -5"
            r -= 5
        
    if green10 > green20 and g < 390 :
        print "green +5"
        g += 5
    else:
        if  g > 8:
            print "green -5"
            g -= 5
        
    if blue10 > blue20 and b < 390 :
        print "blue +5"
        b += 5
    else:
        if  b > 8:
            print "blue -5"
            b -= 5
        
        
    indirizzo = urlForColor+str(r)+"/"+str(g)+"/"+str(b) 
    #print indirizzo
    response = urllib2.urlopen(indirizzo)
    
    return r,g,b
    
    
#i = 0
#while True:
#i += 1
colore = colorz("image.jpg")[0]
#print colore
red_hex = "0x" + str(colore[1:3])
red = int((int(red_hex,0) / 255.0 )* 394.0)

green_hex = "0x" + str(colore[3:5])
green = int((int(green_hex,0) / 255.0 ) * 394.0)

blue_hex = "0x" + str(colore[5:7])
blue =  int((int(blue_hex,0) / 255.0) * 394.0)

#print red,green,blue
indirizzo = urlForColor+str(red)+"/"+str(green)+"/"+str(blue) 
print indirizzo
response = urllib2.urlopen(indirizzo)
#html = response.read()
print "inizio loop fase 2"
time.sleep(1)
#pygame.camera.init()
cam2 = pygame.camera.Camera(pygame.camera.list_cameras()[1])
cam2.start()
r = 150
g = 150
b = 150
for i in range(1,200):
    srf = cam2.get_image()
    #pygame.image.save(img2, str(i) + "image.bmp")
    
    img2 = pygame.image.tostring(srf, 'RGB')
    img2 = Image.fromstring('RGB', srf.get_size(), img2)
    pygame.camera.quit()
    
    print "colore rilevato fase 1"
    print colore
    #time.sleep(1)
    colore2 = colorzimg(img2)[0]
    print "colore rilevato fase 2"
    print colore2
    #red_hex2 = "0x" + str(colore2[1:3])
    #red2 = int((int(red_hex2,0) / 255.0 )* 394.0)
    
    #green_hex2 = "0x" + str(colore2[3:5])
    #green2 = int((int(green_hex2,0) / 255.0 ) * 394.0)
    
    #blue_hex2 = "0x" + str(colore2[5:7])
    #blue2 =  int((int(blue_hex2,0) / 255.0) * 394.0)
    #print red2,green2,blue2
    #print "fine"
    #if i == 9:
    #    i = 0
    
    r,g,b = aggiustacolore(colore,colore2,r,g,b)
    print r
    print g
    print b
    
    
