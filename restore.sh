#!/bin/bash

psql << EOF
# psql -d imdb << EOF
select nspname from pg_namespace where nspname='public';
analyze;