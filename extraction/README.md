# ChEMBL database extract for MELLODDY

## Running the ChEMBL database

### The first time
1. Get ChEMBL database dump
```bash
mkdir data
wget ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_25_postgresql.tar.gz
tar -xf chembl_25_postgresql.tar.gz chembl_25/chembl_25_postgresql/chembl_25_postgresql.dmp
mv chembl_25/chembl_25_postgresql/chembl_25_postgresql.dmp data/
rm -r chembl_25
```

2. Launch the container
```bash
docker run -it --name iktos_postgres -p 5432:5432 -e POSTGRES_PASSWORD=mypassword -d iktos-postgres
```

3. Create database and restore the ChEMBL dump
```bash
docker exec -it iktos_postgres psql -h localhost -p 5432 -U postgres -c "create database chembl_25;"
docker exec -it iktos_postgres pg_restore --dbname=chembl_25 --username=postgres data/chembl_25_postgresql.dmp > restore.log
```

4. Access CLI PostgreSQL client
```bash
docker exec -it iktos_postgres psql -h localhost -p 5432 -U postgres
```

### Re-starting the container after a machine reboot
+ Simply start the container
```bash
docker start iktos_postgres
```

### Other commands
+ Run SQL script
```bash
cat query.sql | docker exec -it iktos_postgres psql -h localhost -p 5432 -U postgres -d chembl_25
```

+ Dump database
```bash
docker exec -it iktos_postgres pg_dumpall -c -U postgres > database_export.sql
```

+ Export table
```bash
docker exec -it iktos_postgres psql -h localhost -p 5432 -U postgres -d chembl_25 -c "\copy melloddy TO STDOUT WITH (FORMAT CSV, HEADER);" > melloddy.csv
```
