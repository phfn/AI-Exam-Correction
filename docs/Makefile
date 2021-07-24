.PHONY: clean view user dev system create-folder

FILES = src/devdoc.tex src/systemdoc.tex src/userdoc.tex
PDFBUILDER = pdflatex
FLAGS = -halt-on-error -output-directory=build/
MOVE = mv build/*.pdf build/pdf
 

main: create-folder
	cd src/uml && make
	for file in $(FILES); do \
		$(PDFBUILDER) $(FLAGS) $$file; \
	done;
	$(MOVE)

create-folder:
	mkdir -p build/pdf


user: create-folder
	mkdir -p build/pdf
	$(PDFBUILDER) $(FLAGS)	src/userdoc.tex
	$(MOVE)

system: create-folder
	mkdir -p build/pdf
	$(PDFBUILDER) $(FLAGS)	src/systemdoc.tex
	$(MOVE)

devdoc: create-folder 
	mkdir -p build/pdf
	$(PDFBUILDER) $(FLAGS)	src/devdoc.tex
	$(MOVE)

clean: 
	rm -rf build/
	cd src/uml && make clean

view:
	evince build/pdf/*.pdf
