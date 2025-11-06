import sqlite3
import json
from typing import List, Dict, Optional
from datetime import datetime
import os


class DatabaseManager:
    def __init__(self, dbpath: str = "resumescreener.db"):
        self.dbpath = dbpath
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dbpath)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print(f"Connected to database at {self.dbpath}")
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise

    def create_tables(self):
        schemafile = "schema.sql"
        if not os.path.exists(schemafile):
            print(f"Error: schema.sql file not found. Cannot create tables.")
            return
        try:
            with open(schemafile, "r") as f:
                schema = f.read()
            self.conn.executescript(schema)
            self.conn.commit()
            print("Database tables created or verified successfully.")
        except sqlite3.OperationalError as e:
            print(f"SQLite Operational Error during table creation: {e}")
            print("Check your schema.sql file for syntax errors.")
            raise e
        except Exception as e:
            print(f"Unexpected error during table creation: {e}")
            raise e

    def insert_job_posting(self, jobdata: Dict) -> int:
        query = '''INSERT INTO jobpostings 
                   (title, description, requiredskills, preferredskills, minexperience, educationlevel)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        try:
            required = json.dumps(jobdata.get('required_skills', []))
            preferred = json.dumps(jobdata.get('preferred_skills', []))
            minexp = jobdata.get('min_experience', 0)
            education = jobdata.get('education_requirement', 'not_specified')
            self.cursor.execute(query, (
                jobdata.get('title'),
                jobdata.get('description'),
                required,
                preferred,
                minexp,
                education
            ))
            self.conn.commit()
            jobid = self.cursor.lastrowid
            print(f"Job inserted with ID: {jobid}")
            return jobid
        except Exception as e:
            print(f"Error inserting job posting: {e}")
            raise

    def insert_job_skills(self, jobid: int, requiredskills: List[str], preferredskills: List[str]):
        try:
            query = '''
            INSERT INTO jobskills (jobid, skillname, isrequired, weight)
            VALUES (?, ?, ?, ?)
            '''
            for skill in requiredskills:
                self.cursor.execute(query, (jobid, skill, True, 1.0))
            for skill in preferredskills:
                self.cursor.execute(query, (jobid, skill, False, 0.5))
            self.conn.commit()
            print(f"Inserted skills for job ID: {jobid}")
        except Exception as e:
            print(f"Error inserting job skills: {e}")
            raise

    def get_job_posting(self, jobid: int) -> Optional[Dict]:
        query = '''SELECT * FROM jobpostings WHERE jobid = ?'''
        try:
            self.cursor.execute(query, (jobid,))
            row = self.cursor.fetchone()
            if row:
                job = dict(row)
                job['requiredskills'] = json.loads(job.get('requiredskills', '[]'))
                job['preferredskills'] = json.loads(job.get('preferredskills', '[]'))
                print(f"Fetched job posting with ID: {jobid}")
                return job
            else:
                print(f"No job posting found with ID: {jobid}")
                return None
        except Exception as e:
            print(f"Error fetching job posting: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    try:
        db = DatabaseManager()

        jobs_to_insert = [
            {
                "title": "Senior Python Developer",
                "description": "We are looking for an experienced Python developer with Django skills...",
                "required_skills": ["python", "django", "sql"],
                "preferred_skills": ["aws", "docker"],
                "min_experience": 5,
                "education_requirement": "bachelors"
            },
            {
                "title": "Junior Python Developer",
                "description": "Junior Python Developer with knowledge of Django, SQL, AWS, and machine learning.",
                "required_skills": ["python", "django", "sql"],
                "preferred_skills": ["aws", "machine learning"],
                "min_experience": 2,
                "education_requirement": "bachelors"
            },
            {
                "title": "Senior AI Engineer",
                "description": "Senior AI Engineer experienced in ML, deep learning, NLP, TensorFlow, and PyTorch, with knowledge of AWS or Azure.",
                "required_skills": ["machine learning", "deep learning", "nlp", "tensorflow", "pytorch"],
                "preferred_skills": ["aws", "azure", "big data"],
                "min_experience": 8,
                "education_requirement": "masters"
            },
            {
                "title": "Software Engineer",
                "description": "Software Engineer proficient in Java, JavaScript, Python, React, microservices, with familiarity in Docker and Kubernetes.",
                "required_skills": ["java", "javascript", "python", "react", "microservices"],
                "preferred_skills": ["docker", "kubernetes", "communication"],
                "min_experience": 3,
                "education_requirement": "bachelors"
            }
        ]

        for job in jobs_to_insert:
            job_id = db.insert_job_posting(job)
            db.insert_job_skills(job_id, job['required_skills'], job['preferred_skills'])
            fetched_job = db.get_job_posting(job_id)
            if fetched_job:
                print("Job record retrieved:")
                print(json.dumps(fetched_job, indent=4))
            else:
                print("Job record not found.")

    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        db.close()

