import fiona
from shapely.geometry import MultiPolygon, shape
import zipfile

def load_cutblock(file: str):
  if zipfile.is_zipfile(file):
    with fiona.open('zip://' + file) as shp:
        feature = MultiPolygon([shape(f.get('geometry')) for f in shp])
    return feature
  else:
    with fiona.open(file) as shp:
        feature = MultiPolygon([shape(f.get('geometry')) for f in shp])
    return feature