# AI Mock Interview System

A comprehensive web-based AI-powered mock interview platform that conducts technical interviews, evaluates responses, and provides personalized feedback using Google's Gemini API.

## Features

### 🎯 Core Features
- **Resume Upload & Analysis**: Upload PDF, DOC, or DOCX resumes for AI analysis
- **Domain Selection**: Choose from 5 technical domains (Cyber Security, Python Full Stack, Data Analysis, Data Science, AI/ML Engineering)
- **AI Question Generation**: 10 personalized interview questions (5 MCQs + 5 Theory)
- **Intelligent Evaluation**: AI-powered assessment of theory answers
- **Voice Support**: Voice input and output for accessibility
- **Comprehensive Scoring**: Score calculation from 1-10 with detailed breakdown
- **AI Feedback**: Personalized strengths, weaknesses, and improvement recommendations

### 📊 Interview Structure
- **Questions 1-5**: Multiple Choice Questions (MCQs) based on resume
- **Questions 6-10**: Domain-specific theory questions
- Adaptive difficulty based on candidate's resume

### 🔊 Voice Features
- **Voice Input**: Answer theory questions using speech-to-text
- **Voice Output**: Listen to questions using text-to-speech
- Cross-browser compatibility (Chrome, Firefox, Edge)

### 📈 Results Dashboard
- Detailed score breakdown (MCQ and Theory)
- Performance level assessment
- AI-generated feedback on strengths and areas for improvement
- Recommended topics to study

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Language**: Python 3.8+
- **AI Engine**: Google Gemini API

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern responsive design
- **JavaScript**: Interactive UI with Web Speech API

### Processing
- **Resume Parsing**: PyPDF2 (PDF), python-docx (DOC/DOCX)
- **API Communication**: Flask + Python requests

## Project Structure

```
ai-mock-interview/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore file
│
├── services/
│   ├── gemini_service.py           # Gemini API integration
│   ├── resume_parser.py            # Resume text extraction
│   └── evaluator.py                # Answer evaluation logic
│
├── templates/
│   ├── index.html                  # Home page
│   ├── upload.html                 # Resume upload page
│   ├── domain.html                 # Domain selection
│   ├── interview.html              # Interview page
│   └── result.html                 # Results dashboard
│
├── static/
│   ├── css/
│   │   └── style.css               # All styling
│   └── js/
│       └── script.js               # Frontend logic
│
└── uploads/                        # Uploaded resumes storage
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key (free tier available)

### Step 1: Clone or Download the Project

```bash
cd ai-mock-interview
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

1. Create a `.env` file in the project root:

```bash
# Copy example file
cp .env.example .env
```

2. Edit `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=your_actual_api_key_here
SECRET_KEY=your-random-secret-key
FLASK_ENV=development
```

### Step 5: Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikeys
2. Click "Create API Key"
3. Copy the key
4. Paste it in `.env` file

### Step 6: Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

## Usage Guide

### Basic Workflow

1. **Open Home Page**: Visit http://localhost:5000
2. **Upload Resume**: 
   - Click "Start Mock Interview"
   - Upload your resume (PDF, DOC, or DOCX)
   - Maximum file size: 5MB
3. **Select Domain**: Choose your technical domain
4. **Take Interview**:
   - Answer MCQ questions with radio buttons
   - Answer theory questions with text/voice
   - Use "Listen" button to hear questions
   - Use "Answer Using Voice" button to input voice
5. **Review Results**:
   - See your score (1-10)
   - Review strengths and weaknesses
   - Get improvement recommendations
6. **Retake Interview**: Choose different resume or domain

### MCQ Section (Questions 1-5)

- Questions are based on technologies/projects in your resume
- Select one option (A, B, C, or D)
- Scored automatically

### Theory Section (Questions 6-10)

- Domain-specific technical questions
- Type or speak your answer
- AI evaluates:
  - Correctness
  - Technical understanding
  - Completeness
  - Relevance

### Scoring System

**MCQ Score**: 
- Correct MCQ count / 5 × 5 (out of 5)

**Theory Score**: 
- Average score of 5 theory questions (0-5 each)

**Final Score (1-10)**:
- MCQ contribution: 40%
- Theory contribution: 60%
- Minimum score: 1.0
- Maximum score: 10.0

### Voice Support

#### Text-to-Speech (Question Audio)
- Click "🔊 Listen" button
- Works on all modern browsers
- Click "⏹️ Stop" to stop playback

#### Speech-to-Text (Voice Answer)
- Available for theory questions only
- Requires Chrome, Firefox, or Edge
- Click "🎤 Answer Using Voice"
- Speak your answer clearly
- Click again to stop listening
- Text appears in answer box for review/editing

## Features Explained

### Resume Analysis
- Extracts: Skills, experience, projects, education, certifications
- Uses Gemini to understand candidate profile
- Generates MCQs tailored to resume content

### Question Generation
- **MCQs (1-5)**: Test knowledge of mentioned technologies
- **Theory (6-10)**: Domain-specific technical questions
- AI ensures variety and appropriate difficulty

### Answer Evaluation
- **MCQ**: Exact matching with correct answer
- **Theory**: Gemini evaluates based on:
  - Technical accuracy
  - Completeness
  - Key concepts covered
  - Proper explanation

### Scoring Calculation
- Fair weighting of MCQ and theory
- Minimum score ensures encouragement
- Performance levels: Excellent, Very Good, Good, Satisfactory, Needs Improvement, Beginner

## Security Features

✅ Secure file uploads with validation
✅ File size limits (5MB)
✅ Safe file extensions (PDF, DOC, DOCX)
✅ API key in environment variables (not exposed to frontend)
✅ Session-based user state isolation
✅ Input validation and sanitization
✅ No resume data stored publicly

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: 
- Ensure `.env` file exists
- Check API key is correctly pasted
- Restart Flask application

### Issue: Voice input not working
**Solution**:
- Use Chrome, Firefox, or Edge
- Check microphone permissions
- Allow website to access microphone
- Theory questions only support voice input

### Issue: Resume upload fails
**Solution**:
- Check file format (PDF, DOC, DOCX)
- Ensure file size < 5MB
- Try different PDF if extraction fails
- DOC files may need to be DOCX

### Issue: Questions not generating
**Solution**:
- Check internet connection
- Verify Gemini API key is valid
- Check Flask console for detailed errors
- Wait 30 seconds (API may take time)

### Issue: Poor question quality
**Solution**:
- Upload a more detailed resume
- Ensure resume has skills and projects
- Check selected domain matches experience

### Issue: Score seems wrong
**Solution**:
- MCQs are 40% of final score
- Theory answers are 60%
- Check if all questions answered
- Minimum score is always 1.0

## API Endpoints

### Web Routes
```
GET  /                    # Home page
GET  /upload              # Resume upload page
POST /upload              # Handle file upload
GET  /domains             # Domain selection
GET  /interview           # Interview page
GET  /result              # Result dashboard
GET  /retake              # Clear session and restart
```

### API Endpoints (JSON)
```
POST /api/start-interview       # Generate questions
GET  /api/get-questions         # Retrieve interview questions
POST /api/submit-interview      # Submit answers for evaluation
```

## Environment Variables

### `.env` Configuration

```text
# Required
GEMINI_API_KEY=your_api_key_here

# Optional
SECRET_KEY=your-secret-key-for-sessions
FLASK_ENV=development
DEBUG=True
```

## Performance Tips

1. **Faster Question Generation**:
   - Ensure internet connection is stable
   - Keep resume concise but detailed
   - 2-3 seconds typical for question generation

2. **Better Evaluation**:
   - Write clear theory answers
   - Use technical terminology appropriately
   - Provide complete explanations

3. **Voice input**:
   - Speak clearly and pause between sentences
   - Use microphone in quiet environment
   - Slow down speech pace

## Browser Compatibility

| Feature | Chrome | Firefox | Edge | Safari |
|---------|--------|---------|------|--------|
| UI | ✅ | ✅ | ✅ | ✅ |
| Voice Input | ✅ | ✅ | ✅ | ⚠️ |
| Voice Output | ✅ | ✅ | ✅ | ✅ |
| File Upload | ✅ | ✅ | ✅ | ✅ |

## File Upload Limits

- Maximum file size: 5MB
- Accepted formats: PDF, DOC, DOCX
- Recommended resume length: 1-2 pages

## Interview Domains

1. **Cyber Security**
   - Network security, encryption, threat prevention
   - Common topics: VPN, firewalls, SQL injection, CIA triad

2. **Python Full Stack**
   - Web development, frontend, backend, APIs
   - Common topics: Django, Flask, REST APIs, databases

3. **Data Analysis**
   - Data exploration, visualization, statistics
   - Common topics: EDA, pandas, correlation, preprocessing

4. **Data Science**
   - Machine learning, statistical models, algorithms
   - Common topics: supervised learning, overfitting, cross-validation

5. **AI/ML Engineering**
   - Deep learning, neural networks, advanced algorithms
   - Common topics: neural networks, gradient descent, transformers, CNN

## Tips for Best Results

### Resume Tips
- Include specific technologies and frameworks
- Mention projects with details
- List relevant certifications
- Add programming languages used

### Interview Tips
- Read questions carefully
- For MCQs: Think before answering
- For Theory: Provide detailed explanations
- Use technical terms correctly
- Explain your thought process

### Improvement
- Retake with same domain to track progress
- Focus on weak areas
- Study recommended topics
- Practice similar questions

## License

This project is created for educational purposes as a college academic project.

## Support

For issues or suggestions:
1. Check the troubleshooting section
2. Review Flask console for errors
3. Verify environment setup
4. Check internet connection

## Future Enhancements

- Database storage for interview history
- Performance analytics and progress tracking
- More interview domains
- Advanced natural language processing
- Interview scheduling
- Peer and mentor interaction
- Video upload instead of text
- Advanced analytics dashboard

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Ready for Production Use
