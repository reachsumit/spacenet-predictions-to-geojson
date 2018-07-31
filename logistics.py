import os
from osgeo import gdal
import subprocess

TIFPATH = "RGB-PanSharpen/"

if not os.path.exists("output"):
    os.mkdir("output")

fname = []
for raster in os.listdir(TIFPATH):
    #print(TIFPATH+os.path.splitext(raster)[0]+".tif")
    srcRaster = gdal.Open(TIFPATH+os.path.splitext(raster)[0]+".tif")
    outputRaster = "output/"+os.path.splitext(raster)[0]+".jpg"
    cmd = ['gdal_translate', '-ot', 'Byte', '-of', 'JPEG', '-co', 'PHOTOMETRIC=rgb']
    scaleList = []
    for bandId in range(srcRaster.RasterCount):
        bandId = bandId+1
        band=srcRaster.GetRasterBand(bandId)
        min = band.GetMinimum()
        max = band.GetMaximum()

        # if not exist minimum and maximum values
        if min is None or max is None:
            (min, max) = band.ComputeRasterMinMax(1)
        cmd.append('-scale_{}'.format(bandId))
        cmd.append('{}'.format(0))
        cmd.append('{}'.format(max))
        cmd.append('{}'.format(0))
        cmd.append('{}'.format(255))

    cmd.append(TIFPATH+os.path.splitext(raster)[0]+".tif")
    cmd.append(outputRaster)
    print(" ".join(cmd))
    subprocess.call(cmd)
    os.remove("output/"+os.path.splitext(raster)[0]+".jpg.aux.xml")
