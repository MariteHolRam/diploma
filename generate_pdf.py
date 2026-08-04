import os
import sys

# Ensure the background asset is extracted first
try:
    if not os.path.exists("background_template.png"):
        print("Background template not found. Running extract_assets.py...")
        import extract_assets
        extract_assets.extract_docx_media(extract_assets.docx_path, extract_assets.output_dir)
except Exception as e:
    print(f"Warning: Failed to run automatic extraction: {e}")

html_file = "index.html"
pdf_file = "Reconocimiento_Don_Fermin_Iribarren.pdf"

print("\n--- PDF GENERATION PROCESS ---")

# Method 1: WeasyPrint (Recommended for pure HTML/CSS printing)
try:
    print("Attempting to generate PDF using WeasyPrint...")
    from weasyprint import HTML
    HTML(html_file).write_pdf(pdf_file)
    print(f"Success! PDF generated successfully: '{pdf_file}' using WeasyPrint.")
    sys.exit(0)
except ImportError:
    print("  WeasyPrint is not installed. Trying next method...")
except Exception as e:
    print(f"  WeasyPrint failed: {e}. Trying next method...")

# Method 2: Playwright (Standard Chromium rendering, highly pixel-perfect)
try:
    print("Attempting to generate PDF using Playwright...")
    import asyncio
    
    async def render_playwright():
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Resolve absolute path for local file
            abs_html_path = os.path.abspath(html_file)
            url = f"file:///{abs_html_path.replace(os.sep, '/')}"
            
            await page.goto(url, wait_until="networkidle")
            
            # Print to PDF using exact Letter size
            await page.pdf(
                path=pdf_file,
                format="Letter",
                print_background=True,
                margin={"top": "0in", "right": "0in", "bottom": "0in", "left": "0in"}
            )
            await browser.close()

    asyncio.run(render_playwright())
    print(f"Success! PDF generated successfully: '{pdf_file}' using Playwright.")
    sys.exit(0)
except ImportError:
    print("  Playwright is not installed. Trying next method...")
except Exception as e:
    print(f"  Playwright failed: {e}. Trying next method...")

# Method 3: pdfkit (wkhtmltopdf wrapper)
try:
    print("Attempting to generate PDF using pdfkit...")
    import pdfkit
    options = {
        'page-size': 'Letter',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'enable-local-file-access': None,
        'quiet': ''
    }
    pdfkit.from_file(html_file, pdf_file, options=options)
    print(f"Success! PDF generated successfully: '{pdf_file}' using pdfkit.")
    sys.exit(0)
except ImportError:
    print("  pdfkit is not installed.")
except Exception as e:
    print(f"  pdfkit failed: {e}")

# Manual Fallback Instructions
print("\n" + "="*60)
print("ALERT: AUTOMATED PDF GENERATION REQUIREMENT DETAILS")
print("="*60)
print("To generate the PDF using this Python script, please install one of these options:")
print("Option A (WeasyPrint):   pip install weasyprint")
print("Option B (Playwright):   pip install playwright && playwright install chromium")
print("Option C (pdfkit):       pip install pdfkit (requires wkhtmltopdf installed on your OS)")
print("\nOR USE THE MANUAL BROWSER METHOD (100% pixel-perfect and instant):")
print(f"1. Open the file '{os.path.abspath(html_file)}' in Google Chrome, Microsoft Edge, or Safari.")
print("2. Press Ctrl+P (Windows) or Cmd+P (Mac) to open the print dialog.")
print("3. Configure the following Print Settings:")
print("   - Destination: Save as PDF")
print("   - Pages: All (will automatically fit on exactly 1 page)")
print("   - Layout: Portrait")
print("   - Paper size: Letter")
print("   - Margins: None (IMPORTANT - to let the design margins take over)")
print("   - Background graphics: Enabled (check this box to render the background template and logos)")
print("4. Click 'Save' and name it 'Reconocimiento_Don_Fermin_Iribarren.pdf'.")
print("="*60 + "\n")
