#!/usr/bin/env python3
"""
Fetches the latest Overture Maps release from the STAC catalog and generates a static HTML page.
Requirements:
    pip install pystac
Usage:
    python generate_overture_page.py
    
Output:
    index.html - Static page with latest release info
"""
import pystac
from urllib.parse import quote

STAC_CATALOG_URL = "https://stac.overturemaps.org/catalog.json"
PMTILES_BASE = "s3://overturemaps-extras-us-west-2/tiles/"
# Theme -> (zoom, lat, lng)
THEME_VIEWS = {
    "addresses": (14, 40.7359, -73.9911),  # Union Square, NYC
    "buildings": (11, 39.95, -75.17),       # Philadelphia
    "base": (8, 39.95, -75.17),             # Philadelphia
    "divisions": (8, 39.95, -75.17),        # Philadelphia
    "places": (8, 39.95, -75.17),           # Philadelphia
    "transportation": (8, 39.95, -75.17),   # Philadelphia
}
THEMES = list(THEME_VIEWS.keys())


def get_latest_release() -> str:
    """Fetch the latest release version from the STAC catalog."""
    catalog = pystac.Catalog.from_file(STAC_CATALOG_URL)
    return catalog.extra_fields["latest"]


def get_tile_version(version: str) -> str:
    """Convert release version to tile version (strip minor version)."""
    # 2026-01-21.0 -> 2026-01-21
    return version.rsplit(".", 1)[0]


def get_pmtiles_viewer_url(tile_version: str, theme: str) -> str:
    """Generate pmtiles.io viewer URL for a theme."""
    pmtiles_url = f"{PMTILES_BASE}/{tile_version}/{theme}.pmtiles"
    zoom, lat, lng = THEME_VIEWS[theme]
    return f"https://pmtiles.io/?url={quote(pmtiles_url, safe='')}#map={zoom}/{lat}/{lng}"


def generate_html(version: str) -> str:
    """Generate the HTML page with the given version."""
    tile_version = get_tile_version(version)
    
    # Generate tile links
    tile_links_html = "\n".join(
        f'        <a href="{get_pmtiles_viewer_url(tile_version, theme)}" target="_blank" class="tile-link">{theme}</a>'
        for theme in THEMES
    )
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Overture Maps Latest Release</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            margin: 0;
        }}
        
        .subtitle {{
            font-size: 1rem;
            color: #666;
            margin-bottom: 16px;
        }}
        
        .version {{
            color: #7c3aed;
            font-size: 5rem;
            font-weight: 700;
            margin-bottom: 48px;
        }}
        
        .paths {{
            display: flex;
            gap: 12px;
            margin-bottom: 32px;
        }}
        
        .copy-btn {{
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            padding: 10px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            color: #374151;
            transition: background 0.2s;
        }}
        
        .copy-btn:hover {{
            background: #e5e7eb;
        }}
        
        .copy-btn.copied {{
            background: #d1fae5;
            border-color: #a7f3d0;
            color: #065f46;
        }}
        
        .tiles-section {{
            margin-bottom: 48px;
            text-align: center;
        }}
        
        .tiles-label {{
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 12px;
        }}
        
        .tiles {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
        }}
        
        .tile-link {{
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 0.85rem;
            color: #374151;
            text-decoration: none;
            transition: background 0.2s;
        }}
        
        .tile-link:hover {{
            background: #e5e7eb;
            color: #7c3aed;
        }}
        
        .footer a {{
            color: #7c3aed;
            text-decoration: none;
            font-size: 0.9rem;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="subtitle">What's the latest Overture Maps release?</div>
    
    <div class="version">{version}</div>
    
    <div class="paths">
        <button class="copy-btn" onclick="copyPath('s3://overturemaps-us-west-2/release/{version}/', this)">Copy S3 path</button>
        <button class="copy-btn" onclick="copyPath('https://overturemapswestus2.blob.core.windows.net/release/{version}/', this)">Copy Azure path</button>
    </div>
    
    <div class="tiles-section">
        <div class="tiles-label">View tiles in PMTiles viewer</div>
        <div class="tiles">
{tile_links_html}
        </div>
    </div>
    
    <div class="footer">
        <a href="https://docs.overturemaps.org/getting-data/" target="_blank">Read the docs</a>
    </div>
    
    <script>
        function copyPath(text, btn) {{
            navigator.clipboard.writeText(text).then(() => {{
                const original = btn.textContent;
                btn.textContent = 'Copied!';
                btn.classList.add('copied');
                setTimeout(() => {{
                    btn.textContent = original;
                    btn.classList.remove('copied');
                }}, 2000);
            }});
        }}
    </script>
</body>
</html>
"""


def main():
    print("Fetching latest Overture Maps release from STAC catalog...")
    version = get_latest_release()
    print(f"Latest release: {version}")
    
    html = generate_html(version)
    
    with open("index.html", "w") as f:
        f.write(html)
    print("Generated index.html")


if __name__ == "__main__":
    main()
