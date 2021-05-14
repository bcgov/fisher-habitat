import fiona
import json
import geojson
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform
import pyproj
import zipfile

def load_cutblock(file: str):
  if zipfile.is_zipfile(file):
    with fiona.open('zip://' + file) as shp:
        feature = MultiPolygon([shape(f.get('geometry')) for f in shp])
    return feature
  else:
    feature_collection = geojson.loads(file)
    poly = MultiPolygon([shape(p.geometry) for p in feature_collection.features ])

    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:3005')

    project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
    feature = transform(project, poly)

    return feature