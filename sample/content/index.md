---
title: Sample
description: A compact specimen book for developing a Jupyter Book 2 CSS theme.
---

:::{div}
:class: custom-class-lead

A small book with enough variety to make styling decisions visible.
Edit one stylesheet, then inspect prose, mathematics, figures, tables,
and executable notebook outputs in both light and dark modes.
:::

## Start with the specimens

| Page | What to inspect |
| :--- | :--- |
| [Markdown kitchen sink](markdownpage.md) | Headings, text, lists, tables, images, equations, admonitions, tabs, and code fences. |
| [Executable notebook](notebook.ipynb) | Real Python cells, printed output, a DataFrame, Seaborn plots, image includes, and mathematics. |

:::{div}
:class: custom-class-card

### The edit–preview loop

1. Open `theme/custom.css` in your editor.
2. Run `jupyter book start` from this book's folder, such as `sample/`.
3. Change a colour, font, or spacing rule.
4. Inspect both specimen pages and switch between light and dark modes.
5. Build static HTML before transferring the stylesheet to another book.
:::

## A deliberately small project

This website uses the MyST `book-theme` renderer with a custom CSS layer.
There is no separate landing-page replacement in this repository:
the homepage is also a regular book page, so navigation and the theme
can be inspected together.

The notebook includes saved, successfully executed outputs. Building
the website uses those outputs; editing CSS does not require rerunning
the numerical examples. See the repository README for setup, execution,
static builds, checks, and deploying each design version.

```{note}
The pale background, clay-coloured accents, and serif body text are
starter choices. Replace them with the visual style you want to develop.
```

