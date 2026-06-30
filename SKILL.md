---
name: mathmodel-latex-skill
description: Generate stable and competition-style LaTeX mathematical modeling paper projects for MCM/ICM and CUMCM. Use when Codex needs to create, adapt, compile, or preflight competition paper templates for COMAP MCM/ICM, Chinese Undergraduate Mathematical Contest in Modeling (CUMCM), or similar mathematical modeling submissions, including mcmthesis, cumcmthesis, XeLaTeX, latexmk, PDF page/size checks, identity-info checks, references, appendices, and AI-use disclosure sections.
---

# Mathematical Modeling LaTeX Projects

Use this skill to create reproducible LaTeX paper projects for MCM/ICM and CUMCM. Prefer the templates in this skill, keep dependencies explicit, and avoid embedding real identity information.

## Competition Recognition

- Treat prompts mentioning MCM, ICM, COMAP, Meritorious/Winner papers, team control number, problem A-F, or "Report on Use of AI" as MCM/ICM.
- Treat prompts mentioning CUMCM, National Undergraduate Mathematical Contest in Modeling, 国赛, 全国大学生数学建模竞赛, 承诺书, 编号专用页, 支撑材料, or 中文摘要 as CUMCM.
- If the contest is unclear, infer from language and required fields: English + team control number usually means MCM/ICM; Chinese + 摘要页/支撑材料 usually means CUMCM.
- If official rules for the current year are provided, follow them over these defaults.

## Reference Mode

- Decide `use_ref_bib` before generating or editing a project.
- Default to `use_ref_bib = false` when the user does not mention a bibliography database, citation manager, BibTeX, or `ref.bib`; keep the inline `thebibliography` block and do not require BibTeX.
- Set `use_ref_bib = true` when the user asks for `ref.bib`, BibTeX, citation-key based references, Zotero/JabRef/BibDesk exports, or a reusable bibliography database.
- When `use_ref_bib = true`, set `\userefbibtrue` in `main.tex`, keep `ref.bib` beside `main.tex`, cite entries with `\cite{...}`, and let `latexmk` run BibTeX automatically. Replace the sample `placeholder-ref` entry and `\nocite{placeholder-ref}` before final submission.
- Do not mix active `thebibliography` and active `\bibliography{ref}` in the same generated paper.

## MCM/ICM Generation Rules

- Start from `templates/mcm-icm/main.tex`.
- Use the official LaTeX package class when available:

```tex
\documentclass{mcmthesis}
```

- Treat `mcmthesis` as a formal LaTeX package normally managed by TeX Live or MiKTeX. Do not copy `mcmthesis.cls` into the project by default.
- Include placeholders for team control number, problem letter, title, summary, keywords, model sections, references, appendices, and `Report on Use of AI`.
- Support `use_ref_bib` through the `\userefbibfalse` / `\userefbibtrue` switch and `templates/mcm-icm/ref.bib`.
- Include a table of contents after `\maketitle` for MCM/ICM by default, matching the `mcmthesis` demo pattern. Remove it only if the current official rules or user request say not to include it.
- Keep all identity fields generic. Use placeholders such as `0000000`, `A`, and `Paper Title Placeholder`.
- Do not add school names, author names, adviser names, regions, email addresses, phone numbers, or acknowledgements that reveal the team.

## CUMCM Generation Rules

- Prefer `templates/cumcm/main-cumcmthesis.tex` when `cumcmthesis.cls` is available:

```tex
\documentclass[withoutpreface,bwprint]{cumcmthesis}
```

- This skill includes a lightweight `templates/cumcm/cumcmthesis.cls` compatibility class so the default CUMCM entry can compile offline. Treat it as a portable compatibility layer, not as a guarantee of official current-year formatting. Do not assume third-party `cumcmthesis` variants can be installed with `tlmgr`.
- Also provide `templates/cumcm/main.tex` for the default cumcmthesis-compatible entry point and `templates/cumcm/main-ctexart-fallback.tex` as a no-class fallback.
- Use XeLaTeX for all Chinese templates.
- Default to electronic version options `withoutpreface,bwprint`.
- Include a dedicated abstract page, keywords, body sections, references, appendices, supporting-material file list, and AI tool usage details placeholder.
- Support `use_ref_bib` through the `\userefbibfalse` / `\userefbibtrue` switch and `templates/cumcm/ref.bib`.
- Do not generate a table of contents in CUMCM electronic submissions by default. Keep only commented optional `\tableofcontents` lines for years or local rules that explicitly require it.
- Do not generate school, team member, adviser, instructor, campus, province, or regional identity information. Leave identity-related class commands absent or blank unless the user explicitly supplies non-sensitive placeholders required by official rules.

### CUMCM Excellent-Paper Style Rules

- For CUMCM, follow `templates/cumcm/STYLE_GUIDE.md` when generating paper structure or examples.
- Use the default section order: 摘要, 问题重述, 问题分析, 模型假设, 符号说明, 数据预处理, 模型建立与求解, 模型检验, 模型评价与推广, 参考文献, 附录.
- Render level-one CUMCM sections as Chinese numerals with a dunhao, such as `一、问题重述`; render subsections as `1.1 问题背景`.
- Standardize the data section title as `数据预处理`. Do not use `数据读取与预处理`, `数据剔写`, `数据说明与读取`, or other ad-hoc titles in final-style CUMCM papers.
- Write model assumptions as a numbered list. Each item must follow the pattern `假设 n：...。解释：...` so the assumption and its modeling justification are both visible.
- Do not add non-paper chapters such as `编译测试结果`, `LaTeX 测试说明`, or standalone `算法实现说明` to CUMCM example PDFs. Put run commands, compile notes, and code explanations in README or appendices.
- In the abstract and result sections, never invent numerical results. Use explicit placeholders when no solver output exists.

## Compilation Rules

- Use `latexmkrc`; it defaults to XeLaTeX.
- Compile according to contest/template:

```bash
# MCM/ICM, mcmthesis workflow
latexmk -pdf main.tex

# CUMCM Chinese workflow
latexmk -xelatex main.tex
# or, when this skill's latexmkrc is present in the project directory
latexmk main.tex
```

- Do not use `latexmk -pdf` for CUMCM Chinese templates; it forces pdfLaTeX in many latexmk versions and can fail on `ctexart`/XeLaTeX font handling.

- For MCM/ICM, run `scripts/check_latex_env.py --contest mcm-icm` first to verify `mcmthesis.cls`. If `mcmthesis.cls` is missing, stop MCM/ICM project generation or compilation and tell the user to install `mcmthesis` through TeX Live, MiKTeX, or their TeX package manager before retrying.
- For CUMCM, run `scripts/check_latex_env.py --contest cumcm` first. Prefer the local `templates/cumcm/cumcmthesis.cls` compatibility class when copied with the project. If no local or TeX-tree `cumcmthesis.cls` is available, default to `templates/cumcm/main-ctexart-fallback.tex`; this is a warning, not a failure, as long as the `ctexart` fallback is available.
- Only when the user explicitly requires a third-party/full `cumcmthesis` class or strict official-class compatibility beyond the local compatibility class, ask the user to provide that class and verify its license/font requirements/current-year compliance.
- If `use_ref_bib = true`, add `--use-ref-bib` to the same contest-specific environment check, for example `scripts/check_latex_env.py --contest mcm-icm --use-ref-bib`.
- Do not make successful compilation depend on network access. Network downloads are not a valid build step.
- Before the contest, freeze the final compilable template and dependencies together, including allowed class files. Do not bundle font files unless their license clearly permits redistribution and the user intentionally provides them.

## Prohibited Behavior

- Do not add third-party `.cls` files with unclear redistribution rights. The bundled `templates/cumcm/cumcmthesis.cls` is a lightweight compatibility class; keep third-party class files separate unless the user intentionally provides them and their license permits redistribution.
- Do not invent official year-specific page limits, size limits, AI disclosure rules, or submission rules. Use the current official contest documents when supplied.
- Do not insert real schools, names, student IDs, adviser names, regions, emails, phone numbers, or acknowledgements.
- Do not switch Chinese templates to pdfLaTeX.
- Do not enable `ref.bib` without also keeping the `ref.bib` file in the copied project directory.
- Do not depend on online images, online bibliographies, or online package installation during final compilation.
- Do not include a table of contents in the CUMCM fallback electronic template unless the user explicitly requests it.

## Checklists

Before writing a project:

- Identify the contest as MCM/ICM or CUMCM.
- Decide whether `use_ref_bib` is true or false.
- Choose the matching template directory.
- Run `scripts/check_latex_env.py --contest mcm-icm` or `scripts/check_latex_env.py --contest cumcm`, adding `--use-ref-bib` when BibTeX is needed.
- Decide whether class dependencies are installed locally or whether a fallback is needed.

Before final submission:

- Compile from a clean directory with the contest-appropriate command: `latexmk -pdf main.tex` for MCM/ICM, and `latexmk -xelatex main.tex` or `latexmk main.tex` with this skill's `latexmkrc` for CUMCM.
- Open the PDF and inspect the first page, references, appendices, and AI-use section.
- If official page and file-size limits are known, run `scripts/check_pdf.py <paper.pdf> --max-pages <official-page-limit> --max-size-mb <official-size-limit-mb>`.
- If official limits are not provided, run `scripts/check_pdf.py <paper.pdf>` without page or size flags, then note that the official current-year limits still need manual confirmation.
- Treat default identity keyword matches from `check_pdf.py` as warnings that need human review. For the final gate, run `scripts/check_pdf.py <paper.pdf> --identity-mode strict`, using repeated `--ignore-keyword <word>` only for reviewed false positives such as institution names in references or data sources.
- Confirm manually that the PDF does not contain real personal, school, adviser, team, email, phone, or regional identity information.
- Confirm all generated figures, tables, code listings, references, and supporting-material filenames match the final paper.
