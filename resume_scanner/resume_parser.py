"""
Resume Parser Module
Extracts text and structured information from resume files
"""

import re
import PyPDF2
import docx
from pathlib import Path
import json

class ResumeParser:
    def __init__(self):
        self.skills_keywords = self._load_skills_keywords()
        self.education_keywords = {
            'phd': ['phd', 'ph.d', 'doctorate', 'doctoral'],
            'masters': ['master', 'msc', 'ms', 'ma', 'mba', 'meng'],
            'bachelors': ['bachelor', 'bsc', 'bs', 'ba', 'beng', 'btech'],
            'associate': ['associate', 'diploma'],
            'high_school': ['high school', 'secondary', 'ged']
        }
    
    def _load_skills_keywords(self):
        """Load common technical skills"""
        return {
            'programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php',
                'swift', 'kotlin', 'go', 'rust', 'typescript', 'scala', 'r'
            ],
            'web': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django',
                'flask', 'spring', 'asp.net', 'express', 'jquery', 'bootstrap'
            ],
            'database': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis',
                'cassandra', 'dynamodb', 'sqlite', 'mariadb', 'nosql'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
                'terraform', 'ansible', 'git', 'ci/cd', 'devops'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'nlp', 'tensorflow',
                'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
                'tableau', 'power bi', 'spark', 'hadoop', 'data analysis'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical', 'project management', 'agile', 'scrum'
            ]
        }
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    def extract_text(self, file_path):
        """Extract text from resume file"""
        file_path = Path(file_path)
        if file_path.suffix.lower() == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def extract_email(self, text):
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text):
        """Extract phone number from text"""
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None
    
    def extract_name(self, text):
        """Extract candidate name (simple heuristic)"""
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 3 and len(line) < 50 and not '@' in line:
                words = line.split()
                if 2 <= len(words) <= 4:
                    return line
        return "Unknown"
    
    def extract_skills(self, text):
        """Extract technical skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in self.skills_keywords.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append({
                        'skill': skill,
                        'category': category
                    })
        
        return found_skills
    
    def extract_experience(self, text):
        """Extract years of experience"""
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'experience[:\s]*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*(?:of)?\s*experience'
        ]
        
        text_lower = text.lower()
        years = []
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            years.extend([int(m) for m in matches])
        
        return max(years) if years else 0
    
    def extract_education(self, text):
        """Extract highest education level"""
        text_lower = text.lower()
        
        for level, keywords in self.education_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        return 'unknown'
    
    def parse_resume(self, file_path):
        """Parse resume and extract all information"""
        text = self.extract_text(file_path)
        
        resume_data = {
            'file_path': str(file_path),
            'raw_text': text,
            'candidate_name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text),
            'years_experience': self.extract_experience(text),
            'education_level': self.extract_education(text)
        }
        
        return resume_data

if __name__ == "__main__":
    # Example usage
    parser = ResumeParser()
    # resume_data = parser.parse_resume('path/to/resume.pdf')
    # print(json.dumps(resume_data, indent=2))
