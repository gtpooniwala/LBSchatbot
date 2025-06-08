#!/usr/bin/env python3
"""
PDF Extraction Script for LBS Chatbot Knowledge Base
Extracts text content from Academic Regulations and Extenuating Circumstances Policy PDFs
"""

import os
import sys

try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("Required libraries not found. Installing...")
    os.system("pip install PyPDF2 pdfplumber")
    import PyPDF2
    import pdfplumber

def extract_with_pypdf2(pdf_path):
    """Extract text using PyPDF2 library"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text
            return text
    except Exception as e:
        print(f"PyPDF2 extraction failed: {e}")
        return None

def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber library (better for complex layouts)"""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text
        return text
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")
        return None

def extract_pdf_content(pdf_path):
    """Try multiple extraction methods"""
    print(f"Extracting content from: {pdf_path}")
    
    # Try pdfplumber first (usually better for complex PDFs)
    content = extract_with_pdfplumber(pdf_path)
    if content and len(content.strip()) > 100:
        print("✓ Successfully extracted with pdfplumber")
        return content
    
    # Fallback to PyPDF2
    content = extract_with_pypdf2(pdf_path)
    if content and len(content.strip()) > 100:
        print("✓ Successfully extracted with PyPDF2")
        return content
    
    print("✗ Failed to extract meaningful content")
    return None

def main():
    data_dir = "/Users/gauravpooniwala/Documents/code/projects/LBSChatbot/generative-ai-chatbot/backend/data"
    
    # PDF files to extract
    pdfs = [
        ("Academic Regulations (v2024-1.0).pdf", "academic_regulations_extracted.txt"),
        ("Extenuating Circumstances Policy (v2024-1.0).pdf", "extenuating_circumstances_extracted.txt")
    ]
    
    for pdf_filename, output_filename in pdfs:
        pdf_path = os.path.join(data_dir, pdf_filename)
        output_path = os.path.join(data_dir, output_filename)
        
        if not os.path.exists(pdf_path):
            print(f"✗ PDF not found: {pdf_path}")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_filename}")
        print(f"{'='*60}")
        
        content = extract_pdf_content(pdf_path)
        
        if content:
            # Clean up the content
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('---'):  # Remove page markers for final output
                    cleaned_lines.append(line)
            
            cleaned_content = '\n'.join(cleaned_lines)
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Extracted Content from {pdf_filename}\n")
                f.write(f"# Extraction Date: {os.popen('date').read().strip()}\n")
                f.write(f"# Source: {pdf_filename}\n\n")
                f.write(cleaned_content)
            
            print(f"✓ Content saved to: {output_filename}")
            print(f"✓ Extracted {len(cleaned_content)} characters")
            
            # Show preview
            preview = cleaned_content[:500] + "..." if len(cleaned_content) > 500 else cleaned_content
            print(f"\nPreview:\n{'-'*40}\n{preview}\n{'-'*40}")
        else:
            print(f"✗ Failed to extract content from {pdf_filename}")
    
    print(f"\n{'='*60}")
    print("PDF extraction complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
