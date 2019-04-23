.PHONY: all clean cleanall

all: SpeedTest.pdf

SpeedTest.pdf: SpeedTest.tex bibliografia.bib
	pdflatex SpeedTest.tex
	biber SpeedTest
	pdflatex SpeedTest.tex
	pdflatex SpeedTest.tex

clean:
	rm -f *.aux *.blg *.bbl *.toc *.log *.lof *.lot *.log.xml *.bcf *.out *.run.xml

cleanall: clean
	rm -f SpeedTest.pdf

