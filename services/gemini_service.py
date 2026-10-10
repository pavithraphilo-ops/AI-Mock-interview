import os
import json
import google.generativeai as genai
from typing import Dict, List, Any

class GeminiService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Extract key information from resume"""
        prompt = f"""Analyze this resume and extract key information in JSON format:
        
Resume:
{resume_text}

Return JSON with this structure:
{{
    "candidate_name": "Name if found",
    "skills": ["skill1", "skill2", ...],
    "experience": ["exp1", "exp2", ...],
    "projects": ["project1", "project2", ...],
    "education": ["degree info"],
    "certifications": ["cert1", "cert2", ...]
}}

Return only valid JSON, no other text."""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to parse JSON response
            try:
                data = json.loads(response_text)
                return data
            except json.JSONDecodeError:
                # If JSON parsing fails, return extracted text
                return {
                    "candidate_name": "Candidate",
                    "skills": [],
                    "experience": [],
                    "projects": [],
                    "education": [],
                    "certifications": [],
                    "raw_text": resume_text[:500]
                }
        except Exception as e:
            print(f"Error analyzing resume: {str(e)}")
            return {
                "candidate_name": "Candidate",
                "skills": [],
                "experience": [],
                "projects": [],
                "education": [],
                "certifications": []
            }
    
    def generate_interview_questions(self, resume_text: str, domain: str) -> Dict[str, Any]:
        """Generate 10 interview questions (5 MCQ + 5 theory)"""
        
        prompt = f"""You are an expert interview conductor. Based on the resume and selected domain, generate exactly 10 interview questions in JSON format.

Resume:
{resume_text}

Interview Domain: {domain}

IMPORTANT REQUIREMENTS:
- Questions 1-5 MUST be Multiple Choice Questions (MCQ) based on the resume
- Questions 6-10 MUST be theory questions based on the domain
- MCQ questions should test knowledge of technologies, projects, and skills mentioned in the resume
- Theory questions should be domain-specific technical questions
- Return ONLY valid JSON, nothing else

Return this exact JSON structure:
{{
    "questions": [
        {{
            "number": 1,
            "type": "mcq",
            "question": "Question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "A",
            "explanation": "Why this is correct"
        }},
        {{
            "number": 6,
            "type": "theory",
            "question": "Theory question text"
        }}
    ]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to parse JSON
            try:
                data = json.loads(response_text)
                return data
            except json.JSONDecodeError:
                # Generate default questions if parsing fails
                return self._generate_default_questions(domain)
        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            return self._generate_default_questions(domain)
    
    def evaluate_theory_answer(self, question: str, answer: str, domain: str) -> Dict[str, Any]:
        """Evaluate a theory answer using Gemini"""
        
        prompt = f"""You are an expert evaluator for {domain} technical interviews.

Question: {question}
Candidate's Answer: {answer}

Evaluate this answer and return JSON:
{{
    "score": (0-5),
    "feedback": "Specific feedback",
    "correct_concepts": ["concept1", "concept2"],
    "missing_concepts": ["missing1", "missing2"],
    "suggestion": "How to improve"
}}

Consider:
- Correctness and accuracy
- Completeness of the answer
- Technical understanding demonstrated
- Use of proper terminology
- Relevance to the question

Return only valid JSON."""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            try:
                data = json.loads(response_text)
                # Ensure score is between 0-5
                if 'score' in data:
                    data['score'] = max(0, min(5, int(data['score'])))
                return data
            except (json.JSONDecodeError, ValueError):
                return {
                    "score": 2,
                    "feedback": "Answer recorded but auto-evaluation unavailable",
                    "correct_concepts": [],
                    "missing_concepts": [],
                    "suggestion": "Review core concepts"
                }
        except Exception as e:
            print(f"Error evaluating answer: {str(e)}")
            return {
                "score": 2,
                "feedback": "Evaluation error occurred",
                "correct_concepts": [],
                "missing_concepts": [],
                "suggestion": "Please try again"
            }
    
    def generate_final_feedback(self, resume_text: str, domain: str, scores: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final interview feedback"""
        
        prompt = f"""Generate professional interview feedback based on performance.

Resume: {resume_text[:500]}
Domain: {domain}
MCQ Score: {scores.get('mcq_score', 0)}/5
Theory Score: {scores.get('theory_score', 0)}/5
Overall Score: {scores.get('overall_score', 0)}/10

Return JSON:
{{
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["area1", "area2"],
    "interview_summary": "1-2 sentence summary",
    "recommendation": "Recommendation level",
    "topics_to_study": ["topic1", "topic2"]
}}

Recommendations: Excellent preparation, Good preparation, Needs more practice, Beginner level, Strong technical candidate

Return only valid JSON."""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return {
                    "strengths": ["Participated in interview"],
                    "weaknesses": ["Review technical concepts"],
                    "interview_summary": "Interview completed.",
                    "recommendation": "Good preparation",
                    "topics_to_study": ["Core concepts", "Domain fundamentals"]
                }
        except Exception as e:
            print(f"Error generating feedback: {str(e)}")
            return {
                "strengths": [],
                "weaknesses": [],
                "interview_summary": "Interview completed.",
                "recommendation": "Review and practice",
                "topics_to_study": []
            }
    
    def _generate_default_questions(self, domain: str) -> Dict[str, Any]:
        """Generate default questions if API fails"""
        
        default_questions = {
            "Cyber Security": [
                {"number": 1, "type": "mcq", "question": "What is the primary goal of cybersecurity?",
                 "options": ["Prevent all attacks", "Protect data and systems", "Encrypt everything", "Monitor networks"],
                 "correct_answer": "B", "explanation": "Protect data and systems from unauthorized access."},
                {"number": 2, "type": "mcq", "question": "Which of these is a strong password practice?",
                 "options": ["Use your birthday", "Use 8+ characters with mixed case", "Reuse passwords", "Write password on sticky note"],
                 "correct_answer": "B", "explanation": "Strong passwords need length and complexity."},
                {"number": 3, "type": "mcq", "question": "What does VPN stand for?",
                 "options": ["Virtual Private Network", "Very Public Network", "Virtual Proxy Node", "Verified Private Network"],
                 "correct_answer": "A", "explanation": "VPN encrypts connections over public networks."},
                {"number": 4, "type": "mcq", "question": "What is SQL injection?",
                 "options": ["Injecting data into databases", "Inserting malicious SQL code", "Adding user data", "Updating records"],
                 "correct_answer": "B", "explanation": "SQL injection exploits database vulnerabilities."},
                {"number": 5, "type": "mcq", "question": "Which protocol is secure for web browsing?",
                 "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
                 "correct_answer": "C", "explanation": "HTTPS encrypts web traffic."},
                {"number": 6, "type": "theory", "question": "Explain the CIA Triad and its importance in cybersecurity."},
                {"number": 7, "type": "theory", "question": "What is the difference between symmetric and asymmetric encryption?"},
                {"number": 8, "type": "theory", "question": "Describe common types of cyberattacks and how to prevent them."},
                {"number": 9, "type": "theory", "question": "What is a firewall and how does it protect networks?"},
                {"number": 10, "type": "theory", "question": "Explain the importance of regular security audits and penetration testing."}
            ],
            "Python Full Stack": [
                {"number": 1, "type": "mcq", "question": "Which framework is most commonly used for Python web development?",
                 "options": ["Django", "Flask", "FastAPI", "Pyramid"],
                 "correct_answer": "A", "explanation": "Django is the most comprehensive Python web framework."},
                {"number": 2, "type": "mcq", "question": "What is the purpose of virtual environments in Python?",
                 "options": ["Run Python in cloud", "Isolate project dependencies", "Speed up execution", "Enable multithreading"],
                 "correct_answer": "B", "explanation": "Virtual environments prevent dependency conflicts."},
                {"number": 3, "type": "mcq", "question": "Which database is commonly used with Flask?",
                 "options": ["MongoDB", "PostgreSQL", "SQLite", "All of the above"],
                 "correct_answer": "D", "explanation": "Flask works with various databases."},
                {"number": 4, "type": "mcq", "question": "What does REST API stand for?",
                 "options": ["Representational State Transfer API", "Remote Execution Service Tool", "Reactive Stateful Endpoint", "Reliable Service Transport"],
                 "correct_answer": "A", "explanation": "REST is an architectural pattern for APIs."},
                {"number": 5, "type": "mcq", "question": "What is the difference between request and response in HTTP?",
                 "options": ["They're the same", "Request is client to server, response is server to client", "Response is first", "No difference"],
                 "correct_answer": "B", "explanation": "HTTP follows a request-response model."},
                {"number": 6, "type": "theory", "question": "Explain the Model-View-Controller (MVC) architecture in web applications."},
                {"number": 7, "type": "theory", "question": "What are decorators in Python and how are they used in Flask?"},
                {"number": 8, "type": "theory", "question": "Describe the difference between SQL and NoSQL databases."},
                {"number": 9, "type": "theory", "question": "Explain how authentication and authorization work in web applications."},
                {"number": 10, "type": "theory", "question": "What is CORS and why is it important for web development?"}
            ],
            "Data Analysis": [
                {"number": 1, "type": "mcq", "question": "Which Python library is primarily used for data analysis?",
                 "options": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn"],
                 "correct_answer": "B", "explanation": "Pandas is the main data analysis library."},
                {"number": 2, "type": "mcq", "question": "What is data preprocessing?",
                 "options": ["Visualizing data", "Cleaning and preparing data", "Storing data", "Deleting data"],
                 "correct_answer": "B", "explanation": "Preprocessing prepares data for analysis."},
                {"number": 3, "type": "mcq", "question": "What does EDA stand for?",
                 "options": ["Exploratory Data Analysis", "External Data Access", "Error Detection Algorithm", "Extended Data Architecture"],
                 "correct_answer": "A", "explanation": "EDA is exploring data to understand patterns."},
                {"number": 4, "type": "mcq", "question": "What is a correlation coefficient?",
                 "options": ["Data comparison measure", "Relationship strength between variables", "Data sorting method", "Classification metric"],
                 "correct_answer": "B", "explanation": "Correlation measures relationship strength."},
                {"number": 5, "type": "mcq", "question": "Which visualization library is best for data analysis?",
                 "options": ["Matplotlib", "Seaborn", "Plotly", "Any can be used"],
                 "correct_answer": "D", "explanation": "Multiple libraries are suitable for visualization."},
                {"number": 6, "type": "theory", "question": "Explain the steps involved in the data analysis process."},
                {"number": 7, "type": "theory", "question": "What are outliers and how do you handle them in data analysis?"},
                {"number": 8, "type": "theory", "question": "Describe different types of data cleaning techniques."},
                {"number": 9, "type": "theory", "question": "Explain the importance of data visualization in analysis."},
                {"number": 10, "type": "theory", "question": "What is feature engineering and why is it important?"}
            ],
            "Data Science": [
                {"number": 1, "type": "mcq", "question": "What is the main purpose of machine learning?",
                 "options": ["Store data", "Learn patterns from data", "Encrypt data", "Delete data"],
                 "correct_answer": "B", "explanation": "ML learns patterns to make predictions."},
                {"number": 2, "type": "mcq", "question": "What is overfitting in machine learning?",
                 "options": ["Model learns noise", "Model generalizes well", "Too many features", "Insufficient data"],
                 "correct_answer": "A", "explanation": "Overfitting occurs when a model memorizes training data."},
                {"number": 3, "type": "mcq", "question": "What does cross-validation help prevent?",
                 "options": ["Underfitting", "Overfitting", "Both", "Neither"],
                 "correct_answer": "C", "explanation": "Cross-validation helps detect both issues."},
                {"number": 4, "type": "mcq", "question": "What is the difference between supervised and unsupervised learning?",
                 "options": ["Supervised has labels, unsupervised doesn't", "Unsupervised is faster", "Same thing", "Unrelated concepts"],
                 "correct_answer": "A", "explanation": "Supervised learning uses labeled data."},
                {"number": 5, "type": "mcq", "question": "Which metric is used for classification problems?",
                 "options": ["Mean Squared Error", "Accuracy", "R-squared", "All are used"],
                 "correct_answer": "D", "explanation": "Different metrics suit different situations."},
                {"number": 6, "type": "theory", "question": "Explain the difference between classification and regression."},
                {"number": 7, "type": "theory", "question": "What is a confusion matrix and how is it interpreted?"},
                {"number": 8, "type": "theory", "question": "Describe the train-test split and its importance."},
                {"number": 9, "type": "theory", "question": "Explain gradient descent and its role in machine learning."},
                {"number": 10, "type": "theory", "question": "What are ensemble methods and why are they effective?"}
            ],
            "AI/ML Engineering": [
                {"number": 1, "type": "mcq", "question": "What is a neural network?",
                 "options": ["Network of computers", "Computer network", "Biologically inspired computation model", "Internet connection"],
                 "correct_answer": "C", "explanation": "Neural networks are inspired by biological neurons."},
                {"number": 2, "type": "mcq", "question": "What is a Deep Learning model?",
                 "options": ["Neural network with many layers", "Fast model", "Simple model", "Database system"],
                 "correct_answer": "A", "explanation": "Deep learning uses multiple neural network layers."},
                {"number": 3, "type": "mcq", "question": "What does backpropagation do?",
                 "options": ["Moves data forward", "Computes gradients for weight updates", "Stores memory", "Deletes errors"],
                 "correct_answer": "B", "explanation": "Backpropagation calculates gradients for training."},
                {"number": 4, "type": "mcq", "question": "What is a convolutional neural network used for?",
                 "options": ["Text processing", "Image processing", "Audio", "Time series"],
                 "correct_answer": "B", "explanation": "CNNs are effective for image analysis."},
                {"number": 5, "type": "mcq", "question": "What is transfer learning?",
                 "options": ["Moving models to cloud", "Using pre-trained models", "Changing model architecture", "Data migration"],
                 "correct_answer": "B", "explanation": "Transfer learning reuses pre-trained features."},
                {"number": 6, "type": "theory", "question": "Explain how gradient descent works in neural networks."},
                {"number": 7, "type": "theory", "question": "What are activation functions and why are they important?"},
                {"number": 8, "type": "theory", "question": "Describe the vanishing gradient problem and solutions."},
                {"number": 9, "type": "theory", "question": "Explain the architecture of a recurrent neural network."},
                {"number": 10, "type": "theory", "question": "What is the attention mechanism in transformer models?"}
            ]
        }
        
        questions = default_questions.get(domain, default_questions["Python Full Stack"])
        return {"questions": questions}
