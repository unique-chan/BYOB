
### Preliminaries

~~~shell
conda create -n byob python=3.11 -y
conda activate byob
~~~

### Test (Arma3 metadata)
~~~shell
sqlite3 outputs/dump_arma/state.db
~~~

~~~sql
.header on
.mode column  # Try .mode line

select * from 'groups' limit 1;
select * from 'units' limit 1;
select * from 'vehicles' limit 1;
select * from 'snapshots' limit 1;
~~~