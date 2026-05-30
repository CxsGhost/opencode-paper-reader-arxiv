#!/usr/bin/env python3
"""
download_arxiv.py
Helper script to download arXiv paper LaTeX source using Python requests.
Usage: python download_arxiv.py <arxiv_id> [output_dir]
"""

import sys
import os
import re
import tarfile
import shutil
import requests


def sanitize_dirname(name):
    """Sanitize paper title for filesystem safety."""
    # Replace invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|]', ' ', name)
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    # Replace spaces with hyphens for readability
    sanitized = sanitized.replace(' ', '-')
    return sanitized


def download_arxiv(arxiv_id, output_dir='.'):
    """Download and extract arXiv LaTeX source."""
    
    # Validate arXiv ID format
    if not re.match(r'^[0-9]+(\.[0-9]+)?$', arxiv_id):
        print(f"Error: Invalid arXiv ID format: {arxiv_id}")
        print("Expected format: XXXX.XXXXX or XXXX")
        return False
    
    download_url = f"https://arxiv.org/src/{arxiv_id}"
    archive_name = f"arxiv_{arxiv_id}.tar.gz"
    
    print(f"Downloading arXiv source for ID: {arxiv_id}")
    print(f"URL: {download_url}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Download the archive
    archive_path = os.path.join(output_dir, archive_name)
    try:
        print("Downloading archive...")
        response = requests.get(download_url, timeout=120)
        response.raise_for_status()
        
        # Check if content is HTML error page
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            print("Error: arXiv returned an HTML page. The paper ID may be invalid or source is not available.")
            return False
        
        with open(archive_path, 'wb') as f:
            f.write(response.content)
        print(f"Archive saved: {archive_path}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to download from {download_url}: {e}")
        return False
    
    # Create paper directory
    paper_dir = os.path.join(output_dir, f"paper_{arxiv_id}")
    src_dir = os.path.join(paper_dir, "src")
    report_dir = os.path.join(paper_dir, "analysis_report")
    
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    
    # Extract the archive
    print("Extracting archive...")
    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(path=src_dir)
        print(f"Extracted to: {src_dir}")
    except tarfile.TarError as e:
        print(f"Error: Failed to extract archive: {e}")
        os.remove(archive_path)
        return False
    
    # Remove the archive after extraction
    os.remove(archive_path)
    print(f"Removed archive: {archive_path}")
    
    print("")
    print(f"Success! Paper source extracted to: {paper_dir}")
    print(f"  - Source files: {src_dir}")
    print(f"  - Analysis reports: {report_dir}")
    
    # List extracted files
    print("\nExtracted files:")
    for root, dirs, files in os.walk(src_dir):
        level = root.replace(src_dir, '').count(os.sep)
        indent = '  ' * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '  ' * (level + 1)
        for file in files[:10]:  # Limit to first 10 files
            print(f"{subindent}{file}")
        if len(files) > 10:
            print(f"{subindent}... and {len(files) - 10} more files")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python download_arxiv.py <arxiv_id> [output_dir]")
        print("Example: python download_arxiv.py 2512.15745 ./papers")
        sys.exit(1)
    
    arxiv_id = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
    
    success = download_arxiv(arxiv_id, output_dir)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()