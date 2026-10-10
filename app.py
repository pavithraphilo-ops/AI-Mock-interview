from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import json
from services.gemini_service import GeminiService
from services.resume_parser import ResumeParser
from services.evaluator import Evaluator

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Interview domains
DOMAINS = {
    "Cyber Security": "Cyber Security and Network Protection",
    "Python Full Stack": "Python Web Development with Frontend and Backend",
    "Data Analysis": "Data Analysis and Visualization",
    "Data Science": "Machine Learning and Data Science",
    "AI/ML Engineering": "Artificial Intelligence and Machine Learning Engineering"
}

# Initialize Gemini service with error handling
try:
    gemini_service = GeminiService()
except Exception as e:
    print(f"Warning: Could not initialize Gemini service: {str(e)}")
    gemini_service = None


@app.route('/')
def index():
    """Home page"""
    session.clear()
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    """Handle resume upload"""
    if request.method == 'POST':
        if 'resume' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not ResumeParser.allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload PDF, DOC, or DOCX'}), 400
        
        try:
            # Save file
            success, result = ResumeParser.save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
            if not success:
                return jsonify({'success': False, 'message': result}), 400
            
            file_path = result
            
            # Extract text
            success_msg, resume_text = ResumeParser.parse_resume(file_path)
            if not resume_text:
                return jsonify({'success': False, 'message': success_msg}), 400
            
            # Store in session (limited to first 3000 chars to avoid session size issues)
            session['resume_text'] = resume_text[:3000]
            session['resume_file'] = file_path
            
            # Analyze resume with Gemini if available
            if gemini_service:
                try:
                    resume_analysis = gemini_service.analyze_resume(resume_text)
                    session['resume_analysis'] = resume_analysis
                except Exception as e:
                    print(f"Error analyzing resume: {str(e)}")
            
            return jsonify({
                'success': True,
                'message': 'Resume uploaded successfully ✓',
                'resume_name': secure_filename(file.filename)
            }), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error processing resume: {str(e)}'}), 500
    
    return render_template('upload.html')


@app.route('/domains')
def select_domain():
    """Show domain selection page"""
    if 'resume_text' not in session:
        return redirect(url_for('upload_resume'))
    
    return render_template('domain.html', domains=DOMAINS)


@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    """Start interview and generate questions"""
    if 'resume_text' not in session:
        return jsonify({'success': False, 'message': 'No resume uploaded'}), 400
    
    data = request.get_json()
    domain = data.get('domain', '')
    
    if domain not in DOMAINS:
        return jsonify({'success': False, 'message': 'Invalid domain selected'}), 400
    
    if not gemini_service:
        return jsonify({'success': False, 'message': 'AI service not available. Check GEMINI_API_KEY'}), 500
    
    try:
        resume_text = session.get('resume_text', '')
        
        # Generate questions with Gemini
        questions_data = gemini_service.generate_interview_questions(resume_text, domain)
        
        if not questions_data or 'questions' not in questions_data:
            return jsonify({'success': False, 'message': 'Failed to generate questions'}), 500
        
        questions = questions_data['questions']
        
        # Validate we have exactly 10 questions
        if len(questions) < 10:
            return jsonify({'success': False, 'message': 'Insufficient questions generated'}), 500
        
        # Ensure exactly 10 questions
        questions = questions[:10]
        
        # Store in session
        session['domain'] = domain
        session['questions'] = questions
        session['answers'] = {}
        
        return jsonify({
            'success': True,
            'message': 'Interview started',
            'questions_count': len(questions)
        }), 200
    
    except Exception as e:
        print(f"Error starting interview: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/interview')
def interview():
    """Interview page"""
    if 'questions' not in session or 'domain' not in session:
        return redirect(url_for('select_domain'))
    
    questions = session.get('questions', [])
    return render_template('interview.html', questions=questions)


@app.route('/api/get-questions', methods=['GET'])
def get_questions():
    """Get interview questions for frontend"""
    if 'questions' not in session:
        return jsonify({'success': False, 'message': 'No questions available'}), 400
    
    questions = session.get('questions', [])
    return jsonify({
        'success': True,
        'questions': questions,
        'domain': session.get('domain', '')
    }), 200


@app.route('/api/submit-interview', methods=['POST'])
def submit_interview():
    """
    Submit interview answers for evaluation
    Expected format: {"answers": [{"question_number": 1, "type": "mcq", "answer": "A", ...}, ...]}
    """
    if 'questions' not in session:
        return jsonify({'success': False, 'message': 'No active interview'}), 400
    
    data = request.get_json()
    answers = data.get('answers', [])
    
    if not answers or len(answers) < 10:
        return jsonify({'success': False, 'message': 'All 10 questions must be answered'}), 400
    
    if not gemini_service:
        return jsonify({'success': False, 'message': 'AI service not available'}), 500
    
    try:
        questions = session.get('questions', [])
        domain = session.get('domain', '')
        resume_text = session.get('resume_text', '')
        
        # Evaluate MCQ answers (Questions 1-5)
        mcq_answers = []
        for answer in answers:
            if answer['question_number'] <= 5:
                # Find correct answer from questions
                question = next((q for q in questions if q['number'] == answer['question_number']), None)
                if question:
                    correct_answer = question.get('correct_answer', '')
                    mcq_answers.append({
                        'question_num': answer['question_number'],
                        'answer': answer.get('answer', ''),
                        'correct_answer': correct_answer
                    })
        
        mcq_results = Evaluator.evaluate_mcq_answers(mcq_answers)
        
        # Evaluate theory answers (Questions 6-10) with Gemini
        theory_evaluations = []
        for answer in answers:
            if answer['question_number'] > 5:
                question = next((q for q in questions if q['number'] == answer['question_number']), None)
                if question:
                    question_text = question.get('question', '')
                    answer_text = answer.get('answer', '')
                    
                    # Get Gemini evaluation
                    evaluation = gemini_service.evaluate_theory_answer(
                        question_text,
                        answer_text,
                        domain
                    )
                    theory_evaluations.append({
                        'question_number': answer['question_number'],
                        'score': evaluation.get('score', 2),
                        'max_score': 5,
                        'feedback': evaluation.get('feedback', ''),
                        'correct_concepts': evaluation.get('correct_concepts', []),
                        'missing_concepts': evaluation.get('missing_concepts', [])
                    })
        
        # Calculate all scores
        all_scores = Evaluator.calculate_all_scores(mcq_answers, theory_evaluations)
        
        # Generate final feedback
        feedback_data = gemini_service.generate_final_feedback(
            resume_text,
            domain,
            all_scores
        )
        
        # Store results in session
        session['scores'] = all_scores
        session['theory_evaluations'] = theory_evaluations
        session['feedback'] = feedback_data
        
        return jsonify({
            'success': True,
            'message': 'Interview evaluated successfully',
            'final_score': all_scores['final_score']
        }), 200
    
    except Exception as e:
        print(f"Error submitting interview: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/result')
def result():
    """Display interview result"""
    if 'scores' not in session:
        return redirect(url_for('start_interview'))
    
    scores = session.get('scores', {})
    feedback = session.get('feedback', {})
    domain = session.get('domain', '')
    resume_analysis = session.get('resume_analysis', {})
    
    candidate_name = resume_analysis.get('candidate_name', 'Candidate')
    
    return render_template('result.html',
                         scores=scores,
                         feedback=feedback,
                         domain=domain,
                         candidate_name=candidate_name)


@app.route('/retake')
def retake():
    """Clear interview and restart"""
    session.clear()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    print(f"Server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
