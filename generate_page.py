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


STAC_CATALOG_URL = "https://stac.overturemaps.org/catalog.json"


def get_latest_release() -> str:
    """Fetch the latest release version from the STAC catalog."""
    catalog = pystac.Catalog.from_file(STAC_CATALOG_URL)
    
    # Get all child collections/catalogs and sort by ID (date-based) descending
    children = list(catalog.get_children())
    latest = sorted(children, key=lambda c: c.id, reverse=True)[0]
    
    return latest.id


def generate_html(version: str) -> str:
    """Generate the HTML page with the given version."""
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
            margin-bottom: 48px;
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