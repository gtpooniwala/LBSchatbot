#!/usr/bin/env python3
"""
PDF Content Extraction Tool for LBS RAG Chatbot
Extracts text content from Academic Regulations and Extenuating Circumstances Policy PDFs
and formats them for the knowledge base.
"""

import os
import sys
import argparse

try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("Installing required libraries...")
    os.system("pip install PyPDF2 pdfplumber")
    import PyPDF2
    import pdfplumber

def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber (better formatting)"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text
            return text
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")
        return None

def extract_with_pypdf2(pdf_path):
    """Extract text using PyPDF2 (fallback method)"""
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

def clean_text(text):
    """Clean extracted text for better readability"""
    if not text:
        return ""
    
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line and len(line) > 1:  # Skip empty lines and single characters
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def extract_pdf(pdf_path, output_path=None):
    """Extract content from a PDF file"""
    print(f"Extracting content from: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    
    # Try pdfplumber first (better formatting)
    text = extract_with_pdfplumber(pdf_path)
    
    # Fallback to PyPDF2 if pdfplumber fails
    if not text:
        print("Trying PyPDF2 as fallback...")
        text = extract_with_pypdf2(pdf_path)
    
    if not text:
        print("Failed to extract text with both methods")
        return False
    
    # Clean the text
    cleaned_text = clean_text(text)
    
    # Generate output path if not provided
    if not output_path:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"{base_name}_extracted.txt"
    
    # Save extracted text
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        print(f"✅ Extraction successful!")
        print(f"📄 Output saved to: {output_path}")
        print(f"📊 Extracted {len(cleaned_text)} characters")
        return True
        
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def main():
    """Main extraction function"""
    parser = argparse.ArgumentParser(description='Extract text from PDF files for LBS RAG Chatbot')
    parser.add_argument('pdf_path', help='Path to the PDF file to extract')
    parser.add_argument('-o', '--output', help='Output text file path (optional)')
    
    args = parser.parse_args()
    
    success = extract_pdf(args.pdf_path, args.output)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
