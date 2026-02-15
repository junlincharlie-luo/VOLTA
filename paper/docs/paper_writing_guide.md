# Paper Writing Guide

## Overview

This document provides high-level instructions for writing the NeurIPS 2025 paper.

---

## Paper Structure

### 1. Title
- Concise and descriptive
- Avoid acronyms unless widely known
- Should capture the main contribution

### 2. Abstract (1 paragraph)
- **Problem**: What problem are you solving?
- **Approach**: What is your method/solution?
- **Results**: What are the key findings?
- **Impact**: Why does this matter?

### 3. Introduction (1-1.5 pages)
- Motivate the problem
- State the research gap
- Summarize your contributions (use bullet points)
- Outline paper structure (optional)

### 4. Related Work (0.5-1 page)
- Group related papers by theme
- Clearly differentiate your work from prior art
- Be fair and comprehensive

### 5. Method (2-3 pages)
- Problem formulation
- Proposed approach with clear notation
- Algorithm or model description
- Theoretical analysis (if applicable)

### 6. Experiments (2-3 pages)
- Datasets and baselines
- Implementation details
- Main results with tables/figures
- Ablation studies
- Analysis and discussion

### 7. Conclusion (0.5 page)
- Summarize contributions
- Discuss limitations
- Suggest future work

### 8. References
- Use consistent citation style
- Include recent and relevant works

---

## Formatting Guidelines

| Element | Requirement |
|---------|-------------|
| Page limit | 9 pages (main content) |
| References | Do not count toward limit |
| Appendix | Do not count toward limit |
| Paper size | US Letter |
| Font | Times New Roman, 10pt |
| Margins | As defined in neurips_2025.sty |

---

## Writing Tips

### Clarity
- One idea per paragraph
- Use simple, direct language
- Define terms before using them

### Figures and Tables
- Make them self-contained with descriptive captions
- Use vector graphics when possible
- Ensure readability when printed in grayscale

### Math
- Use consistent notation throughout
- Number important equations
- Explain symbols when first introduced

### Citations
- Use `\citet{}` for "Author (Year)" in text
- Use `\citep{}` for "(Author, Year)" in parentheses

---

## Submission Checklist

- [ ] Paper is within 9-page limit
- [ ] Abstract is under 250 words
- [ ] All figures are high resolution
- [ ] References are complete and consistent
- [ ] Paper checklist is filled out (required)
- [ ] No author-identifying information (for submission)
- [ ] Supplementary material prepared (if needed)

---

## File Structure

```
paper/
├── neurips_2025.tex    # Main paper file
├── neurips_2025.sty    # Style file (do not modify)
├── neurips_2025.pdf    # Compiled output
├── figures/            # Store figures here
├── docs/
│   └── paper_writing_guide.md
└── references.bib      # Bibliography (create as needed)
```

---

## Useful Commands

```bash
# Compile the paper
pdflatex neurips_2025.tex

# Compile with bibliography
pdflatex neurips_2025.tex
bibtex neurips_2025
pdflatex neurips_2025.tex
pdflatex neurips_2025.tex
```

---

## Resources

- [NeurIPS 2025 Call for Papers](https://neurips.cc/Conferences/2025/CallForPapers)
- [NeurIPS Style Guidelines](https://neurips.cc)
- [LaTeX Cheat Sheet](https://wch.github.io/latexsheet/)
