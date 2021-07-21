.PHONY: clean view

main:
	mkdir -p build/pdf
	cd src/uml && make
	pdflatex -output-directory=build/ src/devdoc.tex
	pdflatex -output-directory=build/ src/systemdoc.tex
	pdflatex -output-directory=build/ src/userdoc.tex
	mv build/*.pdf build/pdf

clean: 
	rm -rf build/
	cd src/uml && make clean

view:
	evince build/pdf/*.pdf
