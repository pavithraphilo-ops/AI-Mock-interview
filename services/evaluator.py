from typing import Dict, List, Any
import math

class Evaluator:
    """
    Handles interview answer evaluation and score calculation
    """
    
    @staticmethod
    def evaluate_mcq_answers(mcq_answers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate multiple choice answers
        Expected mcq_answers format: [{"question_num": 1, "answer": "A"}, ...]
        """
        correct_count = 0
        total_mcq = len(mcq_answers)
        
        for answer_data in mcq_answers:
            if answer_data.get('answer') == answer_data.get('correct_answer'):
                correct_count += 1
        
        # Score out of 5
        mcq_score = (correct_count / total_mcq * 5) if total_mcq > 0 else 0
        
        return {
            "correct_count": correct_count,
            "total_count": total_mcq,
            "mcq_score": round(mcq_score, 2),
            "percentage": round((correct_count / total_mcq * 100) if total_mcq > 0 else 0, 2)
        }
    
    @staticmethod
    def calculate_theory_score(theory_evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate overall theory score from individual theory evaluations
        Expected format: [{"score": 4, "max_score": 5}, ...]
        """
        if not theory_evaluations:
            return {
                "theory_score": 0,
                "theory_average": 0,
                "total_possible": 0,
                "percentage": 0
            }
        
        total_score = sum(eval.get('score', 0) for eval in theory_evaluations)
        total_possible = sum(eval.get('max_score', 5) for eval in theory_evaluations)
        
        average_score = total_score / len(theory_evaluations) if theory_evaluations else 0
        theory_score = (total_score / total_possible * 5) if total_possible > 0 else 0
        percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
        
        return {
            "theory_score": round(theory_score, 2),
            "theory_average": round(average_score, 2),
            "total_score": total_score,
            "total_possible": total_possible,
            "percentage": round(percentage, 2)
        }
    
    @staticmethod
    def calculate_final_score(mcq_score: float, theory_score: float) -> float:
        """
        Calculate final interview score (1-10)
        MCQ contributes 40%, Theory contributes 60%
        """
        # Weighted calculation
        weighted_score = (mcq_score / 5 * 40) + (theory_score / 5 * 60)
        weighted_percentage = weighted_score  # This is already a percentage out of 100
        
        # Convert percentage to 1-10 scale
        final_score = (weighted_percentage / 100) * 10
        
        # Ensure minimum score is 1
        final_score = max(1, final_score)
        
        return round(final_score, 1)
    
    @staticmethod
    def get_performance_level(score: float) -> str:
        """Get performance level based on score"""
        if score >= 9:
            return "Excellent"
        elif score >= 8:
            return "Very Good"
        elif score >= 7:
            return "Good"
        elif score >= 6:
            return "Satisfactory"
        elif score >= 5:
            return "Needs Improvement"
        else:
            return "Beginner Level"
    
    @staticmethod
    def calculate_all_scores(mcq_answers: List[Dict[str, Any]], 
                            theory_evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate all scores comprehensively
        """
        # MCQ evaluation
        mcq_results = Evaluator.evaluate_mcq_answers(mcq_answers)
        
        # Theory evaluation  
        theory_results = Evaluator.calculate_theory_score(theory_evaluations)
        
        # Final score
        final_score = Evaluator.calculate_final_score(
            mcq_results['mcq_score'],
            theory_results['theory_score']
        )
        
        # Performance level
        performance_level = Evaluator.get_performance_level(final_score)
        
        return {
            "mcq": mcq_results,
            "theory": theory_results,
            "final_score": final_score,
            "performance_level": performance_level,
            "mcq_percentage": mcq_results['percentage'],
            "theory_percentage": theory_results['percentage']
        }
    
    @staticmethod
    def prepare_score_summary(scores: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare score summary for display"""
        return {
            "correct_mcqs": scores['mcq']['correct_count'],
            "total_mcqs": scores['mcq']['total_count'],
            "mcq_score": scores['mcq']['mcq_score'],
            "theory_score": scores['theory']['theory_score'],
            "overall_score": scores['final_score'],
            "performance": scores['performance_level'],
            "mcq_percentage": scores['mcq_percentage'],
            "theory_percentage": scores['theory_percentage']
        }
