import fiona
from shapely.geometry import MultiPolygon, shape

def load_cutblock(file: str):
    with fiona.open(file) as shp:
        feature = MultiPolygon([shape(f.get('geometry')) for f in shp])
    return feature