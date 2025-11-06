"""
Job Description Analyzer Module

Extracts requirements and key information from job descriptions
"""

import re
import json
from typing import Dict, List, Set

class JobAnalyzer:
    def __init__(self):
        self.skills_keywords = self._load_skills_keywords()
        self.experience_keywords = ['experience', 'years', 'yrs']
        self.education_keywords = {
            'phd': 5,
            'masters': 4,
            'bachelors': 3,
            'associate': 2,
            'high_school': 1
        }

    def _load_skills_keywords(self) -> Set[str]:
        """Load common technical skills"""
        return {
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php',
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django',
            'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'nosql',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'machine learning', 'deep learning', 'nlp', 'tensorflow',
            'agile', 'scrum', 'git', 'ci/cd', 'rest api', 'microservices',
            'leadership', 'communication', 'project management'
        }

    def extract_required_skills(self, job_description: str) -> Dict[str, List[str]]:
        """Extract required and preferred skills from job description"""
        text_lower = job_description.lower()
        required_skills = []
        preferred_skills = []

        required_section = self._extract_section(
            text_lower,
            ['required', 'requirements', 'must have', 'qualifications']
        )
        preferred_section = self._extract_section(
            text_lower,
            ['preferred', 'nice to have', 'plus', 'bonus']
        )

        for skill in self.skills_keywords:
            if skill.lower() in required_section:
                required_skills.append(skill)
            elif skill.lower() in preferred_section:
                preferred_skills.append(skill)
            elif skill.lower() in text_lower:
                if skill not in preferred_skills:
                    required_skills.append(skill)

        required_skills = [s for s in required_skills if s not in preferred_skills]

        return {
            'required': list(set(required_skills)),
            'preferred': list(set(preferred_skills))
        }

    def _extract_section(self, text: str, keywords: List[str]) -> str:
        """Extract a specific section from job description"""
        for keyword in keywords:
            pattern = rf'(?:^|\n)\s*{keyword}[:\s]+(.*?)(?=\n\s*\n|\Z)'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return ""

    def extract_experience_requirement(self, job_description: str) -> int:
        """Extract minimum years of experience required"""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'minimum\s*(?:of)?\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?',
            r'(\d+)\+?\s*yrs?'
        ]
        text_lower = job_description.lower()
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            years.extend([int(m) for m in matches])
        return min(years) if years else 0

    def extract_education_requirement(self, job_description: str) -> str:
        """Extract education requirement"""
        text_lower = job_description.lower()
        education_patterns = {
            'phd': [r'ph\.?d', r'doctorate', r'doctoral'],
            'masters': [r'master[\'s]*', r'msc', r'ms\b', r'ma\b', r'mba'],
            'bachelors': [r'bachelor[\'s]*', r'bsc', r'bs\b', r'ba\b', r'degree'],
            'associate': [r'associate', r'diploma'],
        }
        for level, patterns in education_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return level
        return 'not_specified'

    def identify_key_phrases(self, job_description: str) -> List[str]:
        """Extract key phrases and important terms"""
        text = job_description.lower()
        important_patterns = [
            r'strong ([\w\s-]+)',
            r'excellent ([\w\s-]+)',
            r'proven ([\w\s-]+)',
            r'experience (?:with|in) ([\w\s-]+)',
            r'knowledge of ([\w\s-]+)',
        ]
        key_phrases = []
        for pattern in important_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                phrase = m.strip()
                if 5 < len(phrase) < 50:
                    key_phrases.append(phrase)
        return list(set(key_phrases))[:20]

    def analyze_job(self, job_title: str, job_description: str) -> Dict:
        skills = self.extract_required_skills(job_description)
        analysis = {
            'title': job_title,
            'description': job_description,
            'required_skills': sorted(skills['required']),
            'preferred_skills': sorted(skills['preferred']),
            'min_experience': self.extract_experience_requirement(job_description),
            'education_requirement': self.extract_education_requirement(job_description),
            'key_phrases': sorted(self.identify_key_phrases(job_description))
        }
        return analysis

if __name__ == "__main__":
    analyzer = JobAnalyzer()

    jobs_to_analyze = [
        {
            "title": "Senior Python Developer",
            "description": """
Senior Python Developer

Requirements:
- 5+ years of experience in Python development
- Strong knowledge of Django and Flask
- Experience with SQL databases (PostgreSQL, MySQL)
- Bachelor's degree in Computer Science

Preferred:
- AWS experience
- Machine learning knowledge
"""
        },
        {
            "title": "Junior Python Developer",
            "description": """
Junior Python Developer

Requirements:
- 2+ years of experience in Python development
- Familiarity with Django and Flask
- Experience with SQL databases (PostgreSQL, MySQL)
- Bachelor's degree in Computer Science

Preferred:
- AWS experience
- Machine learning knowledge
"""
        },
        {
            "title": "Senior AI Engineer",
            "description": """
Senior AI Engineer

Requirements:
- 8+ years of experience in artificial intelligence development
- Strong skills in machine learning, deep learning, and NLP
- Experience with TensorFlow and PyTorch
- Master's degree preferred

Preferred:
- Experience with AWS or Azure
- Knowledge of big data technologies
"""
        },
        {
            "title": "Software Engineer",
            "description": """
Software Engineer

Requirements:
- 3+ years of experience in software development
- Proficient in Java, JavaScript, and Python
- Experience with React and Microservices
- Bachelor's degree required

Preferred:
- Familiarity with Docker and Kubernetes
- Good communication skills
"""
        }
    ]

    for job in jobs_to_analyze:
        result = analyzer.analyze_job(job['title'], job['description'])
        print(json.dumps(result, indent=4))
