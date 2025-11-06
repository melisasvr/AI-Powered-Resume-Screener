# 🤖 AI-Powered Resume Screener
- An intelligent system built in Python to process, analyze, and rank candidate resumes against specific job descriptions using skill matching, experience scoring, and semantic similarity.

## 🚀 Key Features
- Resume Parsing: Extracts text, name, email, phone, skills, experience, and education from PDF and DOCX files.
- Job Analysis: Extracts required skills, preferred skills, and minimum experience/education from job postings.
- Intelligent Matching: Calculates an Overall Score based on weighted factors: Skills, Experience, Education, and Semantic Similarity (using TF-IDF).
- Database Integration: Uses SQLite (or optionally PostgreSQL) to manage job postings, processed resumes, and final rankings.
- Configuration: Highly configurable scoring weights, skills keywords, and database settings via config.py.
- Multi-Factor Scoring: Evaluate candidates on skills, experience, education, and semantic similarity
- SQL Database: Store and query resume data efficiently
- Batch Processing: Handle 1000+ resumes efficiently
-  Export Results: Generate CSV reports and JSON summaries
## 📂 Project Structure
```
resume_screener/
├── __init__.py         # Makes 'resume_scanner' a Python package
├── resume_parser.py    # Extract data from resumes
├── job_analyzer.py     # Analyze job descriptions
├── matching_engine.py   # Score and rank candidates
├── database_manager.py  # Database operations
├── main_application.py  # Main orchestration
├── schema.sql           # Database schema
├── requirements.txt     # Python dependencies
├── config.py           # System configuration settings
```
## 🛠️ Installation

### 1. Clone or Download the Project

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Set Up Database

The database will be created automatically on the first run. The SQL schema is in `schema.sql`.

## 💻 Usage

### Quick Start

```python
from main_application import ResumeScreener

# Initialize the screener
screener = ResumeScreener()

# Add a job posting
job_description = """
Senior Python Developer

Requirements:
- 5+ years of Python experience
- Django or Flask expertise
- SQL database knowledge
- Bachelor's degree

Preferred:
- AWS experience
- Docker knowledge
"""

job_id = screener.add_job_posting("Senior Python Developer", job_description)

# Process resumes from a folder
resumes = screener.batch_process_resumes('./resumes')

# Rank resumes
screener.rank_resumes_for_job(job_id, resumes)

# Display top 10 candidates
screener.display_top_candidates(job_id, top_n=10)

# Export results
screener.export_results(job_id, 'results.csv')

# Generate report
screener.generate_report(job_id)

screener.close()
```

### Command Line Usage

```python
# Run the main application
python main_application.py
```

## 📊 Scoring Algorithm

The system uses a weighted scoring approach:

- **Skills Match (40%)**: Matches required and preferred skills
- **Experience (25%)**: Compares years of experience
- **Education (15%)**: Evaluates education level
- **Semantic Similarity (20%)**: TF-IDF cosine similarity

### Score Calculation Example

```
Overall Score = (Skills × 0.40) + (Experience × 0.25) + 
                (Education × 0.15) + (Semantic × 0.20)
```

## 🗄️ Database Schema
### Main Tables
1. **job_postings**: Store job information
1. **resumes**: Store candidate resumes
1. **resume_rankings**: Store matching scores and ranks
1. **candidate_skills**: Store extracted skills per candidate
1. **job_skills**: Store required/preferred skills per job
   
## 📝 Input Requirements
### Resume Files
- Supported formats: PDF, DOCX
- Recommended: Place all resumes in a single folder
- Files should contain clear text (not scanned images)

### Job Descriptions
- Plain text format
- Clearly separate required vs preferred skills
- Include experience and education requirements

## 📊 Performance

- **Processing Speed**: ~2-5 resumes per second
- **Scalability**: Tested with 1000+ resumes
- **Memory**: ~100MB for 1000 resumes
- **Database**: SQLite handles 10,000+ records efficiently

## 🐛 Troubleshooting
### PDF Extraction Fails
- Try alternative library: `pdfplumber` instead of `PyPDF2`
- Ensure PDFs contain actual text (not images)

### Low Matching Scores
- Check if skills keywords are in your skills database
- Adjust scoring weights
- Review job description clarity

### Database Locked Error
- Close any open database connections
- Use context manager: `with DatabaseManager() as db:`


## 🤝 Contributing
- Contributions welcome! Areas for improvement:
- Better NLP models
- More robust parsing
- Additional export formats
- Performance optimizations

## 📧 Support
- If you have any issues or questions, please refer to the code comments and documentation.

## ⚠️ Important Notes
1. **Privacy**: Handle resume data responsibly and comply with GDPR/privacy laws
1. **Bias**: Regularly audit for algorithmic bias in scoring
1. **Accuracy**: Manual review of top candidates is still recommended
1. **Testing**: Test with diverse resume formats before production use

-----

**Version**: 1.0  
**Last Updated**: November 2025
