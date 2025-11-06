-- Table to store job postings
CREATE TABLE IF NOT EXISTS jobpostings (
    jobid INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    requiredskills TEXT,
    preferredskills TEXT,
    minexperience INTEGER,
    educationlevel TEXT,
    createdat DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table to store resumes
CREATE TABLE IF NOT EXISTS resumes (
    resumeid INTEGER PRIMARY KEY AUTOINCREMENT,
    candidatename TEXT,
    email TEXT,
    phone TEXT,
    filepath TEXT,
    rawtext TEXT,
    extractedskills TEXT,
    yearsexperience REAL,
    educationlevel TEXT,
    createdat DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table to store resume rankings for each job
CREATE TABLE IF NOT EXISTS resumerankings (
    rankingid INTEGER PRIMARY KEY AUTOINCREMENT,
    jobid INTEGER,
    resumeid INTEGER,
    score REAL,
    details TEXT,
    createdat DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (jobid) REFERENCES jobpostings(jobid),
    FOREIGN KEY (resumeid) REFERENCES resumes(resumeid)
);

-- New table for job skills (required and preferred)
CREATE TABLE IF NOT EXISTS jobskills (
    skillid INTEGER PRIMARY KEY AUTOINCREMENT,
    jobid INTEGER,
    skillname TEXT NOT NULL,
    isrequired BOOLEAN,
    weight REAL,
    FOREIGN KEY (jobid) REFERENCES jobpostings(jobid)
);

