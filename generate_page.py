#!/usr/bin/env python3
"""
Fetches the latest Overture Maps release from S3 and generates a static HTML page.

Requirements:
    pip install obstore

Usage:
    python generate_overture_page.py
    
Output:
    index.html - Static page with latest release info
"""

from obstore.store import S3Store


def get_latest_release() -> str:
    """Fetch the latest release version from the S3 bucket."""
    store = S3Store("overturemaps-us-west-2", region="us-west-2", skip_signature=True)
    releases = store.list_with_delimiter("release/")
    
    # Sort releases in reverse order (newest first)
    sorted_releases = sorted(releases.get("common_prefixes"), reverse=True)
    
    # Extract version from path like "release/2025-11-19.0/"
    latest = sorted_releases[0].split("/")[1]
    return latest


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
            margin-bottom: 20px;
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
    </style>
</head>
<body>
    <div class="card">
        <h1><span>Overture Maps</span> Latest Release</h1>
        
        <div class="version">{version}</div>
        
        <label>Amazon S3</label>
        <div class="path">s3://overturemaps-us-west-2/release/{version}/</div>
        
        <label>Microsoft Azure Blob Storage</label>
        <div class="path">https://overturemapswestus2.blob.core.windows.net/release/{version}/</div>
        
        <div class="footer">
            <a href="https://docs.overturemaps.org/getting-data/" target="_blank">Documentation</a>
        </div>
    </div>
</body>
</html>
"""


def main():
    print("Fetching latest Overture Maps release from S3...")
    version = get_latest_release()
    print(f"Latest release: {version}")
    
    html = generate_html(version)
    
    with open("index.html", "w") as f:
        f.write(html)
    print("Generated index.html")


if __name__ == "__main__":
    main()
