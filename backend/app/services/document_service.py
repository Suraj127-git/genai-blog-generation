import PyPDF2
import docx
from typing import Optional
import logging
import io

logger = logging.getLogger(__name__)


class DocumentService:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
            
            logger.info(f"Extracted text from PDF: {len(text)} characters")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docx_file = io.BytesIO(file_content)
            doc = docx.Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            logger.info(f"Extracted text from DOCX: {len(text)} characters")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """Extract text from TXT file"""
        try:
            text = file_content.decode('utf-8')
            logger.info(f"Extracted text from TXT: {len(text)} characters")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {e}")
            raise ValueError(f"Failed to extract text from TXT: {str(e)}")
    
    @classmethod
    def extract_text(cls, file_content: bytes, file_type: str) -> str:
        """Extract text based on file type"""
        if file_type == "pdf":
            return cls.extract_text_from_pdf(file_content)
        elif file_type == "docx":
            return cls.extract_text_from_docx(file_content)
        elif file_type == "txt":
            return cls.extract_text_from_txt(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def create_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Split text into chunks for embedding"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks
    
    @staticmethod
    def get_content_preview(text: str, max_length: int = 200) -> str:
        """Get preview of content"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."


def get_document_service() -> DocumentService:
    """Get document service instance"""
    return DocumentService()
