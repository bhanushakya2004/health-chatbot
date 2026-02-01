import os
import tempfile
from typing import Optional
import pytesseract
from PIL import Image
import pdf2image
from pathlib import Path
import time
from app.utils.logger import info, error, log_ocr_processing

class OCRService:
    """Service for extracting text from documents using Tesseract OCR"""
    
    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        """Extract text from image file using OCR"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            error(f"Error extracting text from image: {e}", exc_info=True)
            return ""
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from PDF file using OCR (or fallback to direct extraction)"""
        try:
            # Try OCR method first (requires poppler)
            try:
                # Convert PDF pages to images
                images = pdf2image.convert_from_path(pdf_path)
                
                extracted_text = []
                for i, image in enumerate(images):
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        temp_path = temp_file.name
                        image.save(temp_path, 'PNG')
                    
                    # Extract text from image
                    text = pytesseract.image_to_string(image)
                    extracted_text.append(f"--- Page {i+1} ---\n{text}")
                    
                    # Clean up temp file
                    os.unlink(temp_path)
                
                return "\n\n".join(extracted_text).strip()
                
            except Exception as poppler_error:
                error(f"pdf2image failed (poppler may not be installed): {poppler_error}")
                info("Attempting direct text extraction using PyPDF2 as fallback...")
                
                # Fallback: Try direct text extraction without OCR
                try:
                    import PyPDF2
                    with open(pdf_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        text_parts = []
                        for i, page in enumerate(pdf_reader.pages):
                            page_text = page.extract_text()
                            if page_text.strip():
                                text_parts.append(f"--- Page {i+1} ---\n{page_text}")
                        
                        if text_parts:
                            info("Successfully extracted text using PyPDF2 fallback")
                            return "\n\n".join(text_parts).strip()
                        else:
                            error("PyPDF2 extracted empty text")
                            return ""
                            
                except ImportError:
                    error("PyPDF2 not installed - cannot use fallback")
                    raise Exception(
                        "PDF text extraction failed. Poppler is not installed and PyPDF2 fallback unavailable. "
                        "Please install Poppler: https://github.com/oschwartz10612/poppler-windows/releases/"
                    )
                except Exception as pypdf_error:
                    error(f"PyPDF2 fallback also failed: {pypdf_error}")
                    raise Exception(
                        "PDF text extraction failed with both OCR and direct extraction methods. "
                        "The PDF may be image-based and requires Poppler for OCR. "
                        "Download: https://github.com/oschwartz10612/poppler-windows/releases/"
                    )
                    
        except Exception as e:
            error(f"Error extracting text from PDF: {e}", exc_info=True)
            return ""
    
    @staticmethod
    def extract_text(file_path: str, file_type: str, document_id: str = None, doc_filename: str = None) -> Optional[str]:
        """
        Extract text from document based on file type
        
        Args:
            file_path: Path to the document
            file_type: MIME type of the file
            document_id: Optional document ID for logging
            doc_filename: Optional filename for logging (renamed to avoid LogRecord conflict)
        
        Returns:
            Extracted text or None if extraction fails
        """
        start_time = time.time()
        file_path = Path(file_path)
        
        if not file_path.exists():
            error(f"File not found: {file_path}", document_id=document_id)
            return None
        
        try:
            info(f"Starting OCR extraction for {doc_filename or file_path.name}", 
                 document_id=document_id, file_type=file_type)
            
            # Handle PDFs
            if 'pdf' in file_type.lower():
                text = OCRService.extract_text_from_pdf(str(file_path))
            # Handle images
            elif any(img_type in file_type.lower() for img_type in ['image', 'jpeg', 'jpg', 'png']):
                text = OCRService.extract_text_from_image(str(file_path))
            else:
                error(f"Unsupported file type: {file_type}", document_id=document_id)
                return None
            
            duration = time.time() - start_time
            
            if text and len(text.strip()) > 0:
                log_ocr_processing(
                    document_id=document_id or "unknown",
                    filename=doc_filename or file_path.name,
                    status="success",
                    duration=duration
                )
                info(f"OCR extraction successful: {len(text)} characters", 
                     document_id=document_id, duration=duration, chars=len(text))
                return text
            else:
                log_ocr_processing(
                    document_id=document_id or "unknown",
                    filename=doc_filename or file_path.name,
                    status="no_text",
                    duration=duration
                )
                info("OCR completed but no text found", document_id=document_id)
                return None
                
        except Exception as e:
            duration = time.time() - start_time
            log_ocr_processing(
                document_id=document_id or "unknown",
                filename=doc_filename or file_path.name,
                status="failed",
                duration=duration
            )
            error(f"OCR extraction failed: {str(e)}", exc_info=True, document_id=document_id)
            return None
