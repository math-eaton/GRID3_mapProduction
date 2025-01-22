# Author:  Esri
# Date:    March 2020
# Version: ArcGISPro 2.5
# Purpose: This script alters a Layer's patch shape and then a Legend's
#          patch sizes and legend item properties.
# Notes:   - The script is intended to work from a script tool provided with
#            a sample project using "CURRENT".  To see the changes happen be
#            sure to active the appropriate map or layout.
#          - Changing a layer's patch shape will also affect a legend that
#            displays the layer.

p = arcpy.mp.ArcGISProject('current')


#Change a layer's patch shape
m = p.listMaps('GreatLakes')[0]

#Iterate through each layer 
for lyr in m.listLayers():            #Get the layer's CIM definition
  lyr_cim = lyr.getDefinition('V2')

  if lyr.name == "GreatLakes":
    lyr_cim.renderer.patch = "AreaHydroPoly"  #Change patch for single symbol

  if lyr.name == "States" or lyr.name == 'Provinces':
    for grp in lyr_cim.renderer.groups:       #Iterate through each group
      for cls in grp.classes:                 #Iterate through each class
        cls.patch = "AreaBoundary"            #Change patch for each class in group
      
  lyr.setDefinition(lyr_cim)          #Set the layer's CIM definition


#Change layout legend item properties
lyt = p.listLayouts('GreatLakes')[0]
lyt_cim = lyt.getDefinition('V2')     #Get the layout's CIM definition

#Iterate though all layout elements to find the Legend element
for elm in lyt_cim.elements:
  if elm.name == "Legend":

    #Legend item changes
    for itm in reversed(elm.items):
      itm.patchWidth = 25
      itm.patchHeight = 15
      
      if itm.name == "States" or itm.name == "Provinces":
        nn = itm
        #Update visibility
        itm.autoVisibility = True       #Display items in visible extent 
        itm.showGroupLayerName = False
        itm.showLayerName = True
        itm.showHeading = False
        itm.keepTogether = False        #Keep in single column
        itm.classIndent = 10

        #Update layer name symbol
        itm.layerNameSymbol.symbol.symbol.symbolLayers[0].color.values = [255,0,0,100]
    
lyt.setDefinition(lyt_cim)            #Set the layout's CIM definition
