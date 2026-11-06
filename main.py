from PIL import Image
import numpy as np

def smoothFunc(t):return (6*(t**5))-(15*(t**4))+(10*(t**3))
def noise(x,y,a):return ((1-a)*x)+(a*y)

def fbm (st,x,y,a,O):
    value = 0
    amplitude = 1
    i=0
    while i < O:
        value += amplitude*noise(x,y,a);
        st *= 2
        amplitude *= 0.5
        i+= 1
    return value;

def perlinImageGen(imageSZ,cellCount,name,O):
    grid = 2**cellCount
    gradientVectors = [
        np.array([0,1]),
        np.array([1,0]),
        np.array([0,-1]),
        np.array([-1,0]),
        np.array([np.sqrt(2)/2,np.sqrt(2)/2]),
        np.array([np.sqrt(2)/2,-np.sqrt(2)/2]),
        np.array([-np.sqrt(2)/2,np.sqrt(2)/2]),
        np.array([-np.sqrt(2)/2,-np.sqrt(2)/2])
    ]
    image = Image.new('RGB', (imageSZ,imageSZ), 1)
    image.save('perl.jpg')

    vectors = []
    for i in range(grid+1):
        vectors.append([])
        for j in range(grid+1):
            vectors[i].append(gradientVectors[np.random.randint(8)])
    corners = []
    increment = (1/grid) * (imageSZ - 1)
    for y in range(0,grid+1):
        for x in range(0,grid+1):
            corners.append(np.array([x*increment,y*increment]))

    with Image.open('perl.jpg') as im:
        cellSZ = increment
        for y in range(imageSZ):
            y_CZ = (y%cellSZ)/cellSZ
            for x in range(imageSZ):
                xPos, yPos, x_CZ = int(x/cellSZ),int(y/cellSZ),(x%cellSZ)/cellSZ
                if xPos==grid:xPos = grid-1
                if yPos==grid:yPos = grid-1
                if x==imageSZ-1: x=imageSZ-1.1
                if y==imageSZ-1: y=imageSZ-1.1
                u = np.dot(vectors[yPos][xPos], (x_CZ,y_CZ))
                v = np.dot(vectors[yPos][xPos+1], (x_CZ-1,y_CZ))
                s = np.dot(vectors[yPos+1][xPos], (x_CZ,y_CZ-1))
                t = np.dot(vectors[yPos+1][xPos+1], (x_CZ-1,y_CZ-1))
                st = noise(s,t,smoothFunc(x_CZ))
                uv = noise(u,v,smoothFunc(x_CZ))
                noiseRes = noise(uv,st,smoothFunc(y_CZ))
                noiseRes = fbm(noise(uv,st,smoothFunc(y_CZ)) * 3,uv,st,smoothFunc(y_CZ), O)
                if x==imageSZ-1.1:x=imageSZ-1
                if y==imageSZ-1.1:y=imageSZ-1
                #if (noiseRes)>=0.05:
                #    im.putpixel((int(x),int(y)), (int(125),int(125),int(0)))
                #if (noiseRes)<0.05:
                #    im.putpixel((int(x),int(y)), (int(0),int(0),int(0)))
                im.putpixel((int(x),int(y)), (int(70-255*noiseRes),int(70-255*noiseRes),int(70-255*noiseRes)))
        return im

def perlStack(n,s):
    test=[]
    im0 = perlinImageGen(s,1,'0',1)
    im1 = perlinImageGen(s,2,'1',2)
    im2 = perlinImageGen(s,3,'2',3)
    imRes = Image.open('perl.jpg')
    avrg = []
    for y in range(s):
        for x in range(s):
            try:
                c0 = im0.getpixel((x,y))[0]
                c1 = im1.getpixel((x,y))[0]
                c2 = im2.getpixel((x,y))[0]
            except:
                continue
            average = int((c0+c1+c2)/3)
            avrg.append(average)
            imRes.putpixel((x,y), (average-50,average-50,average-50))

            if average < 255 and average > -10:
                imRes.putpixel((x,y), (255,255,255))
            if average < 255 and average > 0:
                imRes.putpixel((x,y), (58,58,87))
            if average < 255 and average > 15:
                imRes.putpixel((x,y), (0,125,0))
            if average < 170 and average > 70:
                imRes.putpixel((x,y), (183,176,107))
            if average > 80 and average < 200:
                imRes.putpixel((x,y), (0,0,200))
            if average > 100 and average < 255:
                imRes.putpixel((x,y), (0,0,125))
    imRes.save('perl.jpg')

perlStack(3,1024)
