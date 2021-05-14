"""
Map layers (layers module) API endpoints/handlers.
"""
import random
import logging
from fastapi import FastAPI, HTTPException, APIRouter, BackgroundTasks, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.db.utils import get_db
from app.fisher.cutblocks import load_cutblock
from app.config import DATABASE_URI
from fastapi.encoders import jsonable_encoder
import os 

router = APIRouter()
logger = logging.getLogger('api')

def bgtask():
    time.sleep(1)

@router.get('/hello/{hi}')
def hello_world(hi: str):
    """ function goes here """
    return hi

@router.get('/background')
def background(background_tasks: BackgroundTasks):
    background_tasks.add_task(bgtask)
    return {"message": "added background task"}


@router.get('/dbexample')
def dbexample(db: Session = Depends(get_db)):
    """ function goes here """

    q = """
    select 42
    """

    result = db.execute(q)
    result = result.fetchone()[0]

    return result

def habitat_in_polygon(cutblock, db):
    """
    returns statistics about Fisher habitat within a cutblock polygon.
    Cutblock must be in BC Albers EPSG:3005.

    The density of landscape features that Fishers rely on are retrieved
    from polygons from the `fisher_fhe` table.  The density is converted
    to a count by multiplying by the intersecting area of every fisher_fhe
    polygon and the cutblock polygon.

    Polygons with different types of warnings are also returned as `yellow_polygons`
    and `red_polygons`.

    Fields that contain "density" are in units/hectare (hectare = 10000 sq m).
    """

    q = """
    with cutblock as (
        select ST_SetSRID(ST_GeomFromText(:cutblock), 3005) as geom
    ),
    fisher_habitats as (
        select  ogc_fid as id,
                ST_Transform(ST_Intersection(ST_Transform(f.geom, 3005), c.geom), 4326) as geom,
                ST_Area(ST_Intersection(ST_Transform(f.geom, 3005), c.geom)) / 10000 as area_ha,
                fisher_hab,
                harvest_im,
                coalesce(denning_wa, 0) as denning_wa,
                coalesce(denning_pr, 0) as denning_pr,
                coalesce(branch_res, 0) as branch_res,
                coalesce(branch_r_1, 0) as branch_r_1,
                coalesce(cavity_res, 0) as cavity_res,
                coalesce(cavity_r_1, 0) as cavity_r_1,
                coalesce(cwd_restin, 0) as cwd_restin,
                coalesce(cwd_rest_1, 0) as cwd_rest_1
        from    fisher_fhe f
        inner join cutblock c on ST_Intersects(ST_Transform(c.geom, 4326), f.geom)
    )
    select
        sum(denning_wa) as sum_denning_warning,
        ROUND(sum(denning_pr * area_ha)) as sum_denning_primary,
        ROUND(sum(denning_pr * area_ha * 4)) as sum_denning_contingency,
        ROUND(sum((denning_pr * area_ha) / (select ST_Area(geom)/10000 from cutblock))::numeric, 1) as denning_primary_density_cutblock,
        sum(branch_res) as sum_branch_resting_warning,
        ROUND(sum(branch_r_1  * area_ha)) as sum_branch_resting_primary,
        ROUND(sum(branch_r_1  * area_ha * 4)) as sum_branch_resting_contingency,
        ROUND(sum((branch_r_1  * area_ha) / (select ST_Area(geom)/10000 from cutblock))::numeric, 1) as branch_resting_primary_density_cutblock,
        sum(cavity_res) as sum_cavity_resting_warning,
        ROUND(sum(cavity_r_1 * area_ha)) as sum_cavity_resting_primary,
        ROUND(sum(cavity_r_1 * area_ha)) as sum_cavity_resting_primary,
        ROUND(sum((cavity_r_1 * area_ha) / (select ST_Area(geom)/10000 from cutblock))::numeric, 1) as cavity_resting_primary_density_cutblock,
        ROUND(sum(cwd_restin * area_ha)) as sum_resting_piece,
        ROUND(sum(cwd_rest_1 * area_ha)) as sum_resting_piles,
        ROUND(sum((cwd_restin * area_ha) / (select ST_Area(geom)/10000 from cutblock))::numeric, 1) as resting_piece_density_cutblock,
        ROUND(sum((cwd_rest_1 * area_ha) / (select ST_Area(geom)/10000 from cutblock))::numeric, 1) as resting_piles_density_cutblock,
        (select count(*) from fisher_habitats where harvest_im ilike 'warning%') as warning_count,
        (select count(*) from fisher_habitats where harvest_im ilike 'caution%') as caution_count,
        (select json_build_object(
            'type', 'FeatureCollection',
            'features', coalesce(json_agg(ST_AsGeoJSON(t.*)::json), '[]'::json)
            )
            from (
                select  id,
                        fisher_hab,
                        harvest_im,
                        geom
                from fisher_habitats where harvest_im ilike 'WARNING: Any harvest of this rare%'
            ) t
        ) as yellow_polygons,
        (select json_build_object(
            'type', 'FeatureCollection',
            'features', coalesce(json_agg(ST_AsGeoJSON(t.*)::json), '[]'::json)
            )
            from (
                select  id,
                        fisher_hab,
                        harvest_im,
                        geom
                from fisher_habitats where harvest_im ilike 'WARNING: Harvest of this exceptionally rare%'
            ) t
        ) as red_polygons
    from fisher_habitats
    """

    # sample_cutblock = load_cutblock('/app/fixtures/cutblocks_sample.shp')

    result = db.execute(
        q,
        {
            "cutblock":cutblock.wkt
        }
    )

    result = dict(result.fetchone())

    return result

  
@router.post("/process_file")
async def upload_file(shape: UploadFile = File(...), db: Session = Depends(get_db)):
    print(shape.file)
    try:
        os.mkdir("shapes")
        print(os.getcwd())
    except Exception as e:
        print(e) 
    file_name = os.getcwd()+"/shapes/"+shape.filename.replace(" ", "-")
    print('filepath' + file_name)
    with open(file_name,'wb+') as f:
        f.write(shape.file.read())
        f.close()
    
    file = jsonable_encoder({"imagePath":file_name})

    this_cutblock = load_cutblock(file_name)
    result = habitat_in_polygon(this_cutblock, db)
    return result

@router.post("/process_drawing")
def upload_drawing(shape):
  print(shape)
  this_cutblock = load_cutblock(shape)
  result = habitat_in_polygon(this_cutblock)

  return result