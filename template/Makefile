PALESTRAS=out

%.pdf: %.tex
	xelatex $<
	xelatex $<
	$(RM) *.aux *.dvi *.out *.log *.nav *.snm *.toc *.vrb

all: $(patsubst %,%.pdf,$(PALESTRAS))

.PHONY: all clean

clean:
	$(RM) *.aux *.dvi *.pdf *.out *.log *.nav *.snm *.toc *.fls *.fdb_latexmk *.synctex.gz *.vrb
