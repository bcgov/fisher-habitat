import fiona
import json
import geojson
from shapely.geometry import MultiPolygon, shape
import zipfile

def load_cutblock(file: str):
  if zipfile.is_zipfile(file):
    with fiona.open('zip://' + file) as shp:
        feature = MultiPolygon([shape(f.get('geometry')) for f in shp])
    return feature
  else:
    s = json.dumps(file)
    cut_shape = geojson.loads(s)
    print(cut_shape)
    feature = shape(cut_shape)
    return feature.wkt