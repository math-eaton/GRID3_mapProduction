#This script will change the fill color to be none and the out
p = arcpy.mp.ArcGISProject('current')
m = p.listMaps('Symbology')[0]
l = m.listLayers('States_SingleSymbol')[0]


l_cim = l.getDefinition('V2')

#Symbol Level 1 (Solid Stroke)
symLvl1 = l_cim.renderer.symbol.symbol.symbolLayers[0]
symLvl1.color.values = [0, 0, 0, 100]
symLvl1.width = 3

if len(symLvl1.effects) == 0:
    dash = arcpy.cim.CreateCIMObjectFromClassName('CIMGeometricEffectDashes', 'V2')
    dash.dashTemplate = [20,30]
#ef1 = symLvl1.effects[0]
#ef1.dashTemplate = [20, 30]

#Symbol Level 2 (Solid Fill)
symLvl2 = l_cim.renderer.symbol.symbol.symbolLayers[1]
symLvl2.color.values = [140, 70, 20, 20]

l.setDefinition(l_cim)
