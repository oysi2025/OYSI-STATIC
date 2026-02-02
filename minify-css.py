#!/usr/bin/env python3
"""
CSS Minifier for inline styles in HTML files
"""
import re
from pathlib import Path

def minify_css(css: str) -> str:
    """Minify CSS by removing whitespace and comments"""
    # Remove comments
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)

    # Remove newlines and extra whitespace
    css = re.sub(r'\s+', ' ', css)

    # Remove whitespace around special characters
    css = re.sub(r'\s*([{};:,>+~])\s*', r'\1', css)

    # Remove whitespace around parentheses
    css = re.sub(r'\s*\(\s*', '(', css)
    css = re.sub(r'\s*\)\s*', ')', css)

    # Remove trailing semicolons before closing braces
    css = re.sub(r';}', '}', css)

    # Remove leading/trailing whitespace
    css = css.strip()

    return css

def process_html_file(filepath: Path):
    """Process a single HTML file and minify its inline CSS"""
    print(f"\n📄 Processing: {filepath.name}")

    content = filepath.read_text(encoding='utf-8')
    original_size = len(content)

    # Find all <style> blocks
    def replace_style(match):
        original_css = match.group(1)
        minified_css = minify_css(original_css)
        original_len = len(original_css)
        minified_len = len(minified_css)
        savings = ((original_len - minified_len) / original_len) * 100 if original_len > 0 else 0
        print(f"   CSS: {original_len:,} → {minified_len:,} bytes ({savings:.1f}% smaller)")
        return f'<style>{minified_css}</style>'

    # Replace all style blocks
    new_content = re.sub(r'<style>([\s\S]*?)</style>', replace_style, content)

    new_size = len(new_content)
    total_savings = ((original_size - new_size) / original_size) * 100

    # Write back
    filepath.write_text(new_content, encoding='utf-8')
    print(f"   Total: {original_size:,} → {new_size:,} bytes ({total_savings:.1f}% smaller)")

def main():
    print("🗜️  CSS Minification for OYSI Static")
    print("=" * 50)

    base_path = Path("/home/ubuntu/services/oysi-static/public")

    # Process all active HTML files
    files_to_process = [
        "de/index.html",
        "fr/index.html",
        "en/index.html",
        "de/about.html",
        "fr/about.html",
        "en/about.html",
        "de/contact.html",
        "fr/contact.html",
        "en/contact.html",
        "de/faq.html",
        "fr/faq.html",
        "en/faq.html",
        "de/services.html",
        "fr/services.html",
        "en/services.html",
        "de/dpp.html",
        "fr/dpp.html",
        "en/dpp.html",
        "de/legal.html",
        "fr/legal.html",
        "en/legal.html",
        "de/privacy.html",
        "fr/privacy.html",
        "en/privacy.html",
        "de/outcomes.html",
        "fr/outcomes.html",
        "en/outcomes.html",
        "de/seo-block.html",
        "fr/seo-block.html",
        "en/seo-block.html",
    ]

    for file_path in files_to_process:
        full_path = base_path / file_path
        if full_path.exists():
            process_html_file(full_path)

    print("\n" + "=" * 50)
    print("✅ CSS minification complete!")

if __name__ == "__main__":
    main()
