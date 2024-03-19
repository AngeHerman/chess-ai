all:
	# -shell escape : nécessaire pour minted
	pdflatex -shell-escape rapport-kouehemazro-nzaba.tex
	# on compile une deuxième fois pour les références
	pdflatex -shell-escape rapport-kouehemazro-nzaba.tex

prof:
	# -shell escape : nécessaire pour minted
	pdflatex -shell-escape report.tex
	# on compile une deuxième fois pour les références
	pdflatex -shell-escape report.tex

clean:
	rm -rf *bak *~ *out *log *aux _minted-report *.aex
