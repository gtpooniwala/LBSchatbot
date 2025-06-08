#!/usr/bin/env python3
"""
Alternative PDF extraction approach using different methods
"""

import os
import PyPDF2
import pdfplumber

def extract_with_pyld2_detailed(pdf_path):
    """Try more detailed PyPDF2 extraction"""
    print(f"Detailed PyPDF2 extraction of: {pdf_path}")
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""
            
            for i, page in enumerate(reader.pages):
                print(f"Processing page {i+1}/{len(reader.pages)}")
                
                # Try different extraction methods
                text = page.extract_text()
                
                if text and len(text.strip()) > 10:
                    # Clean up the text
                    lines = text.split('\n')
                    cleaned_lines = []
                    
                    for line in lines:
                        line = line.strip()
                        # Skip lines that are mostly dots or numbers
                        if line and len(line) > 5 and not line.replace('.', '').replace(' ', '').isdigit():
                            if not all(c in '.… ' for c in line):
                                cleaned_lines.append(line)
                    
                    if cleaned_lines:
                        full_text += f"\n\n=== PAGE {i+1} ===\n"
                        full_text += '\n'.join(cleaned_lines)
                        print(f"  Found {len(cleaned_lines)} useful lines")
                    else:
                        print(f"  Page {i+1}: No useful content found")
                else:
                    print(f"  Page {i+1}: No text extracted")
            
            return full_text.strip()
    
    except Exception as e:
        print(f"PyPDF2 detailed extraction failed: {e}")
        return None

def extract_with_pdfplumber_detailed(pdf_path):
    """Try more detailed pdfplumber extraction"""
    print(f"Detailed pdfplumber extraction of: {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            
            for i, page in enumerate(pdf.pages):
                print(f"Processing page {i+1}/{len(pdf.pages)}")
                
                # Try extracting text with different settings
                text = page.extract_text()
                
                if text and len(text.strip()) > 10:
                    # Clean up the text
                    lines = text.split('\n')
                    cleaned_lines = []
                    
                    for line in lines:
                        line = line.strip()
                        # Skip lines that are mostly dots, numbers, or very short
                        if (len(line) > 5 and 
                            not line.replace('.', '').replace(' ', '').replace('…', '').isdigit() and
                            not all(c in '.… ' for c in line) and
                            len(line.replace('.', '').replace(' ', '').replace('…', '')) > 3):
                            cleaned_lines.append(line)
                    
                    if cleaned_lines:
                        full_text += f"\n\n=== PAGE {i+1} ===\n"
                        full_text += '\n'.join(cleaned_lines)
                        print(f"  Found {len(cleaned_lines)} useful lines")
                    else:
                        print(f"  Page {i+1}: No useful content after cleaning")
                        # Show what was found for debugging
                        if text:
                            sample = text[:200] + "..." if len(text) > 200 else text
                            print(f"  Raw sample: {repr(sample)}")
                else:
                    print(f"  Page {i+1}: No text extracted")
                    
                # Also try extracting tables
                try:
                    tables = page.extract_tables()
                    if tables:
                        print(f"  Found {len(tables)} tables on page {i+1}")
                        for j, table in enumerate(tables):
                            if table:
                                full_text += f"\n\n=== PAGE {i+1} TABLE {j+1} ===\n"
                                for row in table:
                                    if row and any(cell and str(cell).strip() for cell in row):
                                        row_text = " | ".join(str(cell).strip() if cell else "" for cell in row)
                                        if len(row_text.strip()) > 5:
                                            full_text += row_text + "\n"
                except Exception as e:
                    print(f"  Table extraction failed for page {i+1}: {e}")
            
            return full_text.strip()
    
    except Exception as e:
        print(f"pdfplumber detailed extraction failed: {e}")
        return None

def main():
    backend_data_dir = "/Users/gauravpooniwala/Documents/code/projects/LBSChatbot/generative-ai-chatbot/backend/data"
    
    pdfs = [
        "Academic Regulations (v2024-1.0).pdf",
        "Extenuating Circumstances Policy (v2024-1.0).pdf"
    ]
    
    for pdf in pdfs:
        pdf_path = os.path.join(backend_data_dir, pdf)
        
        print(f"\n{'='*80}")
        print(f"PROCESSING: {pdf}")
        print(f"{'='*80}")
        
        # Try both methods
        text_pdfplumber = extract_with_pdfplumber_detailed(pdf_path)
        text_pypdf2 = extract_with_pyld2_detailed(pdf_path)
        
        # Choose the better result
        if text_pdfplumber and len(text_pdfplumber) > len(text_pypdf2 or ""):
            final_text = text_pdfplumber
            method = "pdfplumber"
        elif text_pypdf2:
            final_text = text_pypdf2
            method = "PyPDF2"
        else:
            print(f"❌ No useful content extracted from {pdf}")
            continue
        
        print(f"\n✅ Best result from {method}: {len(final_text)} characters")
        
        # Save the result
        output_name = pdf.replace('.pdf', '_real_content.txt').replace(' ', '_').replace('(', '').replace(')', '').lower()
        output_path = os.path.join(backend_data_dir, output_name)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {pdf.replace('.pdf', '')} - Real Content\n")
            f.write(f"# Extracted using: {method}\n")
            f.write(f"# Character count: {len(final_text)}\n")
            f.write(f"# Date: {os.popen('date').read().strip()}\n\n")
            f.write(final_text)
        
        print(f"💾 Saved to: {output_name}")
        
        # Show preview
        preview_lines = final_text.split('\n')[:10]
        print(f"\n📋 Preview:")
        print("-" * 60)
        for line in preview_lines:
            if line.strip():
                print(line[:80] + ("..." if len(line) > 80 else ""))
        print("-" * 60)

if __name__ == "__main__":
    main()
