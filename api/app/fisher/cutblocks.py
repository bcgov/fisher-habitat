import fiona
import json
import geojson
from shapely.geometry import MultiPolygon, shape
from shapely.ops import transform
import pyproj
import zipfile

def load_cutblock(fc: str):
    feature_collection = geojson.loads(fc)
    poly = MultiPolygon([shape(p.geometry) for p in feature_collection.features ])

    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:3005')

    project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
    feature = transform(project, poly)

    return feature


def load_cutblock_file(file: bytes):
    with fiona.BytesCollection(file) as shp:
        feature = MultiPolygon([shape(f.get('geometry')) for f in shp])
    return feature


"""
insert into fisher_poly(harvest_im, geom)
SELECT harvest_im,
       ST_Multi(ST_Union(ST_MakeValid(geom))) AS geom
FROM   (
  SELECT harvest_im,
         geom,
         ST_ClusterDBSCAN(geom, .01, 1) OVER(PARTITION BY harvest_im) AS _clst
  FROM   fisher_fhe
) q
WHERE  _clst IS NOT NULL
GROUP BY
       harvest_im, _clst
;
"""
