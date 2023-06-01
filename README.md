# Installation
Pour exécuter ce programme, vous devez installer la bibliothèque python :
```
pip install geopandas
```
Il est possible que vous rencontriez une erreur lors du lancement du programme, si l'erreur est : 
```
QSqlDatabase: QPSQL driver not loaded
QSqlDatabase: available drivers: QSQLITE QODBC QPSQL
```
Vous devez ajouter cette ligne dans vos variables d'environnement
```
C:\Program Files\PostgreSQL\<version>\bin
```