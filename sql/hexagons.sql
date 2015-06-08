--bug: overshooting y-max a lot. Need adjustments on the nrow calculations
--Thanks to: http://rexdouglass.com/spatial-hexagon-binning-in-postgis/ 
SET search_path TO "sandbox","public";
DROP TABLE IF EXISTS hex_grid;
CREATE TABLE hex_grid (gid serial not null primary key);
 
SELECT addgeometrycolumn('hex_grid','the_geom', 0, 'POLYGON', 2);
 
CREATE OR REPLACE FUNCTION genhexagons(width float, xmin float,ymin  float,xmax float,ymax float  )
RETURNS float AS $total$
declare
    b float :=width/2;
    a float :=b/2; --sin(30)=.5
    c float :=2*a;
    height float := 2*a+c;  --1.1547*width;
    ncol float :=ceil(abs(xmax-xmin)/width);
    nrow float :=ceil(abs(ymax-ymin)/height);
 
    polygon_string varchar := 'POLYGON((' ||
 
                                        0 || ' ' || 0     || ' , ' ||
 
                                        b || ' ' || a     || ' , ' ||
 
                                        b || ' ' || a+c   || ' , ' ||
 
                                        0 || ' ' || a+c+a || ' , ' ||
 
                                     -1*b || ' ' || a+c   || ' , ' ||
 
                                     -1*b || ' ' || a     || ' , ' ||
 
                                        0 || ' ' || 0     ||
 
                                '))';
 
BEGIN
    INSERT INTO hex_grid (the_geom) 
    SELECT st_translate(the_geom, x_series*(2*a+c)+xmin, y_series*(2*(c+a))+ymin)
        FROM 
        generate_series(0, ncol::int,1) AS x_series,
        generate_series(0, nrow::int,1) AS y_series,
        (SELECT polygon_string::geometry AS the_geom
            UNION
        SELECT ST_Translate(polygon_string::geometry, b , a+c)  AS the_geom
        ) AS two_hex;
 
    ALTER TABLE hex_grid
    ALTER COLUMN the_geom TYPE geometry(Polygon, 4326)
 
    USING ST_SetSRID(the_geom,4326);
 
    RETURN NULL;
 
END;
 
$total$ LANGUAGE plpgsql;
 
--width in the units of the projection, xmin,ymin,xmax,ymax
SELECT genhexagons(0.5,3.339844,57.562995,31.904297,71.497037);
 
CREATE INDEX
  ON hex_grid
  USING gist
  (the_geom);
 
DROP TABLE IF EXISTS hex_grid_05;
ALTER TABLE hex_grid RENAME TO hex_grid_05;

CREATE OR REPLACE VIEW public.hex AS 
 SELECT hex_grid_05.the_geom AS wkb_geometry,
    hex_grid_05.gid AS ogc_fid
   FROM hex_grid_05,
    kommuner
  WHERE hex_grid_05.the_geom && kommuner.wkb_geometry;

ALTER TABLE public.hex
  OWNER TO atlefren;
