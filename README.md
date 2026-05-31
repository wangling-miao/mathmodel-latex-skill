# 数学建模 LaTeX 论文 Skill

这是一个给 Codex 和 Claude Code 使用的 skill，用来生成和检查美赛 MCM/ICM、国赛 CUMCM 的 LaTeX 数学建模论文项目。

它不是一个单独发布的 LaTeX 模板包，而是一组给 AI 编程助手读取的工作规则、模板和检查脚本。安装后，你可以直接让 Codex 或 Claude Code 按比赛类型生成论文项目，并让它处理模板选择、引用方式、匿名信息检查和编译前检查。

## 适合做什么

- 生成 MCM/ICM 英文论文项目。
- 生成 CUMCM 中文论文项目。
- 在 `mcmthesis`、`cumcmthesis`、`ctexart` fallback 之间做稳定选择。
- 控制是否启用 `ref.bib` / BibTeX。
- 避免默认写入学校、队员、导师、赛区等真实身份信息。
- 提供 PDF 页数、大小和明显身份关键词的提交前检查脚本。

## 安装

把整个 `mathmodel-latex-skill` 文件夹复制到对应助手的 skills 目录下。文件夹名建议保持为 `mathmodel-latex-skill`。

### Codex

Windows PowerShell 示例：

```powershell
$skills = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
Copy-Item -Recurse -Force . "$skills\mathmodel-latex-skill"
```

WSL / macOS / Linux 示例：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R . "${CODEX_HOME:-$HOME/.codex}/skills/mathmodel-latex-skill"
```

### Claude Code / cc-switch

如果你使用 `cc-switch` 管理 Claude Code skills，放到 `.cc-switch/skills`。

Windows PowerShell 示例：

```powershell
$skills = "$env:USERPROFILE\.cc-switch\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
Copy-Item -Recurse -Force . "$skills\mathmodel-latex-skill"
```

WSL / macOS / Linux 示例：

```bash
mkdir -p "$HOME/.cc-switch/skills"
cp -R . "$HOME/.cc-switch/skills/mathmodel-latex-skill"
```

如果你的 Claude Code 使用其他 skills 目录，请复制到你实际配置的 skills 路径。

安装后建议开启一个新会话，让新 skill 被重新发现。

## 如何触发

在 Codex 或 Claude Code 里直接描述你的数学建模论文任务即可。可以显式提到 skill 名，也可以只描述比赛类型。

示例：

```text
使用 mathmodel-latex-skill，给我创建一份 MCM/ICM A 题论文项目，启用 ref.bib。
```

```text
使用 mathmodel-latex-skill，生成国赛 CUMCM 电子版论文模板；如果没有 cumcmthesis，就用 ctexart fallback。
```

```text
用这个 skill 检查我的 CUMCM 论文 PDF，确认页数、大小和身份信息风险。
```

## 使用时可以指定的关键选项

`contest`：比赛类型。常用值是 `MCM/ICM` 或 `CUMCM`。

`use_ref_bib`：是否启用 `ref.bib`。默认关闭，使用手写参考文献；如果你需要 BibTeX、Zotero/JabRef 导出的 `.bib`，或希望用 `\cite{...}` 管理引用，就让助手启用它。

`strict_class`：是否严格要求官方或常用类文件。CUMCM 如果没有 `cumcmthesis.cls`，默认会走 `ctexart` fallback；只有你明确要求 `cumcmthesis` 时，助手才会停下来让你提供类文件。

## 内置内容

- `SKILL.md`：AI 助手实际读取的工作规则。
- `templates/mcm-icm/`：MCM/ICM 模板，优先使用 `mcmthesis`。
- `templates/cumcm/`：CUMCM 模板，包含 `cumcmthesis` 版本和 `ctexart` fallback。
- `scripts/check_latex_env.py`：检查本机 LaTeX 类文件和 BibTeX 环境。
- `scripts/check_pdf.py`：检查 PDF 页数、文件大小和明显身份关键词。
- `latexmkrc`：默认使用 XeLaTeX 的构建配置。

## 注意事项

- 本仓库不默认放入 `.cls` 文件。
- `mcmthesis` 通常由 TeX Live / MiKTeX 管理。
- `cumcmthesis` 可能需要你自行提供或安装；不要假设 `tlmgr` 一定能安装。
- 最终比赛提交前，应以当年官方规则为准。
- 任何由 AI 生成的论文内容都需要人工核验。
