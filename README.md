# ATS-from-Scratch

A custom Applicant Tracking System (ATS) built from scratch using Python. This application analyzes resumes against job descriptions using Natural Language Processing (NLP) to provide matching scores and detailed analysis. The project includes both Flask and Streamlit implementations.

## Features

- PDF resume and job description parsing
- Advanced text analysis using SpaCy NLP
- Semantic similarity matching
- Skills and keyword extraction
- Multiple scoring criteria:
  - Overall match percentage
  - Resume-Job Description similarity
  - Skills match percentage
  - Work experience match
  - Education match
  - General ATS score
- Support for multiple file uploads
- Interactive web interface (both Flask and Streamlit versions)
- Analysis result export functionality

## Prerequisites

- Python 3.8+
- SpaCy with English language model
- PDF processing capabilities
- Flask/Streamlit (depending on chosen implementation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ATS-from-Scratch.git
cd ATS-from-Scratch
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Download the SpaCy model:
```bash
python -m spacy download en_core_web_md
```

## Usage

### Flask Version:
```bash
python Using_flask.py
```
Access the application at `http://localhost:5000`

### Streamlit Version:
```bash
streamlit run Using_streamlit.py
```
The application will automatically open in your default browser.

## Project Structure
```
ATS-from-Scratch/
├── README.md
├── requirements.txt
├── Using_flask.py
├── Using_streamlit.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── tests/
    └── test_ats.py
```

## How It Works

1. Upload a resume (PDF format)
2. Upload a job description (PDF format)
3. Click "Analyze Resume" or "Percentage Match"
4. View detailed analysis including:
   - Overall match percentage
   - Similarity scores
   - Skills matching
   - Work experience evaluation
   - Education matching
   - General ATS score

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
