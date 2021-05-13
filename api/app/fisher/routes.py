"""
Map layers (layers module) API endpoints/handlers.
"""
import random
import logging
from fastapi import APIRouter, Depends, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.db.utils import get_db
from app.fisher.cutblocks import load_cutblock

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


@router.get('/habitat')
def habitat_in_polygon(db: Session = Depends(get_db)):
    """ function goes here """

    q = """
    with fisher_habitats as (
        select  geom,
                fisher_hab,
                harvest_im,
                denning_wa,
                denning_pr * shape_area / 10000 as denning_pr,
                branch_res,
                branch_r_1 * shape_area / 10000 as branch_r_1,
                cavity_res,
                cavity_r_1 * shape_area / 10000 as cavity_r_1,
                cwd_restin  * shape_area / 10000 as cwd_restin,
                cwd_rest_1 * shape_area / 10000 as cwd_rest_1
        from    fisher_fhe
        where   ST_Intersects(
                    geom,
                    ST_Transform(
                        ST_SetSRID(ST_GeomFromText(:cutblock), 3005),
                        4326
                    )
        )
    )
    select
        sum(denning_wa) as sum_denning_warning,
        sum(denning_pr) as sum_denning_primary_density,
        sum(branch_res) as sum_branch_resting_warning,
        sum(branch_r_1) as sum_branch_resting_primary_density,
        sum(cavity_res) as sum_cavity_resting_warning,
        sum(cavity_r_1) as sum_cavity_resting_primary_density,
        sum(cwd_restin) as sum_resting_piece_density,
        sum(cwd_rest_1) as sum_resting_piles_density,
        (select count(*) from fisher_habitats where harvest_im ilike 'warning%') as warning_count,
        (select count(*) from fisher_habitats where harvest_im ilike 'caution%') as caution_count,
        (select ST_AsGeoJSON(ST_CollectionExtract(ST_Collect(geom), 3)) from fisher_habitats where harvest_im ilike 'warning%') as warning_geom,
        (select ST_AsGeoJSON(ST_CollectionExtract(ST_Collect(geom), 3)) from fisher_habitats where harvest_im ilike 'caution%') as caution_geom
    from fisher_habitats
    """

    sample_cutblock = load_cutblock('/app/fixtures/cutblocks_sample.shp')

    result = db.execute(
        q,
        {
            "cutblock":sample_cutblock.wkt
        }
    )

    result = dict(result.fetchone())

    return result
