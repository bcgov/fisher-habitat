ogr2ogr -f "PostgreSQL" PG:"dbname=fisher user=fisher host=localhost port=5432 password=test" \
"./data/Fisher_Range/Fisher_Range.shp" \
--config PG_USE_COPY YES \
-lco precision=NO \
-t_srs EPSG:4326 \
-lco GEOMETRY_NAME=geom \
-nlt PROMOTE_TO_MULTI -nln fisher_range

ogr2ogr -f "PostgreSQL" PG:"dbname=fisher user=fisher host=localhost port=5432 password=test" \
"./data/fisher_fhe.shp" \
--config PG_USE_COPY YES \
-t_srs EPSG:4326 \
-lco GEOMETRY_NAME=geom \
-nlt PROMOTE_TO_MULTI -nln fisher_fhe -progress
