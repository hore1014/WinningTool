# WinningTool

A Tool to automatically generate inputs for the IBSYS 2 Supply Chain Simulator

## Einrichten von SQLite
Die vorkompilierten Binaries von SQLite befinden sich im Ordner `.\sqlite\`. Darin befindet sich das Programm `sqlite3.exe` zur Ausführung von SQLite. Um SQLite im Programm oder in der Kommandozeile auszuführen, muss das oben genannte Verzeichnis des Programms zur PATH Umgebungsvariable hinzugefügt werden. 

Zum Einsehen der Datenbank in VSCode kann die [SQLite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite) Extension installiert werden. Die Nutzung wird auf der Downloadseite beschrieben.

## Installieren der Requirements
```sh
pip install -r dev-requirements.txt
```

## Hosting der Webseite mit Heroku 
Dies ist die Dokumentation des Hostings der Webseite mit Heroku. Es ist daher nicht erforderlich diese Schritte erneut durchzuführen.

1. Auf [Heroku](https://dashboard.heroku.com/apps) eine neue App namens `scp-winningtool` erstellt.
2. Installiere die [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Öffne das Terminal in VS Code und führe folgende Befehle aus:
   1. `heroku login`
   2. `git:remote -a "scp-winningtool"`
   3. `git pusj heroku main`, wobei main die branch ist die gehostet werden soll
4. Das Programm kann nun unter https://scp-winningtool.herokuapp.com/ aufgerufen werden.