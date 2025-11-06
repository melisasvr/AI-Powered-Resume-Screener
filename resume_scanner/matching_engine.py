import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple

class MatchingEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2), stop_words='english')
        self.weights = {
            'skills': 0.40,
            'experience': 0.25,
            'education': 0.15,
            'semantic': 0.20
        }
        self.education_levels = {
            'phd': 5,
            'masters': 4,
            'bachelors': 3,
            'associate': 2,
            'high_school': 1,
            'unknown': 0
        }

    def calculate_skill_score(self, resume_skills: List[str], required_skills: List[str], preferred_skills: List[str]) -> float:
        resume_lower = [s.lower() for s in resume_skills]
        required_lower = [s.lower() for s in required_skills]
        preferred_lower = [s.lower() for s in preferred_skills]

        required_matches = sum(1 for skill in required_lower if skill in resume_lower)
        preferred_matches = sum(1 for skill in preferred_lower if skill in resume_lower)

        if len(required_skills) == 0:
            required_score = 1.0
        else:
            required_score = required_matches / len(required_skills)

        if len(preferred_skills) == 0:
            preferred_bonus = 0.0
        else:
            preferred_bonus = (preferred_matches / len(preferred_skills)) * 0.2  # Preferred adds up to 0.2 bonus

        total_score = min(required_score + preferred_bonus, 1.0)
        return total_score

    def calculate_experience_score(self, candidate_experience: float, required_experience: int) -> float:
        if required_experience == 0:
            return 1.0
        if candidate_experience >= required_experience:
            # Bonus for extra experience capped at 20% extra
            bonus = min((candidate_experience - required_experience) / required_experience * 0.2, 0.2)
            return min(1.0, 1.0 + bonus)
        else:
            return candidate_experience / required_experience  # Partial credit

    def calculate_education_score(self, candidate_education: str, required_education: str) -> float:
        candidate_level = self.education_levels.get(candidate_education.lower(), 0)
        required_level = self.education_levels.get(required_education.lower(), 0)

        if required_level == 0:
            return 1.0  # No requirement
        if candidate_level >= required_level:
            return 1.0
        elif candidate_level == required_level - 1:
            return 0.7
        elif candidate_level > 0:
            return 0.4
        else:
            return 0.0

    def calculate_semantic_score(self, resume_text: str, job_description: str) -> float:
        try:
            documents = [resume_text, job_description]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            return 0.0

    def calculate_overall_score(self, resume_data: Dict, job_requirements: Dict) -> Dict[str, float]:
        resume_skills = resume_data.get('skills', [])
        required_skills = job_requirements.get('required_skills', [])
        preferred_skills = job_requirements.get('preferred_skills', [])
        candidate_experience = resume_data.get('years_experience', 0)
        required_experience = job_requirements.get('min_experience', 0)
        candidate_education = resume_data.get('education_level', 'unknown')
        required_education = job_requirements.get('education_requirement', 'not_specified')
        resume_text = resume_data.get('raw_text', '')
        job_description = job_requirements.get('description', '')

        skill_score = self.calculate_skill_score(resume_skills, required_skills, preferred_skills)
        experience_score = self.calculate_experience_score(candidate_experience, required_experience)
        education_score = self.calculate_education_score(candidate_education, required_education)
        semantic_score = self.calculate_semantic_score(resume_text, job_description)

        overall_score = (skill_score * self.weights['skills'] +
                         experience_score * self.weights['experience'] +
                         education_score * self.weights['education'] +
                         semantic_score * self.weights['semantic'])
        overall_score = min(overall_score, 1.0)

        return {
            'overall_score': overall_score,
            'skill_score': skill_score,
            'experience_score': experience_score,
            'education_score': education_score,
            'semantic_score': semantic_score
        }

    def generate_match_explanations(self, scores: Dict[str, float]) -> str:
        explanations = []
        # Skill explanation
        if scores['skill_score'] >= 0.8:
            explanations.append("Excellent skill match")
        elif scores['skill_score'] >= 0.6:
            explanations.append("Good skill match")
        else:
            explanations.append("Partial skill match")

        # Experience explanation
        if scores['experience_score'] >= 0.9:
            explanations.append("Exceeds experience requirement")
        elif scores['experience_score'] >= 0.7:
            explanations.append("Meets experience requirement")
        else:
            explanations.append("Below experience requirement")

        # Education explanation
        if scores['education_score'] >= 0.9:
            explanations.append("Meets education requirement")

        return "\n".join(explanations)

    def print_scorecard(self, candidate_name: str, job_title: str, scores: Dict[str, float], explanation: str):
        print("\n--- Resume Match Scorecard ---")
        print(f"Candidate: {candidate_name}")
        print(f"Job:       {job_title}")
        print("\n--- Scores (Max 1.0) ---")
        print(f"  Overall Score:    {scores['overall_score']:.3f}")
        print(f"  Skills Match:     {scores['skill_score']:.3f}")
        print(f"  Experience Match: {scores['experience_score']:.3f}")
        print(f"  Education Match:  {scores['education_score']:.3f}")
        print(f"  Semantic Match:   {scores['semantic_score']:.3f}")
        print("\n--- Match Explanation ---")
        print(explanation)
        print("---------------------------------")

if __name__ == "__main__":
    engine = MatchingEngine()

    # Sample resume data (example candidate)
    sample_resume = {
        'skills': ['Python', 'Django', 'PostgreSQL', 'AWS'],
        'years_experience': 6,
        'education_level': 'bachelors',
        'raw_text': "Experienced Python developer with Django"
    }

    # List of job descriptions to run against
    jobs = [
        {
            "title": "Senior Python Developer",
            "required_skills": ['python', 'django', 'sql'],
            "preferred_skills": ['aws', 'docker'],
            "min_experience": 5,
            "education_requirement": "bachelors",
            "description": "Looking for a Python developer with Django, SQL skills, AWS and Docker experience."
        },
        {
            "title": "Junior Python Developer",
            "required_skills": ['python', 'django', 'sql'],
            "preferred_skills": ['aws', 'machine learning'],
            "min_experience": 2,
            "education_requirement": "bachelors",
            "description": "Junior Python Developer with knowledge of Django, SQL, AWS, and machine learning."
        },
        {
            "title": "Senior AI Engineer",
            "required_skills": ['machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch'],
            "preferred_skills": ['aws', 'azure', 'big data'],
            "min_experience": 8,
            "education_requirement": "masters",
            "description": "Senior AI Engineer experienced in ML, deep learning, NLP, TensorFlow, and PyTorch, with knowledge of AWS or Azure."
        },
        {
            "title": "Software Engineer",
            "required_skills": ['java', 'javascript', 'python', 'react', 'microservices'],
            "preferred_skills": ['docker', 'kubernetes', 'communication'],
            "min_experience": 3,
            "education_requirement": "bachelors",
            "description": "Software Engineer proficient in Java, JavaScript, Python, React, microservices, with familiarity in Docker and Kubernetes."
        }
    ]

    candidate_name = "Sample Candidate"

    for job in jobs:
        scores = engine.calculate_overall_score(sample_resume, job)
        explanation = engine.generate_match_explanations(scores)
        engine.print_scorecard(candidate_name, job['title'], scores, explanation)
