"""
Main Application - AI-Powered Resume Screener
Orchestrates all components to process and rank resumes
"""

import os
from pathlib import Path
from typing import List, Dict
import time
from tqdm import tqdm
import json

# Import custom modules
from resume_scanner.resume_parser import ResumeParser
from resume_scanner.job_analyzer import JobAnalyzer
from resume_scanner.matching_engine import MatchingEngine
from resume_scanner.database_manager import DatabaseManager

class ResumeScreener:
    def __init__(self, db_path: str = 'resume_screener.db'):
        """Initialize the resume screening system"""
        self.parser = ResumeParser()
        self.job_analyzer = JobAnalyzer()
        self.matching_engine = MatchingEngine()
        self.db = DatabaseManager(db_path)
        
        print("✓ Resume Screener initialized successfully")
    
    def add_job_posting(self, title: str, description: str) -> int:
        """Add a new job posting and analyze it"""
        print(f"\n📋 Analyzing job posting: {title}")
        
        # Analyze job description
        job_analysis = self.job_analyzer.analyze_job(title, description)
        
        # Insert into database
        job_id = self.db.insert_job_posting(job_analysis)
        
        # Insert job skills
        self.db.insert_job_skills(
            job_id,
            job_analysis['required_skills'],
            job_analysis['preferred_skills']
        )
        
        print(f"✓ Job posted with ID: {job_id}")
        print(f"  Required skills: {len(job_analysis['required_skills'])}")
        print(f"  Preferred skills: {len(job_analysis['preferred_skills'])}")
        print(f"  Min experience: {job_analysis['min_experience']} years")
        
        return job_id
    
    def process_resume(self, file_path: str) -> Dict:
        """Process a single resume"""
        try:
            resume_data = self.parser.parse_resume(file_path)
            return resume_data
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def batch_process_resumes(self, resume_folder: str) -> List[Dict]:
        """Process all resumes in a folder"""
        resume_folder = Path(resume_folder)
        
        if not resume_folder.exists():
            print(f"❌ Folder not found: {resume_folder}")
            return []
        
        # Find all resume files
        resume_files = []
        for ext in ['*.pdf', '*.docx', '*.doc']:
            resume_files.extend(resume_folder.glob(ext))
        
        print(f"\n📂 Found {len(resume_files)} resumes to process")
        
        processed_resumes = []
        
        # Process each resume with progress bar
        for file_path in tqdm(resume_files, desc="Processing resumes"):
            resume_data = self.process_resume(file_path)
            if resume_data:
                # Insert into database
                resume_id = self.db.insert_resume(resume_data)
                resume_data['resume_id'] = resume_id
                
                # Insert skills
                if resume_data.get('skills'):
                    self.db.insert_candidate_skills(resume_id, resume_data['skills'])
                
                processed_resumes.append(resume_data)
        
        print(f"✓ Successfully processed {len(processed_resumes)} resumes")
        return processed_resumes
    
    def rank_resumes_for_job(self, job_id: int, resumes: List[Dict] = None):
        """Rank all resumes for a specific job"""
        print(f"\n🎯 Ranking resumes for job ID: {job_id}")
        
        # Get job requirements
        job_data = self.db.get_job_posting(job_id)
        if not job_data:
            print(f"❌ Job {job_id} not found")
            return
        
        # If no resumes provided, get all from database
        if resumes is None:
            print("Loading resumes from database...")
            # In production, you'd query resumes from DB
            # For now, we'll use the provided resumes list
            print("⚠️  Please provide resumes list")
            return
        
        # Delete existing rankings for this job
        self.db.delete_rankings_for_job(job_id)
        
        # Rank all resumes
        print("Calculating match scores...")
        ranked_resumes = self.matching_engine.rank_resumes(resumes, job_data)
        
        # Insert rankings into database
        print("Saving rankings to database...")
        for resume, scores, rank in tqdm(ranked_resumes, desc="Saving rankings"):
            ranking_data = {
                'job_id': job_id,
                'resume_id': resume['resume_id'],
                'overall_score': scores['overall_score'],
                'skills_score': scores['skills_score'],
                'experience_score': scores['experience_score'],
                'education_score': scores['education_score'],
                'semantic_score': scores['semantic_score'],
                'rank_position': rank
            }
            self.db.insert_resume_ranking(ranking_data)
        
        print(f"✓ Ranked {len(ranked_resumes)} resumes")
        
        return ranked_resumes
    
    def get_top_candidates(self, job_id: int, top_n: int = 10) -> List[Dict]:
        """Get top N candidates for a job"""
        candidates = self.db.get_top_candidates(job_id, top_n)
        return candidates
    
    def display_top_candidates(self, job_id: int, top_n: int = 10):
        """Display top candidates in a readable format"""
        candidates = self.get_top_candidates(job_id, top_n)
        
        if not candidates:
            print("No candidates found")
            return
        
        print(f"\n{'='*80}")
        print(f"TOP {len(candidates)} CANDIDATES")
        print(f"{'='*80}\n")
        
        for candidate in candidates:
            print(f"Rank #{candidate['rank_position']}")
            print(f"Name: {candidate['candidate_name']}")
            print(f"Email: {candidate['email']}")
            print(f"Phone: {candidate.get('phone', 'N/A')}")
            print(f"Experience: {candidate['years_experience']} years")
            print(f"Education: {candidate['education_level']}")
            print(f"\nScores:")
            print(f"  Overall:    {candidate['overall_score']:.1%}")
            print(f"  Skills:     {candidate['skills_score']:.1%}")
            print(f"  Experience: {candidate['experience_score']:.1%}")
            print(f"  Education:  {candidate['education_score']:.1%}")
            print(f"  Semantic:   {candidate['semantic_score']:.1%}")
            print(f"{'-'*80}\n")
    
    def export_results(self, job_id: int, output_file: str = 'rankings.csv'):
        """Export rankings to CSV"""
        self.db.export_rankings_to_csv(job_id, output_file)
        print(f"✓ Results exported to {output_file}")
    
    def generate_report(self, job_id: int, output_file: str = 'screening_report.json'):
        """Generate comprehensive screening report"""
        job_data = self.db.get_job_posting(job_id)
        all_rankings = self.db.get_all_rankings_for_job(job_id)
        
        report = {
            'job_info': job_data,
            'total_candidates': len(all_rankings),
            'screening_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'top_10_candidates': all_rankings[:10],
            'statistics': {
                'avg_overall_score': sum(r['overall_score'] for r in all_rankings) / len(all_rankings),
                'avg_skills_score': sum(r['skills_score'] for r in all_rankings) / len(all_rankings),
                'avg_experience_score': sum(r['experience_score'] for r in all_rankings) / len(all_rankings),
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Report generated: {output_file}")
        return report
    
    def close(self):
        """Close database connection"""
        self.db.close()

# ==================== EXAMPLE USAGE ====================

def main():
    """Example workflow"""
    
    # Initialize screener
    screener = ResumeScreener()
    
    # Step 1: Add a job posting
    job_description = """
    Senior Python Developer
    
    We are seeking an experienced Python developer to join our team.
    
    Requirements:
    - 5+ years of Python development experience
    - Strong knowledge of Django or Flask
    - Experience with SQL databases (PostgreSQL, MySQL)
    - Bachelor's degree in Computer Science or related field
    - Experience with RESTful APIs
    
    Preferred:
    - AWS or Azure cloud experience
    - Docker and Kubernetes knowledge
    - Machine learning experience
    - Experience with microservices architecture
    """
    
    job_id = screener.add_job_posting("Senior Python Developer", job_description)
    
    # Step 2: Process resumes from a folder
    resumes = screener.batch_process_resumes('./resumes')
    
    # Step 3: Rank resumes for the job
    if resumes:
        screener.rank_resumes_for_job(job_id, resumes)
        
        # Step 4: Display top candidates
        screener.display_top_candidates(job_id, top_n=10)
        
        # Step 5: Export results
        screener.export_results(job_id, 'top_candidates.csv')
        
        # Step 6: Generate report
        screener.generate_report(job_id, 'screening_report.json')
    
    # Close connection
    screener.close()

if __name__ == "__main__":
    main()