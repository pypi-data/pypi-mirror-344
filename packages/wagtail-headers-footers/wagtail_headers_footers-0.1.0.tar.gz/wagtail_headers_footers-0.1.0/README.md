# Wagtail Header Footer Scripts

A reusable Wagtail app for managing header and footer scripts across different sites using Wagtail Settings.

![Wagtail Admin Screenshot](https://raw.githubusercontent.com/dazzymlv/wagtail-headers-footers/main/docs/screenshot.png)

## Features

- Add header/footer scripts per site
- Use Wagtail settings and model clustering
- Toggle scripts on/off

## Installation

```bash
pip install wagtail-headers-footers
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "wagtail_headers_footers",
]
```

## Usage

Go to **Settings > Headers & Footers** in the Wagtail Admin to manage your scripts.

## Testing

```bash
python -m unittest discover tests
```

## License

MIT
