// Global variables
let questions = [];
let currentQuestionIndex = 0;
let answers = {};
let voiceEnabled = false;
let isListeningToVoice = false;
let speechSynthesisUtterance = null;
let speechRecognition = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializePage();
    setupVoiceRecognition();
});

function initializePage() {
    // Check which page we're on
    const page = getCurrentPage();
    
    if (page === 'interview') {
        loadInterviewQuestions();
    }
}

function getCurrentPage() {
    const path = window.location.pathname;
    if (path.includes('/interview')) return 'interview';
    if (path.includes('/result')) return 'result';
    if (path.includes('/domains')) return 'domains';
    if (path.includes('/upload')) return 'upload';
    return 'home';
}

// ==================== INTERVIEW PAGE FUNCTIONS ====================

async function loadInterviewQuestions() {
    try {
        const response = await fetch('/api/get-questions');
        const data = await response.json();
        
        if (data.success) {
            questions = data.questions;
            answers = {};
            currentQuestionIndex = 0;
            
            // Initialize answers object
            questions.forEach((q) => {
                answers[q.number] = {
                    question_number: q.number,
                    type: q.type,
                    answer: null,
                    correct_answer: q.correct_answer || null
                };
            });
            
            displayQuestion();
        }
    } catch (error) {
        console.error('Error loading questions:', error);
        showStatus('Error loading interview questions', 'error');
    }
}

function displayQuestion() {
    const question = questions[currentQuestionIndex];
    if (!question) return;
    
    // Update progress
    updateProgress();
    
    // Update question title
    const questionTitle = document.getElementById('questionTitle');
    questionTitle.textContent = `Question ${question.number}: ${question.question}`;
    
    // Clear previous answer elements
    const mcqContainer = document.getElementById('mcqContainer');
    const theoryContainer = document.getElementById('theoryContainer');
    const answerStatus = document.getElementById('answerStatus');
    answerStatus.classList.add('hidden');
    
    if (question.type === 'mcq') {
        // Display MCQ options
        mcqContainer.classList.remove('hidden');
        theoryContainer.classList.add('hidden');
        displayMCQOptions(question);
    } else {
        // Display theory input
        mcqContainer.classList.add('hidden');
        theoryContainer.classList.remove('hidden');
        displayTheoryInput(question);
    }
    
    // Update button states
    updateNavigationButtons();
    
    // Setup voice button
    setupVoiceButton(question);
}

function displayMCQOptions(question) {
    const mcqOptions = document.getElementById('mcqOptions');
    mcqOptions.innerHTML = '';
    
    const options = ['A', 'B', 'C', 'D'];
    options.forEach((opt, index) => {
        const optionText = question.options[index];
        const optionDiv = document.createElement('div');
        optionDiv.className = 'mcq-option';
        
        const savedAnswer = answers[question.number].answer;
        if (savedAnswer === opt) {
            optionDiv.classList.add('selected');
        }
        
        optionDiv.innerHTML = `
            <input type="radio" id="option_${opt}" name="mcq_option" value="${opt}" 
                   ${savedAnswer === opt ? 'checked' : ''}>
            <label for="option_${opt}">${opt}. ${optionText}</label>
        `;
        
        optionDiv.addEventListener('click', () => selectMCQOption(question.number, opt));
        optionDiv.querySelector('input').addEventListener('change', () => selectMCQOption(question.number, opt));
        
        mcqOptions.appendChild(optionDiv);
    });
}

function selectMCQOption(questionNumber, option) {
    answers[questionNumber].answer = option;
    
    // Update UI
    const mcqOptions = document.querySelectorAll('.mcq-option');
    mcqOptions.forEach(opt => opt.classList.remove('selected'));
    
    const selectedOption = document.querySelector(`input[value="${option}"]`);
    if (selectedOption) {
        selectedOption.parentElement.classList.add('selected');
    }
}

function displayTheoryInput(question) {
    const theoryAnswer = document.getElementById('theoryAnswer');
    const charCount = document.getElementById('charCount');
    
    // Restore saved answer
    const savedAnswer = answers[question.number].answer;
    theoryAnswer.value = savedAnswer || '';
    charCount.textContent = theoryAnswer.value.length;
    
    // Character count listener
    theoryAnswer.addEventListener('input', (e) => {
        charCount.textContent = e.target.value.length;
        answers[question.number].answer = e.target.value;
    });
}

function updateProgress() {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const navProgress = document.getElementById('navProgress');
    
    const percentage = ((currentQuestionIndex + 1) / questions.length) * 100;
    progressFill.style.width = percentage + '%';
    
    const text = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
    progressText.textContent = text;
    navProgress.textContent = text;
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitContainer = document.getElementById('submitContainer');
    
    // Previous button
    prevBtn.disabled = currentQuestionIndex === 0;
    
    // Next button and submit container
    if (currentQuestionIndex === questions.length - 1) {
        nextBtn.style.display = 'none';
        submitContainer.classList.remove('hidden');
    } else {
        nextBtn.style.display = 'inline-flex';
        submitContainer.classList.add('hidden');
    }
}

// Navigation buttons
document.getElementById('prevBtn')?.addEventListener('click', () => {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
});

document.getElementById('nextBtn')?.addEventListener('click', () => {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
});

document.getElementById('endInterviewBtn')?.addEventListener('click', () => {
    const dialog = document.getElementById('confirmDialog');
    dialog.classList.remove('hidden');
});

document.getElementById('confirmCancel')?.addEventListener('click', () => {
    const dialog = document.getElementById('confirmDialog');
    dialog.classList.add('hidden');
});

document.getElementById('confirmEnd')?.addEventListener('click', () => {
    window.location.href = '/';
});

document.getElementById('submitBtn')?.addEventListener('click', submitInterview);

// ==================== FORM SUBMISSION ====================

async function submitInterview() {
    // Validate all questions answered
    let allAnswered = true;
    questions.forEach((q) => {
        if (!answers[q.number].answer) {
            allAnswered = false;
        }
    });
    
    if (!allAnswered) {
        showStatus('Please answer all questions before submitting', 'error');
        return;
    }
    
    // Show loading
    const submitBtn = document.getElementById('submitBtn');
    const loadingContainer = document.getElementById('loadingContainer');
    const loadingText = document.getElementById('loadingText');
    
    submitBtn.disabled = true;
    loadingContainer.classList.remove('hidden');
    loadingText.textContent = 'Evaluating your answers...';
    
    try {
        const answersArray = Object.values(answers).map(a => ({
            question_number: a.question_number,
            type: a.type,
            answer: a.answer,
            correct_answer: a.correct_answer
        }));
        
        const response = await fetch('/api/submit-interview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ answers: answersArray })
        });
        
        const data = await response.json();
        
        if (data.success) {
            loadingText.textContent = 'Preparing your results...';
            setTimeout(() => {
                window.location.href = '/result';
            }, 1500);
        } else {
            showStatus(data.message || 'Submission failed', 'error');
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error submitting interview:', error);
        showStatus('Network error during submission', 'error');
        submitBtn.disabled = false;
    } finally {
        loadingContainer.classList.add('hidden');
    }
}

// ==================== VOICE RECOGNITION SETUP ====================

function setupVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        voiceEnabled = false;
        console.log('Speech recognition not supported in this browser');
        return;
    }
    
    try {
        speechRecognition = new SpeechRecognition();
        speechRecognition.continuous = false;
        speechRecognition.interimResults = true;
        speechRecognition.lang = 'en-US';
        
        let interimTranscript = '';
        
        speechRecognition.onstart = () => {
            isListeningToVoice = true;
            updateVoiceStatus('Listening... Click stop to finish', 'listening');
        };
        
        speechRecognition.onresult = (event) => {
            interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    const theoryAnswer = document.getElementById('theoryAnswer');
                    if (theoryAnswer) {
                        const currentText = theoryAnswer.value;
                        theoryAnswer.value = (currentText ? currentText + ' ' : '') + transcript;
                        
                        // Update character count
                        const charCount = document.getElementById('charCount');
                        charCount.textContent = theoryAnswer.value.length;
                        
                        // Save answer
                        const question = questions[currentQuestionIndex];
                        answers[question.number].answer = theoryAnswer.value;
                    }
                } else {
                    interimTranscript += transcript;
                }
            }
        };
        
        speechRecognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            updateVoiceStatus(`Error: ${event.error}`, '');
        };
        
        speechRecognition.onend = () => {
            isListeningToVoice = false;
            updateVoiceStatus('Ready for voice input', '');
        };
        
        voiceEnabled = true;
    } catch (error) {
        console.error('Error initializing voice recognition:', error);
        voiceEnabled = false;
    }
}

function setupVoiceButton(question) {
    const speakBtn = document.getElementById('speakBtn');
    const stopSpeakBtn = document.getElementById('stopSpeakBtn');
    const voiceInputBtn = document.getElementById('voiceInputBtn');
    
    if (!speakBtn || !stopSpeakBtn) return;
    
    // Clear previous listeners
    speakBtn.onclick = null;
    stopSpeakBtn.onclick = null;
    if (voiceInputBtn) voiceInputBtn.onclick = null;
    
    // Text-to-speech for question
    speakBtn.addEventListener('click', () => speakQuestion(question.question));
    stopSpeakBtn.addEventListener('click', stopSpeaking);
    
    // Voice input for theory questions
    if (question.type === 'theory' && voiceInputBtn) {
        if (!voiceEnabled) {
            voiceInputBtn.textContent = '🎤 Voice not supported in this browser';
            voiceInputBtn.disabled = true;
        } else {
            voiceInputBtn.disabled = false;
            voiceInputBtn.addEventListener('click', startVoiceInput);
        }
    }
}

function speakQuestion(text) {
    // Cancel previous speech if any
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;
    
    const speakBtn = document.getElementById('speakBtn');
    const stopSpeakBtn = document.getElementById('stopSpeakBtn');
    
    speakBtn.style.display = 'none';
    stopSpeakBtn.style.display = 'inline-flex';
    
    utterance.onend = () => {
        speakBtn.style.display = 'inline-flex';
        stopSpeakBtn.style.display = 'none';
    };
    
    window.speechSynthesis.speak(utterance);
}

function stopSpeaking() {
    window.speechSynthesis.cancel();
    const speakBtn = document.getElementById('speakBtn');
    const stopSpeakBtn = document.getElementById('stopSpeakBtn');
    
    speakBtn.style.display = 'inline-flex';
    stopSpeakBtn.style.display = 'none';
}

function startVoiceInput() {
    if (!voiceEnabled || !speechRecognition) {
        showStatus('Voice input not available in this browser', 'error');
        return;
    }

    const voiceInputBtn = document.getElementById('voiceInputBtn');

    try {
        if (isListeningToVoice) {
            speechRecognition.stop();
            isListeningToVoice = false;
            if (voiceInputBtn) {
                voiceInputBtn.classList.remove('listening');
                voiceInputBtn.textContent = '🎤 Answer Using Voice';
            }
            updateVoiceStatus('Voice input stopped', '');
        } else {
            speechRecognition.start();
            isListeningToVoice = true;
            if (voiceInputBtn) {
                voiceInputBtn.classList.add('listening');
                voiceInputBtn.textContent = '🛑 Stop Voice';
            }
            updateVoiceStatus('Listening... click again to stop', 'listening');
        }
    } catch (error) {
        console.error('Error starting voice input:', error);
        showStatus('Error starting voice input', 'error');
    }
}

function updateVoiceStatus(message, className) {
    const voiceStatus = document.getElementById('voiceStatus');
    if (voiceStatus) {
        voiceStatus.textContent = message;
        voiceStatus.className = 'voice-status';
        if (className) voiceStatus.classList.add(className);
    }
}

// ==================== UTILITY FUNCTIONS ====================

function showStatus(message, type = 'info') {
    const statusMessage = document.getElementById('answerStatus') || 
                         document.getElementById('statusMessage');
    
    if (!statusMessage) return;
    
    statusMessage.className = `status-message ${type}`;
    statusMessage.textContent = message;
    statusMessage.classList.remove('hidden');
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        statusMessage.classList.add('hidden');
    }, 5000);
}

// ==================== UTILITY FUNCTIONS ====================

// Store selected domain in localStorage for reference
if (document.querySelector('.domain-card')) {
    document.querySelectorAll('.domain-card').forEach(card => {
        card.addEventListener('click', function() {
            localStorage.setItem('selectedDomain', this.getAttribute('data-domain'));
        });
    });
}

console.log('Interview script loaded successfully');
