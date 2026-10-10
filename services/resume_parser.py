import os
import PyPDF2
from docx import Document
from werkzeug.utils import secure_filename
from typing import Tuple

class ResumeParser:
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ResumeParser.ALLOWED_EXTENSIONS
    
    @staticmethod
    def check_file_size(file_path: str) -> bool:
        """Check if file is within size limit"""
        return os.path.getsize(file_path) <= ResumeParser.MAX_FILE_SIZE
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_doc(file_path: str) -> str:
        """Extract text from DOC file using python-docx (limited support)"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from DOC: {str(e)}")
    
    @staticmethod
    def parse_resume(file_path: str) -> Tuple[str, str]:
        """
        Parse resume file and extract text
        Returns: (success_message, text_content) or (error_message, empty_string)
        """
        try:
            # Check file size
            if not ResumeParser.check_file_size(file_path):
                return ("File size exceeds 5MB limit", "")
            
            # Get file extension
            file_ext = file_path.rsplit('.', 1)[1].lower()
            
            # Extract text based on file type
            if file_ext == 'pdf':
                text = ResumeParser.extract_text_from_pdf(file_path)
            elif file_ext in ['docx', 'doc']:
                text = ResumeParser.extract_text_from_docx(file_path)
            else:
                return ("Unsupported file format", "")
            
            if not text or len(text.strip()) == 0:
                return ("Could not extract text from resume", "")
            
            return ("Resume parsed successfully", text)
        
        except Exception as e:
            return (f"Error parsing resume: {str(e)}", "")
    
    @staticmethod
    def save_uploaded_file(file, upload_folder: str) -> Tuple[bool, str]:
        """
        Save uploaded file safely
        Returns: (success, filename_or_error)
        """
        try:
            if not file or file.filename == '':
                return (False, "No file provided")
            
            if not ResumeParser.allowed_file(file.filename):
                return (False, "File type not allowed. Use PDF, DOC, or DOCX")
            
            filename = secure_filename(file.filename)
            # Add timestamp to prevent filename conflicts
            import time
            filename = f"{int(time.time())}_{filename}"
            
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            return (True, file_path)
        
        except Exception as e:
            return (False, f"Error saving file: {str(e)}")
