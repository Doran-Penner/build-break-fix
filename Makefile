HTML = SPEC.html LOGAPPEND.html LOGREAD.html EXAMPLES.html VM.html SCORE.html

all: $(HTML)

#MD ?= markdown_py-2.7
MD ?= python -m markdown

%.html: %.md
	$(MD) $^ > html/$@

clean:
	rm -f *.html
