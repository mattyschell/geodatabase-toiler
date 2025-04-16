import arcpy

# UPDATE THESE 
# We saw curves returning to geometries like bad penny
# This was due to not managing SE_ANNO_CAD_DATA when peforming 
#    arc densification with SDO SQL. aka my bad
sdefile = """C:/gis/connections/oracle19c/dev/GIS-ditGSdv1/bldg.sde"""
fc_name = 'KAMYACHRISTMAS'

#c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe esri-case-03790185.py

def execute_immediate(sde,
                      sql):

    try:

        sde_conn = arcpy.ArcSDESQLExecute(sde)

    except:

        print (arcpy.GetMessages())
        raise

    try:

        sde_return = sde_conn.execute(sql)

    except Exception as err:

        print (f"sql fail on {sql}") 
        raise ValueError(err)

    del sde_conn
    return sde_return



fc_path = '{0}/{1}'.format(sdefile
                          ,fc_name)

spatial_ref = arcpy.SpatialReference(2263)
config_key  = 'SDO_GEOMETRY'

arcpy.env.workspace = sdefile

try:
    arcpy.Delete_management(fc_path)
except:
    print("doesnt exist or forgot to remove from ArcGIS Pro Table of Contents")
    pass

arcpy.management.CreateFeatureclass(out_path=sdefile
                                   ,out_name=fc_name
                                   ,geometry_type='POLYGON'
                                   ,spatial_reference=spatial_ref
                                   ,config_keyword=config_key)

sql = """insert into kamyachristmas (objectid, shape) values (1,SDO_GEOMETRY
(
   2003,
   2263,
   NULL,
   SDO_ELEM_INFO_ARRAY
   (
      1,
      1003,
      1
   ),
   SDO_ORDINATE_ARRAY
   (
      1022197.32501198,
      244619.019341797,
      1022195.25484188,
      244618.691434871,
      1022193.38732193,
      244617.73985911,
      1022191.90525799,
      244616.25776138,
      1022190.95372481,
      244614.390219733,
      1022190.62586509,
      244612.320042157,
      1022190.95377202,
      244610.249872057,
      1022191.90534778,
      244608.382352106,
      1022193.38744551,
      244606.900288169,
      1022195.25498715,
      244605.94875499,
      1022197.32516473,
      244605.620895266,
      1022199.39533483,
      244605.948802192,
      1022201.26285478,
      244606.900377953,
      1022202.74491872,
      244608.382475683,
      1022203.6964519,
      244610.25001733,
      1022204.02431162,
      244612.320194906,
      1022203.69640469,
      244614.390365006,
      1022202.74482893,
      244616.257884957,
      1022201.2627312,
      244617.739948894,
      1022199.39518956,
      244618.691482073,
      1022197.32501198,
      244619.019341797
   )
))"""

sdereturn = execute_immediate(sdefile,
                              sql)

result = arcpy.management.CheckGeometry(fc_path)
if result[1] == 'true':
    print(result.getMessages())
else:
    print("No problems Found")


 
