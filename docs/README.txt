# Documentation for Automatic Exam Correction Projekt 

### Conventions

* Every sentence in its own line
* Every chapter gets its own section or subsection
* One file per chapter
* Chapters can be insterted locally into the main files, but not beeing pushed
* Work in the created folders
* Create a branch per chapter
* If you want to use (UML)Diagrams use PlantUML

### Building PDFs

Execute "$ make" to build everything, this includes:

* All 3 latex files in src/ (the chapters don't need sperate building)
* All plantUML files in src/uml/src 

Each main file has a command to build, look into the Makefile too see the function names.
You can call it with "$ make <FUNCTION NAME>"

Sourcecode to build movement:

Latex: src/*.tex  -> build/ & build/pdf
PlantUML: src/uml/src/*.puml -> src/uml/build/

Execute "$ make clean" to remove all buildfiles 
