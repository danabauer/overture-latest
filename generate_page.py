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
            background: #0f172a;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            color: #e2e8f0;
            margin: 0;
        }}
        
        .card {{
            background: #1e293b;
            border-radius: 16px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            border: 1px solid #334155;
        }}
        
        h1 {{
            font-size: 1.4rem;
            margin: 0 0 32px 0;
            color: #f8fafc;
        }}
        
        h1 span {{
            color: #818cf8;
        }}
        
        .version {{
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            display: inline-block;
            padding: 16px 32px;
            border-radius: 12px;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 32px;
        }}
        
        label {{
            display: block;
            color: #94a3b8;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 6px;
        }}
        
        .path {{
            background: #0f172a;
            padding: 14px 16px;
            border-radius: 8px;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 0.9rem;
            word-break: break-all;
            border: 1px solid #334155;
        }}
        
        .footer {{
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid #334155;
            text-align: center;
            font-size: 0.85rem;
        }}
        
        .footer a {{
            color: #818cf8;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        .path-container {{
            position: relative;
            margin-bottom: 20px;
        }}
        
        .path-container .path {{
            padding-right: 70px;
        }}
        
        .copy-btn {{
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            background: #4f46e5;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.75rem;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            transition: background 0.2s;
        }}
        
        .copy-btn:hover {{
            background: #4338ca;
        }}
        
        .copy-btn.copied {{
            background: #059669;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1><span>Overture Maps</span> Latest Release</h1>
        
        <div class="version">{version}</div>
        
        <label>Amazon S3</label>
        <div class="path-container">
            <div class="path" id="s3-path">s3://overturemaps-us-west-2/release/{version}/</div>
            <button class="copy-btn" onclick="copyPath('s3-path', this)">Copy</button>
        </div>
        
        <label>Microsoft Azure Blob Storage</label>
        <div class="path-container">
            <div class="path" id="azure-path">https://overturemapswestus2.blob.core.windows.net/release/{version}/</div>
            <button class="copy-btn" onclick="copyPath('azure-path', this)">Copy</button>
        </div>
        
        <div class="footer">
            <a href="https://docs.overturemaps.org/getting-data/" target="_blank">Documentation</a>
        </div>
    </div>
    
    <script>
        function copyPath(id, btn) {{
            const text = document.getElementById(id).textContent;
            navigator.clipboard.writeText(text).then(() => {{
                btn.textContent = 'Copied!';
                btn.classList.add('copied');
                setTimeout(() => {{
                    btn.textContent = 'Copy';
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
