# Logo attribution

Both packages carry two files:

- **`assets/logo.svg`** — the official mark as DataHub ships it, 152×130.
- **`assets/logo-square.svg`** — the same paths in a 1:1 window
  (`viewBox="1.588 -5 140 140"`), centring the mark with no geometry change.
  Anthropic's MCP Directory submission requires a square SVG, so this is the one
  the manifests point at.

`assets/logo.svg` is taken from
`docs-website/static/img/datahub-logo-color-mark.svg` in
[datahub-project/datahub](https://github.com/datahub-project/datahub) and stripped
of Inkscape editor metadata. Geometry, `viewBox`, dimensions and the three brand
colors (`#006dcd`, `#d23500`, `#ec9e32`) are byte-for-byte unchanged.

**The logo is a trademark, not code.** Apache-2.0 covers the source in these
packages but [explicitly does not grant trademark rights](https://www.apache.org/licenses/LICENSE-2.0#trademarks)
(section 6). The mark is used here to identify a DataHub integration. If you fork
these packages into something that isn't a DataHub integration, replace it.
