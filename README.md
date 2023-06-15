# mkdocs-today-plugin

This plugin adds a `today` entry (of type datetime.date) to the config object.
The plugin can also be used to patch configuration items with a date value. The
usual use case is to patch the `copyright` entry.

```yaml
copyright: "&copy; {{ today.year }} Snakeoil Corp"

plugins:
  - search
  - today
      items:
        - copyright
  - macros
```
