import arcpy
from arcpy import env  
from arcpy.sa import *
def buildRangeMap(low, high):
    diff = high - low
    interval = diff / 10
    curr = low
    L = []
    for i in range(0, 10):
        L.append([low +(interval*i), low+(interval * (i + 1)), i + 1])
    return L
def reclassifyRasters(rasters, weight):
    times_rasters = []
    for i in range(len(rasters)):
        raster = arcpy.Raster(rasters[i])
        outReclass= Reclassify(raster, "Value", RemapRange(buildRangeMap(raster.minimum, raster.maximum)))
        outReclass.save("C:\\Users\\Juno\\Downloads\\GGR321 Group Project\\ToolOutput\\reclass_{}.tif".format(rasters[i]))
        timesRaster = arcpy.sa.Times(weight, outReclass)
        times_rasters.append(timesRaster)
    return times_rasters
def makeCostRaster(times_rasters):
    for i in range(1, len(times_rasters)):
        sumRaster = arcpy.sa.Plus(times_rasters[0], times_rasters[i])
    return sumRaster
    
def ScriptTool(param0, Start, End, walkRaster):
    times_rasters = reclassifyRasters(param0, 0.75 / len(param0))
    sumRaster = makeCostRaster(times_rasters)
    
    finalRaster = arcpy.sa.Plus(walkRaster, sumRaster)
    finalRaster.save("C:\\Users\\Juno\\Downloads\\GGR321 Group Project\\ToolOutput\\finalCost.tif")
    
    LeastPath = "C:\\Users\\Juno\\Downloads\\GGR321 Group Project\\ToolOutput\\SafestPath.gdb\\SafestPath"
    LeastCostPath = arcpy.intelligence.LeastCostPath(finalRaster, Start, End, LeastPath)
    
    return
# This is used to execute code if the file was run but not imported
if __name__ == '__main__':
    # Tool parameter accessed with GetParameter or GetParameterAsText
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = "C:\\Users\\Juno\\Downloads\\GGR321 Group Project\\ToolOutput\\"
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    param2 = arcpy.GetParameterAsText(2)
    param3 = arcpy.GetParameterAsText(3)
    L = param0.split(";")
    ScriptTool(L, param1, param2, param3)
    
    # Update derived parameter values using arcpy.SetParameter() or arcpy.SetParameterAsText()
