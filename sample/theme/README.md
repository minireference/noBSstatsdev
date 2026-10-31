# Editing the theme

`custom.css` is an ordinary stylesheet loaded by `site.options.style` in
this book's `myst.yml`. It applies to all pages in this book.

| Section | Change here |
| --- | --- |
| `:root` custom variables | Body and heading fonts, radius, line height. |
| `:root` MyST variables | Light-mode colours. |
| `.dark` | Dark-mode colours. |
| `.article ...` | Prose, headings, code, quotations, and tables. |
| `.custom-class-*` | Blocks explicitly marked in the specimen content. |
| Media query | Small-screen refinements. |

Start the live preview from this book's folder (commands below assume
that you begin at the repository root):

```bash
cd sample
jupyter book start
```

If you copied the book to `design-v2/`, use `cd design-v2` instead. The
root README explains the complete workflow. Build and check from the
repository root:

```bash
python scripts/build.py sample
python scripts/check_build.py sample
```

Inspect the actual DOM and computed styles in browser developer tools.
Prefer documented `--myst-color-*` variables for colours and explicit
content classes for custom components. Check selectors after upgrading
the renderer. Check light mode, dark mode, and a narrow viewport.

Plot colours come from the notebook's Seaborn/Matplotlib code. CSS does
not redraw a saved PNG; re-execute and save the notebook to change plots.

To use the stylesheet in another Jupyter Book 2 project, copy the file
and merge this setting into that book's configuration:

```yaml
site:
  template: book-theme
  options:
    style: theme/custom.css
```

The `.custom-class-*` rules apply to content with those explicit classes.

## References

- [MyST styling guide](https://mystmd.org/guide/website-style)
- [Theme colour variables](https://myst-theme.netlify.app/theming/)
- [Interactive colour picker](https://myst-theme.netlify.app/color-picker/)
- [Upstream styles](https://github.com/jupyter-book/myst-theme/tree/main/styles)
