"""add postgis

Revision ID: 1c20692e980d
Revises: 
Create Date: 2020-01-03 06:37:10.123404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c20692e980d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        create table fisher_poly (id serial, geom GEOMETRY(MultiPolygon, 4326), harvest_im text); 
    """)


def downgrade():
    pass
