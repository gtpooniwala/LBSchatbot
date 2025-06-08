#!/usr/bin/env python3
"""
Simple PDF extraction script for LBS Chatbot knowledge base
Extracts text from PDF files and saves to structured text files
"""

import os
import sys

def extract_with_pypdf2():
    """Extract using PyPDF2 (basic extraction)"""
    try:
        import PyPDF2
        return True, PyPDF2
    except ImportError:
        return False, None

def extract_with_pdfplumber():
    """Extract using pdfplumber (better formatting)"""
    try:
        import pdfplumber
        return True, pdfplumber
    except ImportError:
        return False, None

def clean_text(text):
    """Clean extracted text"""
    if not text:
        return ""
    
    # Basic cleaning
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line and len(line) > 3:  # Skip very short lines
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def extract_pdf_pypdf2(pdf_path):
    """Extract text using PyPDF2"""
    print(f"Extracting {pdf_path} using PyPDF2...")
    
    try:
        import PyPDF2
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"Found {len(reader.pages)} pages")
            
            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {i+1} ---\n"
                        text += page_text
                except Exception as e:
                    print(f"Error extracting page {i+1}: {e}")
                    continue
            
            return clean_text(text)
    
    except Exception as e:
        print(f"PyPDF2 extraction failed: {e}")
        return None

def extract_pdf_pdfplumber(pdf_path):
    """Extract text using pdfplumber"""
    print(f"Extracting {pdf_path} using pdfplumber...")
    
    try:
        import pdfplumber
        
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Found {len(pdf.pages)} pages")
            
            for i, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {i+1} ---\n"
                        text += page_text
                except Exception as e:
                    print(f"Error extracting page {i+1}: {e}")
                    continue
        
        return clean_text(text)
    
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")
        return None

def main():
    # Define paths
    backend_data_dir = "/Users/gauravpooniwala/Documents/code/projects/LBSChatbot/generative-ai-chatbot/backend/data"
    
    pdfs = [
        "Academic Regulations (v2024-1.0).pdf",
        "Extenuating Circumstances Policy (v2024-1.0).pdf"
    ]
    
    # Check if PDFs exist
    for pdf in pdfs:
        pdf_path = os.path.join(backend_data_dir, pdf)
        if not os.path.exists(pdf_path):
            print(f"ERROR: PDF not found: {pdf_path}")
            return 1
    
    # Check available extraction methods
    pypdf2_available, pypdf2_module = extract_with_pypdf2()
    pdfplumber_available, pdfplumber_module = extract_with_pdfplumber()
    
    if not pypdf2_available and not pdfplumber_available:
        print("ERROR: No PDF extraction libraries available. Please install:")
        print("pip install PyPDF2 pdfplumber")
        return 1
    
    print(f"Available extraction methods:")
    print(f"- PyPDF2: {'✓' if pypdf2_available else '✗'}")
    print(f"- pdfplumber: {'✓' if pdfplumber_available else '✗'}")
    
    # Extract each PDF
    for pdf in pdfs:
        pdf_path = os.path.join(backend_data_dir, pdf)
        output_name = pdf.replace('.pdf', '_extracted.txt').replace(' ', '_').replace('(', '').replace(')', '').lower()
        output_path = os.path.join(backend_data_dir, output_name)
        
        print(f"\n{'='*60}")
        print(f"Processing: {pdf}")
        print(f"Output: {output_name}")
        print(f"{'='*60}")
        
        # Try pdfplumber first (better formatting), then PyPDF2
        text = None
        
        if pdfplumber_available:
            text = extract_pdf_pdfplumber(pdf_path)
        
        if not text and pypdf2_available:
            print("Falling back to PyPDF2...")
            text = extract_pdf_pypdf2(pdf_path)
        
        if text:
            # Create structured output
            output_content = f"""# {pdf.replace('.pdf', '')} - Extracted Content
# Source: {pdf}
# Extracted on: {os.popen('date').read().strip()}
# Total length: {len(text)} characters

---

{text}

---
# End of {pdf.replace('.pdf', '')}
"""
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            print(f"✓ Successfully extracted {len(text)} characters")
            print(f"✓ Saved to: {output_path}")
            
            # Show preview
            preview = text[:500] + "..." if len(text) > 500 else text
            print(f"\nPreview:\n{'-'*40}")
            print(preview)
            print(f"{'-'*40}")
        
        else:
            print(f"✗ Failed to extract text from {pdf}")
    
    print(f"\n{'='*60}")
    print("Extraction complete!")
    print(f"{'='*60}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
