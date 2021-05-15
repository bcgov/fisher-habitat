import fiona
import fiona.crs
import geojson
import pyproj
import zipfile
import functools
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform


omit = ['SHAPE_AREA', 'SHAPE_LEN']

def convert_shape_file_zip_to_geojson(file):
    with fiona.open('zip://' + file) as source:
        project = functools.partial(pyproj.transform,
                                    pyproj.Proj(**source.crs),
                                    pyproj.Proj(init='EPSG:4326'))

        features = []
        for f in source:
            s = shape(f['geometry'])
            projected_shape = transform(project, s)

            props = f['properties']
            for k in omit:
                if k in props:
                    del props[k]

            feature = geojson.Feature(id=f['id'],
                                      geometry=projected_shape, 
                                      properties=props)
            features.append(feature)

    feature_collection = geojson.FeatureCollection(features)
    return feature_collection


def load_cutblock(file: str):
  if zipfile.is_zipfile(file):
    cutblock_geojson = convert_shape_file_zip_to_geojson(file)
    with fiona.open('zip://' + file) as shp:
        feature = MultiPolygon([shape(f.get('geometry')) for f in shp])
    return feature, cutblock_geojson
  else:
    cutblock_geojson = geojson.loads(file)
    poly = MultiPolygon([shape(p.geometry) for p in cutblock_geojson.features ])

    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:3005')

    project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
    feature = transform(project, poly)

    return feature, cutblock_geojson
