import os, json
from affine import Affine
from osgeo import gdal
from shapely import geometry

MIN_CONF = 50
adjust_x = 10
adjust_y = 0
TIF_PATH = "/media/sumit/DATA/uChicago/Capstone/dataset/SpaceNet_Buildings_Dataset_v2/AOI_5_Khartoum_Test_public/RGB-PanSharpen/"
CITY = "khartoum"

print("minimum confidence threshold: {}%".format(MIN_CONF))

buildings = []

with open('result.txt', 'r') as outfile:
    image = ""
    # read line by line
    for line in outfile:
        if line.startswith("Enter Image Path:"):
            image = line.split()[3].split("/")[-1][:-5]+".tif"
        elif line.startswith("building"):
            confidence = int(line.split()[1][:-1])
            if confidence < MIN_CONF:
                continue
            x_top_left = int(line.split()[3])
            y_top_left = int(line.split()[5])
            width = int(line.split()[7])
            height = int(line.split()[9][:-1])
            #print(line.split())
            #print(confidence, x_top_left, y_top_left, width, height)
            raster = TIF_PATH+image
            #print(image)
            ds = gdal.Open(raster, gdal.GA_ReadOnly)
            gt = ds.GetGeoTransform()
            #print(ds.RasterXSize)
            #print(ds.RasterYSize)
            ds = None  # close
            col1 = x_top_left + adjust_x
            row1 = y_top_left + adjust_y
            col2 = (x_top_left+width) + adjust_x
            row2 = (y_top_left+height) + adjust_y
            p1 = [(col1 * gt[1]) + gt[0], (row1 * gt[5]) + gt[3]]
            p2 = [(col2 * gt[1]) + gt[0], (row1 * gt[5]) + gt[3]]
            p3 = [(col2 * gt[1]) + gt[0], (row2 * gt[5]) + gt[3]]
            p4 = [(col1 * gt[1]) + gt[0], (row2 * gt[5]) + gt[3]]
            p5 = [(col1 * gt[1]) + gt[0], (row1 * gt[5]) + gt[3]]
            poly = geometry.Polygon([p1, p2, p3, p4, p5])
            buildings.append({"type":"Feature", 'geometry':geometry.mapping(poly), \
                              'properties':{'Name': 'Building'}})
        else:
            continue

if not os.path.exists(CITY+"_test"):
    os.mkdir(CITY+"_test")

for i in range(0,int(len(buildings)/1000)):
    my_geo = {'type':'FeatureCollection', "crs": { "type": "name", \
                                              "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, \
                                              "features":buildings[i*1000:(i+1)*1000-1]}
    filename = "buildings"+str((i+1)*1000-1)+'.geojson'
    print(i*1000, (i+1)*1000-1, filename)
    with open(CITY+"_test/"+filename, 'w') as outfile:
        json.dump(my_geo, outfile)
        
my_geo = {'type':'FeatureCollection', "crs": { "type": "name", \
                                              "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, \
                                              "features":buildings[i*1000:]}
filename = "buildings"+str(len(buildings)-1)+'.geojson'
print((i+1)*1000, len(buildings)-1, filename)
with open(CITY+"_test/"+filename, 'w') as outfile:
    json.dump(my_geo, outfile)
