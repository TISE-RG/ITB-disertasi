#!/usr/bin/env python3
import os
from pathlib import Path

# Base repo name
REPO_NAME = "tise-itb-dissertation-quarto"

# Helper to write file if not exists (so it's safe to re-run)
def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")
        print(f"Created {path}")
    else:
        print(f"Skipped (exists): {path}")

base = Path(REPO_NAME)

# 1. Create core directories
dirs = [
    base,
    base / "chapters",
    base / "_extensions",
    base / "_extensions" / "tise-itb-dissertation",
]

for d in dirs:
    d.mkdir(parents=True, exist_ok=True)

# 2. _quarto.yml at root (starter project config)
root_quarto = """\
project:
  type: tise-itb-dissertation
  title: "TISE-ITB dissertation"

format:
  tise-itb-dissertation-pdf: default

# Default metadata; students should edit these
dissertation-title: "Judul Tesis / Tugas Akhir"
student-name: "Nama Lengkap Mahasiswa"
student-nim: "18xxxxxx"
program: "Program Studi ..."
faculty: "Sekolah Teknik Elektro dan Informatika"
university: "Institut Teknologi Bandung"
degree: "Sarjana Teknik"
dissertation-type: "TUGAS AKHIR"
supervisor-1: "Dr. Pembimbing Satu"
supervisor-2: "Dr. Pembimbing Dua"
year: "2025"

render:
  - dissertation.qmd
"""
write_file(base / "_quarto.yml", root_quarto)

# 3. dissertation.qmd skeleton
dissertation_qmd = """\
---
title: "{{< var dissertation-title >}}"
format:
  tise-itb-dissertation-pdf: default
---

# Pendahuluan

Tulis Bab 1 di sini…

## Latar Belakang

...

# Tinjauan Pustaka

...

# Metodologi

...

# Hasil dan Pembahasan

...

# Kesimpulan

...

# Daftar Pustaka

Gunakan sitasi biasa, misalnya [@ref1].
"""
write_file(base / "dissertation.qmd", dissertation_qmd)

# 4. Chapters skeleton
chapters_content = {
    "01-pendahuluan.qmd": """\
# Pendahuluan

Tulis isi Bab 1 di sini.
""",
    "02-tinjauan-pustaka.qmd": """\
# Tinjauan Pustaka

Tulis isi Bab 2 di sini.
""",
    "03-metodologi.qmd": """\
# Metodologi

Tulis isi Bab 3 di sini.
""",
    "04-hasil.qmd": """\
# Hasil dan Pembahasan

Tulis isi Bab 4 di sini.
""",
    "05-kesimpulan.qmd": """\
# Kesimpulan

Tulis isi Bab 5 di sini.
""",
}

for fname, content in chapters_content.items():
    write_file(base / "chapters" / fname, content)

# 5. Extension: _extensions/tise-itb-dissertation/_extension.yml
extension_yml = """\
title: "TISE-ITB dissertation Project"
author: "Adapted for TISE-ITB"
version: "0.1.0"
quarto-required: ">=1.5.0"

contributes:
  project:
    project:
      type: default
      output-dir: _output
      render:
        - dissertation.qmd
    format:
      tise-itb-dissertation-pdf: default

  formats:
    tise-itb-dissertation-pdf:
      pdf-engine: xelatex
      documentclass: tise-itb       # change to 'eb-itb' if using original class
      include-in-header:
        - tise-itb-header.tex
      include-before-body:
        - tise-itb-frontmatter.tex
      toc: true
      number-sections: true
      keep-tex: true
"""
write_file(base / "_extensions" / "tise-itb-dissertation" / "_extension.yml", extension_yml)

# 6. tise-itb-header.tex
tise_header_tex = r"""% tise-itb-header.tex
% Map Quarto variables to LaTeX macros expected by tise-itb.cls.
% Adjust macro names on the LEFT to match your actual class file.

$if(dissertation-title)$
  \newcommand{\dissertationTitle}{$dissertation-title$}
$endif$

$if(student-name)$
  \newcommand{\AuthorName}{$student-name$}
$endif$

$if(student-nim)$
  \newcommand{\AuthorNIM}{$student-nim$}
$endif$

$if(program)$
  \newcommand{\ProgramStudi}{$program$}
$endif$

$if(faculty)$
  \newcommand{\Fakultas}{$faculty$}
$endif$

$if(university)$
  \newcommand{\Universitas}{$university$}
$endif$

$if(degree)$
  \newcommand{\Gelar}{$degree$}
$endif$

$if(dissertation-type)$
  \newcommand{\Jenisdissertation}{$dissertation-type$}
$endif$

$if(supervisor-1)$
  \newcommand{\PembimbingSatu}{$supervisor-1$}
$endif$

$if(supervisor-2)$
  \newcommand{\PembimbingDua}{$supervisor-2$}
$endif$

$if(year)$
  \newcommand{\TahunLulus}{$year$}
$endif$
"""
write_file(base / "_extensions" / "tise-itb-dissertation" / "tise-itb-header.tex", tise_header_tex)

# 7. tise-itb-frontmatter.tex
tise_frontmatter_tex = r"""% tise-itb-frontmatter.tex
% Included before $body$.
% Reproduce your TISE-ITB dissertation front matter here.

\frontmatter

% TODO: Replace these with real commands/inputs from your class/template:
% \input{cover}
% \input{approval}
% \input{statement}
% \input{abstract-id}
% \input{abstract-en}

\tableofcontents
\listoffigures
\listoftables

\mainmatter
"""
write_file(base / "_extensions" / "tise-itb-dissertation" / "tise-itb-frontmatter.tex", tise_frontmatter_tex)

# 8. Placeholder tise-itb.cls
tise_cls = r"""% tise-itb.cls
% Placeholder class for TISE-ITB dissertation.
% Replace this file with your actual TISE-ITB (or EB-ITB) dissertation class.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tise-itb}[2025/01/01 Placeholder TISE-ITB dissertation class]

\LoadClass[a4paper,12pt]{report}

% NOTE:
% - Implement the real layout, commands, and environments here,
%   or copy/adapt from the official ITB dissertation class.
"""
write_file(base / "tise-itb.cls", tise_cls)

# 9. README.md
readme = """\
# TISE-ITB dissertation Quarto Template

This repository provides a Quarto-based dissertation template using the **TISE-ITB** format.

## Usage

1. Ensure you have Quarto installed.
2. Copy or install this template as a project.
3. Edit `_quarto.yml` to fill in your dissertation metadata.
4. Write your content in `dissertation.qmd` and `chapters/*.qmd`.
5. Render with:

   ```bash
   quarto render
````

## Note

* `tise-itb.cls` is currently a **placeholder**.
* Replace it with your actual dissertation class file (or adapt from the official ITB/EB-ITB class).
* Ensure the macros in `tise-itb-header.tex` and the front matter in `tise-itb-frontmatter.tex`
  match what your class expects.
  """
  write_file(base / "README.md", readme)

# 10. LICENSE (MIT as a sane default; adjust if needed)

license_text = """
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
write_file(base / "LICENSE", license_text)

print(f"\nScaffold complete. Repo created at: {base.resolve()}")
print("Next steps:")
print("1) Replace tise-itb.cls with your real class (or copy from eb-itb).")
print("2) Update tise-itb-frontmatter.tex with the actual front-matter commands.")
print("3) Run: cd tise-itb-dissertation-quarto && quarto render")

```

If you’d like, I can now adjust this script to:

- directly pull in filenames/macros from your actual `eb-itb-latex` clone (assuming a path), or
- generate a version that you can publish as a Quarto template repo (with `quarto use template ...`).
::contentReference[oaicite:0]{index=0}
```
