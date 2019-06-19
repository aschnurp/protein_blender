# Protein Blender

In Blender v2.79 soll ein Addon eingebunden werden, welches die Visualisierung von 
Proteinstrukturen aus PDB-Datein ermöglicht. 


##Installation

Um "Protein Blender" verwenden zu können, werden
+ Blender v2.79 (https://download.blender.org/release/Blender2.79/)
+ Addon (_pdb_addon.py_)
+ PDB File

benötigt. 

Ist das gewünschte PDB File heruntergeladen und  Blender installiert, kann das 
Addon in Blender unter:
 
 __File -> User Preferences -> Add-ons -> Install Add-on from File...__
 
 in dem entsprechenden Verzeichnis installiert werden.
 Um es zu Aktivieren, muss es in der Suchleiste unter "ProteinBlender" gesucht und 
 anschließend ausgewählt werden.

##Benutzeroberfläche

Das Addon ist nun links im _3D Panel_ zu finden und kann von da gesteuert werden. 

Es existieren zwei Optionen:

+ Zeichnen des gewünschten Proteins mithilfe des __Draw Protein__ Buttons
+ Zeichnen der Backbone des Proteins durch den __Draw Backbone__ Button

##Funktionsweise

Wird der __Draw Protein Button__ oder der __Draw Protein Button__ betätigt, so öffnet sich ein File Brwoser und das gewünschte 
PDB File kann ausgewält werden.

Protein Blender liest nun das PDB File aus und zeichnet für jedes Atom eine Kugel in der 
Größe seines Van der Waals Radiuses und färbt sie anschließend in den üblichen Farben ein.

+ C - Schwarz
+ N - Blau
+ O - Rot
+ S - Gelb

__Achtung: Besitzt das Protein mehr als 1000 Atome rechnet das Programm 1 Minute und 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Länger!__

 Wurde ein Protein gezeichnet, so sollte vor der erneuten Betätigung das alte Protein gelöscht werden 
 um Überschneidungen zu vermeiden.
 