<h1 align="center">
 BYOB: Bring Your Own Battleplan! 🍾
</h1>

<h3 align="center">
 🛠️ Simulation Platform and Code
</h3>

<p align="center">
  <a href="#"><img alt="Python3.11" src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white"></a>
  <a href="#"><img alt="Arma 3" src="https://img.shields.io/badge/Game-Arma 3-green?logo=steam"></a>
</p>


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