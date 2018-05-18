# bdsg34

Erstellt automatisch Auskünfte nach Art. 15 DSGVO.

## Abhängigkeiten

Es wird Python und LaTeX benötigt.
## Features

  - Generiert automatisch Anfrageschreiben in LaTeX und im PDF-Format
  - Es können die Unternehmen und Behörden von
    [selbstauskunft.net](https://selbstauskunft.net/) verwendet werden.

## Quick-Start
1. Erstelle eine Datei für die datenverarbeitende Stelle in ```contacts/```,
  von der man eine Auskunft möchte.
   * Eine Beispieldatei ist bereits vorhanden
   * Alternativ kann man bekannte Stelle von
  [selbstauskunft.net](https://selbstauskunft.net/) verwenden
2. Trage persönliche Daten in ```config.json``` ein.
3. Führe ```./bdsg34.py contacts/sample.json``` aus.

## TODO
* Englische Version
* Projektnamen anpassen
