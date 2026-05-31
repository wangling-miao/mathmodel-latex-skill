$pdf_mode = 5;
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$bibtex = 'bibtex %O %B';
$biber = 'biber %O %B';
$max_repeat = 5;

push @generated_exts, 'synctex.gz';
