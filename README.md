# Protein Blender

In Blender v2.79 soll ein Addon eingebunden werden, welches die Visualisierung von 
Proteinstrukturen aus PDB-Dateien ermöglicht. 


## Installation

Um "Protein Blender" verwenden zu können, werden benötigt:
+ Blender v2.79 (https://download.blender.org/release/Blender2.79/)
+ Addon (_pdb_addon.py_)
+ PDB-File

Ist das gewünschte PDB-File heruntergeladen und  Blender installiert, kann das 
Addon in Blender unter:
 
 __File -> User Preferences -> Add-ons -> Install Add-on from File...__
 
 in dem entsprechenden Verzeichnis installiert werden.
 Um es zu Aktivieren, muss es in der Suchleiste unter "ProteinBlender" gesucht und 
 anschließend ausgewählt werden.

## Benutzeroberfläche

Das Addon ist nun links im _3D Panel_ zu finden und kann von da gesteuert werden. 

Es existieren drei Optionen, um das gewünschte Protein darzustellen:

+ Protein mit Van der Walls Radius --> __Draw Protein__ Button
+ Zeichnen der Backbone ohne Bonds --> __Draw Backbone__ Button
+ Zeichnen der Backbone mit Bonds --> __Draw Backbone__ Button

## Funktionsweise

Wird einer der Buttons betätigt, so öffnet sich ein File Browser und das gewünschte 
PDB-File kann ausgewählt werden.

Protein Blender liest nun das PDB-File aus und zeichnet für jedes Atom eine Kugel in der 
Größe seines Van der Waals Radiuses und färbt sie anschließend in den folgenden Farben ein.

+ C - Schwarz
+ N - Blau
+ O - Rot
+ S - Gelb

__Achtung: Hat das Protein mehr als 1000 Atome rechnet das Programm 1 Minute und länger!__

 Wurde ein Protein gezeichnet, so sollte vor der erneuten Ausführung das alte Protein gelöscht 
 werden, um Überschneidungen zu vermeiden.