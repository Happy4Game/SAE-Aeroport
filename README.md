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
Concernant les données nécessaires pour faire fonctionner le programme, vous devez impérativement importer la base de données avec ces caractéristiques suivantes:
- Nom d'utilisateur : john
- Mot de passe : doe

Si vous souhaitez modifier ces valeurs, je vous invite à aller les modifier dans le fichier dénommé BddControler.py à partir de la ligne 22