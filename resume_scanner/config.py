"""
Configuration file for Resume Screener
Adjust these settings to customize the system behavior
"""

# ==================== DATABASE SETTINGS ====================
DATABASE_CONFIG = {
    'type': 'sqlite',  # Options: 'sqlite', 'postgresql'
    'sqlite_path': 'resume_screener.db',
    
    # PostgreSQL settings (if using PostgreSQL)
    'postgresql': {
        'host': 'localhost',
        'port': 5432,
        'database': 'resume_screener',
        'user': 'your_username',
        'password': 'your_password'
    }
}

# ==================== SCORING WEIGHTS ====================
SCORING_WEIGHTS = {
    'skills': 0.40,        # Weight for skills matching
    'experience': 0.25,    # Weight for experience matching
    'education': 0.15,     # Weight for education matching
    'semantic': 0.20       # Weight for semantic similarity
}

# Adjust these if certain factors are more important for your use case
# Example for entry-level positions:
# SCORING_WEIGHTS = {
#     'skills': 0.35,
#     'experience': 0.15,
#     'education': 0.30,
#     'semantic': 0.20
# }

# ==================== SKILLS CONFIGURATION ====================
# Add your custom technical skills here
CUSTOM_SKILLS = {
    'programming_languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 
        'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'perl'
    ],
    
    'web_frameworks': [
        'react', 'angular', 'vue', 'svelte', 'next.js', 'node.js',
        'django', 'flask', 'fastapi', 'spring', 'asp.net', 'express',
        'laravel', 'ruby on rails'
    ],
    
    'databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle',
        'cassandra', 'dynamodb', 'sqlite', 'mariadb', 'elasticsearch',
        'neo4j', 'couchdb'
    ],
    
    'cloud_devops': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
        'terraform', 'ansible', 'git', 'github', 'gitlab', 'ci/cd',
        'devops', 'circleci', 'travis ci'
    ],
    
    'data_science_ml': [
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas',
        'numpy', 'matplotlib', 'seaborn', 'tableau', 'power bi',
        'spark', 'hadoop', 'data analysis', 'statistical analysis'
    ],
    
    'mobile_development': [
        'android', 'ios', 'react native', 'flutter', 'xamarin',
        'swift', 'kotlin', 'objective-c'
    ],
    
    'testing_qa': [
        'selenium', 'junit', 'pytest', 'jest', 'mocha', 'cypress',
        'test automation', 'unit testing', 'integration testing'
    ],
    
    'soft_skills': [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'analytical', 'project management', 'agile', 'scrum', 'kanban',
        'time management', 'mentoring', 'stakeholder management'
    ],
    
    'certifications': [
        'aws certified', 'azure certified', 'pmp', 'scrum master',
        'cissp', 'ceh', 'comptia', 'ccna', 'cka', 'ckad'
    ]
}

# ==================== EDUCATION LEVELS ====================
EDUCATION_HIERARCHY = {
    'phd': 5,
    'doctorate': 5,
    'masters': 4,
    'mba': 4,
    'bachelors': 3,
    'associate': 2,
    'diploma': 2,
    'high_school': 1,
    'unknown': 0
}

# ==================== PARSING SETTINGS ====================
PARSING_CONFIG = {
    'supported_formats': ['.pdf', '.docx', '.doc'],
    'max_file_size_mb': 10,  # Maximum file size in MB
    'extract_images': False,  # Extract images from resumes
    'ocr_enabled': False,     # Enable OCR for scanned PDFs (requires additional setup)
}

# ==================== MATCHING SETTINGS ====================
MATCHING_CONFIG = {
    'min_match_threshold': 0.0,  # Minimum score to consider (0.0 = all candidates)
    'required_skills_weight': 1.0,  # Weight for required skills
    'preferred_skills_weight': 0.5, # Weight for preferred skills
    'experience_bonus_threshold': 2,  # Years above requirement for bonus
    'experience_bonus_max': 0.2,      # Maximum bonus for extra experience
}

# ==================== TF-IDF SETTINGS ====================
TFIDF_CONFIG = {
    'max_features': 500,       # Maximum number of features
    'ngram_range': (1, 2),     # Consider unigrams and bigrams
    'min_df': 1,               # Minimum document frequency
    'max_df': 0.8,             # Maximum document frequency
    'stop_words': 'english'    # Language for stop words
}

# ==================== OUTPUT SETTINGS ====================
OUTPUT_CONFIG = {
    'default_top_n': 10,           # Default number of top candidates to show
    'export_format': 'csv',        # Default export format: 'csv' or 'json'
    'include_resume_text': False,  # Include full text in exports
    'decimal_places': 3,           # Decimal places for scores
}

# ==================== PERFORMANCE SETTINGS ====================
PERFORMANCE_CONFIG = {
    'batch_size': 100,          # Process resumes in batches
    'enable_caching': True,     # Cache parsed resumes
    'parallel_processing': False,  # Enable multiprocessing (experimental)
    'max_workers': 4,           # Number of parallel workers
}

# ==================== LOGGING SETTINGS ====================
LOGGING_CONFIG = {
    'enabled': True,
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'log_file': 'resume_screener.log',
    'log_to_console': True,
}

# ==================== VALIDATION RULES ====================
VALIDATION_RULES = {
    'require_email': False,         # Require email in resume
    'require_phone': False,         # Require phone in resume
    'min_resume_length': 100,       # Minimum characters in resume
    'max_resume_length': 50000,     # Maximum characters in resume
}

# ==================== ADVANCED FEATURES ====================
ADVANCED_FEATURES = {
    'use_semantic_embeddings': False,  # Use BERT/transformers (requires more resources)
    'detect_duplicates': True,          # Detect duplicate candidates
    'extract_certifications': True,     # Extract certifications
    'extract_languages': True,          # Extract spoken languages
    'location_matching': False,         # Match candidate location with job
}

# ==================== API SETTINGS (if building API) ====================
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
    'rate_limit': '100/hour',  # Rate limiting
}

# ==================== HELPER FUNCTIONS ====================

def get_config(section: str = None):
    """Get configuration for a specific section"""
    configs = {
        'database': DATABASE_CONFIG,
        'scoring': SCORING_WEIGHTS,
        'skills': CUSTOM_SKILLS,
        'education': EDUCATION_HIERARCHY,
        'parsing': PARSING_CONFIG,
        'matching': MATCHING_CONFIG,
        'tfidf': TFIDF_CONFIG,
        'output': OUTPUT_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'logging': LOGGING_CONFIG,
        'validation': VALIDATION_RULES,
        'advanced': ADVANCED_FEATURES,
        'api': API_CONFIG,
    }
    
    if section:
        return configs.get(section, {})
    return configs

def update_config(section: str, key: str, value):
    """Update a configuration value"""
    # This is a simple implementation
    # In production, you might want to persist changes
    configs = get_config()
    if section in configs and key in configs[section]:
        configs[section][key] = value
        return True
    return False

# ==================== ENVIRONMENT-SPECIFIC CONFIGS ====================

# Development
DEV_CONFIG = {
    'debug': True,
    'log_level': 'DEBUG',
    'sample_size': 10,  # Process only 10 resumes for testing
}

# Production
PROD_CONFIG = {
    'debug': False,
    'log_level': 'INFO',
    'sample_size': None,  # Process all resumes
    'enable_monitoring': True,
}

# Get current environment (default to development)
import os
ENVIRONMENT = os.getenv('ENV', 'development')

if ENVIRONMENT == 'production':
    ACTIVE_CONFIG = PROD_CONFIG
else:
    ACTIVE_CONFIG = DEV_CONFIG

# ==================== USAGE EXAMPLE ====================
if __name__ == "__main__":
    import json
    
    print("Current Configuration:")
    print(json.dumps(get_config('scoring'), indent=2))
    
    print("\nAll Custom Skills:")
    for category, skills in CUSTOM_SKILLS.items():
        print(f"\n{category.upper()}: {len(skills)} skills")
        print(f"  {', '.join(skills[:5])}...")