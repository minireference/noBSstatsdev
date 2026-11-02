# Editing the theme

`custom.css` is an ordinary stylesheet loaded by `site.options.style` in
this book's `myst.yml`. It applies to all pages in this book.

| Section | Change here |
| --- | --- |
| `:root` custom variables | Body and heading fonts, radius, line height. |
| `:root` MyST variables | Light-mode colours. |
| `.dark` | Dark-mode colours. |
| `.article ...` | Text, headings, code, quotations, and tables. |
| `.custom-class-*` | Blocks explicitly marked in the sample content. |
| Media query | Small-screen refinements. |


Inspect the actual DOM and computed styles in browser developer tools.
Prefer documented `--myst-color-*` variables for colours.
Check light mode, dark mode, and a narrow viewport.
The `.custom-class-*` rules apply to content with those explicit classes.


## Links

- [MyST styling guide](https://mystmd.org/guide/website-style)
- [Theme colour variables](https://myst-theme.netlify.app/theming/)
- [Interactive colour picker](https://myst-theme.netlify.app/color-picker/)
- [Upstream styles](https://github.com/jupyter-book/myst-theme/tree/main/styles)
