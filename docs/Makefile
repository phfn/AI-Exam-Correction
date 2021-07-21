.PHONY: clean view

main:
	mkdir -p build/pdf
	pdflatex -output-directory=build/ src/devdoc.tex
	pdflatex -output-directory=build/ src/systemdoc.tex
	pdflatex -output-directory=build/ src/userdoc.tex
	mv build/*.pdf build/pdf

clean: 
	rm -r build/

view:
	evince build/pdf/*.pdf
