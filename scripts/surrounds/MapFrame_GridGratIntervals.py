# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script will change the grid/graticule interval and symbology.
# Notes:   The script is intended to work from a script tool provided with
#          a sample project using "CURRENT".  To see the changes happen be
#          sure to active the appropriate map or layout.

p = arcpy.mp.ArcGISProject('current')
lyt = p.listLayouts('GreatLakes')[0]

cim_lyt = lyt.getDefinition('V2')     #Get the layout's CIM definition

#Iterate though all layout elements to find the MapFrame element
for elm in cim_lyt.elements:
  if elm.name == 'Great Lakes MF':
    for grd in elm.grids:
        if grd.name == 'Black Horizontal Label Graticule':
          grd.isAutoScaled = False    #MUST turn off the auto interval option

          #iterate through the differnt grid/grat components
          for grdLn in grd.gridLines:
            if grdLn.name == "Gridlines": 
              grdLnPat = grdLn.pattern
              grdLnPat.interval = 2   #Change the interval

              #Modify the symbology for gridlines
              if grdLn.gridLineOrientation == "EastWest":   #Make red
                grdLn.symbol.symbol.symbolLayers[0].color.values = [255,0,0,100]
              if grdLn.gridLineOrientation == "NorthSouth": #Make blue
                grdLn.symbol.symbol.symbolLayers[0].color.values = [0,0,255,100]   

            #Modify the symbology for the text
            if grdLn.name == "Labels":
              grdLn.fromTick.gridEndpoint.gridLabelTemplate.symbol.symbol.symbol.symbolLayers[0].color.values = [255,0,0,100]
              grdLn.toTick.gridEndpoint.gridLabelTemplate.symbol.symbol.symbol.symbolLayers[0].color.values = [0,0,255,100]

lyt.setDefinition(cim_lyt)            #Set the layout's CIM definition
