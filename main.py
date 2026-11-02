from PIL import Image
import numpy as np

def smoothFunc(t):return (6*(t**5))-(15*(t**4))+(10*(t**3))
def noise(x,y,a):return ((1-a)*x)+(a*y)

def perlinImageGen(imageSZ, cellCount):
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
    image.save('test.jpg')

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

    with Image.open('test.jpg') as im:
        cellSZ = increment
        for y in range(imageSZ):
            for x in range(imageSZ):
                xPos, yPos = int(x/cellSZ),int(y/cellSZ)
                if xPos==grid:xPos = grid-1
                if yPos==grid:yPos = grid-1
                if x==255: x=254.9
                if y==255: y=254.9
                u = np.dot(vectors[yPos][xPos], ((x%cellSZ)/cellSZ,(y%cellSZ)/cellSZ))
                v = np.dot(vectors[yPos][xPos+1], ((x%cellSZ)/cellSZ-1,(y%cellSZ)/cellSZ))
                s = np.dot(vectors[yPos+1][xPos], ((x%cellSZ)/cellSZ,(y%cellSZ)/cellSZ-1))
                t = np.dot(vectors[yPos+1][xPos+1], ((x%cellSZ)/cellSZ-1,(y%cellSZ)/cellSZ-1))
                st = noise(s,t,smoothFunc((x%cellSZ)/cellSZ))
                uv = noise(u,v,smoothFunc((x%cellSZ)/cellSZ))
                noiseRes = noise(uv,st,smoothFunc((y%cellSZ)/cellSZ))
                if x==254.9:x=255
                if y==254.9:y=255
                #if (noiseRes)>=0.05:
                #    im.putpixel((int(x),int(y)), (int(125),int(125),int(0)))
                #if (noiseRes)<0.05:
                #    im.putpixel((int(x),int(y)), (int(0),int(0),int(0)))
                im.putpixel((int(x),int(y)), (int(255*noiseRes+30),int(255*noiseRes+30),int(255*noiseRes+30)))
        im.save('test.jpg')

perlinImageGen(256,3)
    

