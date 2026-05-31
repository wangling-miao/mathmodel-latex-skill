# Math Modeling LaTeX Skill

This skill provides reusable LaTeX templates for MCM/ICM and CUMCM papers. It does not include `.cls` files by default.

## Copy A Template

MCM/ICM:

```bash
cp -r templates/mcm-icm my-mcm-paper
cd my-mcm-paper
```

CUMCM with `cumcmthesis`:

```bash
cp -r templates/cumcm my-cumcm-paper
cd my-cumcm-paper
cp main-cumcmthesis.tex main.tex
```

CUMCM fallback without `cumcmthesis`:

```bash
cp -r templates/cumcm my-cumcm-paper
cd my-cumcm-paper
cp main-ctexart-fallback.tex main.tex
```

## Check LaTeX Environment

From this skill directory:

```bash
python scripts/check_latex_env.py
```

If `mcmthesis.cls` is missing, stop MCM/ICM compilation and install it through TeX Live, MiKTeX, or your TeX package manager. For TeX Live, try:

```bash
tlmgr install mcmthesis
```

If `cumcmthesis.cls` is missing, default to the `ctexart` fallback:

```bash
cp main-ctexart-fallback.tex main.tex
```

Only download/provide CUMCMThesis when you explicitly need the `cumcmthesis` class or strict official-class compatibility. Do not assume `tlmgr` can install it.

## Compile

Use XeLaTeX through `latexmkrc`:

```bash
latexmk -pdf main.tex
```

Chinese CUMCM templates must be compiled with XeLaTeX.

## Reference Mode

Templates default to inline references with `thebibliography`.

To use `ref.bib`, change this line in `main.tex`:

```tex
\userefbibfalse
```

to:

```tex
\userefbibtrue
```

Then add entries to the copied `ref.bib` file and cite them with `\cite{placeholder-ref}`. `latexmk` will run BibTeX automatically. Replace the sample `placeholder-ref` entry and `\nocite{placeholder-ref}` before final submission.

Clean auxiliary files when needed:

```bash
latexmk -C
```

## Pre-Submission Check

If official contest limits for the current year are known, pass them explicitly:

```bash
python scripts/check_pdf.py main.pdf --max-pages <official-page-limit> --max-size-mb <official-size-limit-mb>
```

If official limits are not provided, omit the page and size flags:

```bash
python scripts/check_pdf.py main.pdf
```

Before submission, inspect the generated PDF manually and confirm that it contains no school, team member, adviser, region, email, phone, or other identity information.
