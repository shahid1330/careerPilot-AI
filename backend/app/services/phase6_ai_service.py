"""
Phase 6A & 6B: AI Service for Mock Tests and Career Intelligence
Uses Anthropic Claude for intelligent content generation
"""

import json
import os
from typing import List, Dict, Any


class Phase6AIService:
    """AI service for Phase 6A and 6B features"""
    
    # Role to programming language mapping
    ROLE_LANGUAGE_MAP = {
        'python developer': 'python',
        'backend developer': 'python',
        'data scientist': 'python',
        'machine learning engineer': 'python',
        'java developer': 'java',
        'android developer': 'java',
        'javascript developer': 'javascript',
        'frontend developer': 'javascript',
        'react developer': 'javascript',
        'node.js developer': 'javascript',
        'full stack developer': 'javascript',
        'web developer': 'javascript',
        'c++ developer': 'cpp',
        'c# developer': 'csharp',
        '.net developer': 'csharp',
        'go developer': 'go',
        'rust developer': 'rust',
        'default': 'python'
    }
    
    def __init__(self):
        # For now, using Groq. In production, switch to Anthropic Claude
        self.api_key = os.getenv("GROQ_API_KEY") or os.getenv("LLM_API_KEY")
        self.model = os.getenv("LLM_MODEL_NAME", "llama-3.1-8b-instant")
        # self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def get_language_for_role(self, role_name: str) -> str:
        """Get programming language based on role"""
        role_lower = role_name.lower()
        for key, lang in self.ROLE_LANGUAGE_MAP.items():
            if key in role_lower:
                return lang
        return self.ROLE_LANGUAGE_MAP['default']
        
    def generate_mock_test_questions(
        self, 
        completed_topics: List[str],
        role_name: str,
        mcq_count: int,
        coding_count: int,
        previous_questions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized mock test based on completed topics
        
        Args:
            completed_topics: List of topics user has completed
            role_name: User's target role
            mcq_count: Number of MCQs to generate
            coding_count: Number of coding questions to generate
            
        Returns:
            Dict with 'mcq_questions' and 'coding_questions'
        """
        
        # Get programming language for this role
        coding_language = self.get_language_for_role(role_name)
        
        # Build uniqueness constraint
        uniqueness_note = ""
        if previous_questions and len(previous_questions) > 0:
            prev_q_text = '\n'.join([f"- {q}" for q in previous_questions[:30]])
            uniqueness_note = f"""

**❌ ABSOLUTELY DO NOT REPEAT THESE QUESTIONS (from previous tests):**
{prev_q_text}

**✅ YOU MUST:**
- Generate 100% BRAND NEW questions
- Use completely DIFFERENT scenarios, examples, and contexts
- Ask about the SAME topics but with UNIQUE questions
- If you repeat ANY question above, the test will FAIL
"""
        
        prompt = f"""You are an expert technical assessment creator for HackerRank/LeetCode. Generate a professional mock test for a {role_name} candidate.

**🔒 STRICT REQUIREMENTS (MUST FOLLOW):**
1. ✅ Generate questions ONLY from these COMPLETED topics: {', '.join(completed_topics)}
2. ❌ DO NOT include topics the user hasn't studied yet
3. ⚖️ Mix difficulty levels: 40% easy, 40% medium, 20% hard
4. 💻 ALL CODING QUESTIONS MUST BE IN {coding_language.upper()} ONLY
5. 🎯 Each question must be UNIQUE and test practical understanding{uniqueness_note}

**MCQ QUESTIONS:**
- Test practical knowledge of completed topics
- 4 options (A, B, C, D) per question
- Real-world scenarios preferred

**CODING QUESTIONS (HackerRank Style):**
- Must include: Problem Statement, Function Description, Input/Output Format, Constraints
- Provide 3 visible sample test cases with explanations
- Provide 3 hidden test cases (no explanations)
- Include starter code template in {coding_language.upper()}
- Real-world scenario-based problems

**OUTPUT FORMAT (STRICT JSON):**
{{
  "mcq_questions": [
    {{
      "question_text": "Clear, specific question",
      "topic": "Topic from completed list",
      "difficulty": "easy/medium/hard",
      "options": [
        {{"option_letter": "A", "option_text": "..."}},
        {{"option_letter": "B", "option_text": "..."}},
        {{"option_letter": "C", "option_text": "..."}},
        {{"option_letter": "D", "option_text": "..."}}
      ],
      "correct_answer": "A/B/C/D",
      "points": 1
    }}
  ],
  "coding_questions": [
    {{
      "question_text": "**Problem Statement:**\\nClear description of the problem.\\n\\n**Function Description:**\\nComplete the function functionName in the editor below.\\n\\nfunctionName has the following parameter(s):\\n- param1: description\\n\\n**Returns:**\\n- returnType: description\\n\\n**Input Format:**\\nDescription of input format\\n\\n**Output Format:**\\nDescription of output format\\n\\n**Constraints:**\\n- Constraint 1\\n- Constraint 2",
      "topic": "Topic from completed list",
      "difficulty": "easy/medium/hard",
      "visible_test_cases": [
        {{"input": "sample input 1", "output": "expected output 1", "explanation": "why this output"}},
        {{"input": "sample input 2", "output": "expected output 2", "explanation": "why this output"}},
        {{"input": "sample input 3", "output": "expected output 3", "explanation": "why this output"}}
      ],
      "hidden_test_cases": [
        {{"input": "hidden input 1", "output": "hidden output 1"}},
        {{"input": "hidden input 2", "output": "hidden output 2"}},
        {{"input": "hidden input 3", "output": "hidden output 3"}}
      ],
      "starter_code": "def functionName(param):\\n    # Write your code here\\n    pass",
      "points": 10
    }}
  ]
}}

Generate {mcq_count} MCQs and {coding_count} coding questions NOW in this exact JSON format."""

        try:
            # Using Groq for now (Phase 3 setup)
            from groq import Groq
            client = Groq(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                content = content[json_start:json_end]
            
            questions_data = json.loads(content)
            
            # Validate that we have the expected structure
            if "mcq_questions" in questions_data and "coding_questions" in questions_data:
                print(f"✓ Successfully generated {len(questions_data['mcq_questions'])} MCQs and {len(questions_data['coding_questions'])} coding questions")
                return questions_data
            else:
                print("AI response missing expected structure, using fallback")
                return self._generate_fallback_questions(completed_topics, mcq_count, coding_count)
            
        except Exception as e:
            print(f"Error generating mock test: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to default questions
            return self._generate_fallback_questions(completed_topics, mcq_count, coding_count)
    
    def _generate_fallback_questions(self, topics: List[str], mcq_count: int, coding_count: int):
        """Generate better fallback questions when AI fails"""
        
        # Sample questions database for different topics
        sample_mcqs = {
            "Variables": {
                "question": "What is the correct way to declare a variable in Python?",
                "options": [
                    {"option_letter": "A", "option_text": "var x = 10"},
                    {"option_letter": "B", "option_text": "x = 10"},
                    {"option_letter": "C", "option_text": "int x = 10"},
                    {"option_letter": "D", "option_text": "declare x = 10"}
                ],
                "correct": "B"
            },
            "Data Types": {
                "question": "Which data type is mutable in Python?",
                "options": [
                    {"option_letter": "A", "option_text": "Tuple"},
                    {"option_letter": "B", "option_text": "String"},
                    {"option_letter": "C", "option_text": "List"},
                    {"option_letter": "D", "option_text": "Integer"}
                ],
                "correct": "C"
            },
            "Functions": {
                "question": "What keyword is used to define a function in Python?",
                "options": [
                    {"option_letter": "A", "option_text": "function"},
                    {"option_letter": "B", "option_text": "def"},
                    {"option_letter": "C", "option_text": "func"},
                    {"option_letter": "D", "option_text": "define"}
                ],
                "correct": "B"
            },
            "Loops": {
                "question": "Which loop is used when the number of iterations is unknown?",
                "options": [
                    {"option_letter": "A", "option_text": "for loop"},
                    {"option_letter": "B", "option_text": "while loop"},
                    {"option_letter": "C", "option_text": "do-while loop"},
                    {"option_letter": "D", "option_text": "foreach loop"}
                ],
                "correct": "B"
            },
            "default": {
                "question": "What is a fundamental concept in programming?",
                "options": [
                    {"option_letter": "A", "option_text": "Variables and data storage"},
                    {"option_letter": "B", "option_text": "Control flow and logic"},
                    {"option_letter": "C", "option_text": "Functions and modularity"},
                    {"option_letter": "D", "option_text": "All of the above"}
                ],
                "correct": "D"
            }
        }
        
        mcq_questions = []
        for i in range(mcq_count):
            topic = topics[i % len(topics)]
            # Find matching sample or use default
            sample = None
            for key in sample_mcqs:
                if key.lower() in topic.lower():
                    sample = sample_mcqs[key]
                    break
            if not sample:
                sample = sample_mcqs["default"]
            
            mcq_questions.append({
                "question_text": f"{sample['question']} (Topic: {topic})",
                "topic": topic,
                "difficulty": ["easy", "medium", "hard"][i % 3],
                "options": sample["options"],
                "correct_answer": sample["correct"],
                "points": 1
            })
        
        coding_questions = []
        for i in range(coding_count):
            topic = topics[i % len(topics)]
            coding_questions.append({
                "question_text": f"""Problem Statement: Solve a problem related to {topic}.

Function Description:
Complete the function solve in the editor below.

solve has the following parameter(s):
- input_data: the input string

Returns:
- string: the expected result

Input Format:
A single line containing the input.

Output Format:
A single line containing the output.

Constraints:
- Input length: 1 ≤ n ≤ 100
""",
                "topic": topic,
                "difficulty": ["easy", "medium", "hard"][i % 3],
                "visible_test_cases": [
                    {"input": "test1", "output": "result1", "explanation": "Sample test case"},
                    {"input": "test2", "output": "result2", "explanation": "Sample test case"}
                ],
                "hidden_test_cases": [
                    {"input": "hidden1", "output": "result3"},
                    {"input": "hidden2", "output": "result4"}
                ],
                "starter_code": f"def solve_{topic.lower().replace(' ', '_')}(input_data):\n    # Write your solution here\n    # This should implement logic for {topic}\n    pass",
                "points": 5
            })
        
        return {
            "mcq_questions": mcq_questions,
            "coding_questions": coding_questions
        }
    
    def generate_test_feedback(
        self, 
        mcq_score: float,
        coding_score: float,
        weak_topics: List[str],
        strong_topics: List[str],
        role_name: str
    ) -> Dict[str, str]:
        """
        Generate personalized AI feedback and improvement plan
        """
        
        prompt = f"""You are an AI career coach for a {role_name} candidate.

**Performance Summary:**
- MCQ Score: {mcq_score}%
- Coding Score: {coding_score}%
- Strong Areas: {', '.join(strong_topics) if strong_topics else 'None yet'}
- Weak Areas: {', '.join(weak_topics) if weak_topics else 'None'}

**Task:**
Generate:
1. **Personalized Feedback** (3-4 sentences): Encouraging, specific, actionable
2. **Improvement Plan** (3-5 bullet points): Concrete steps to improve

Format as JSON:
{{
  "feedback": "Your personalized feedback here...",
  "improvement_plan": "• Step 1\\n• Step 2\\n• Step 3"
}}"""

        try:
            from groq import Groq
            client = Groq(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1:
                content = content[json_start:json_end]
            
            return json.loads(content)
            
        except:
            return {
                "feedback": "Keep practicing! Focus on your weak areas and you'll improve.",
                "improvement_plan": "• Review weak topics\n• Practice more problems\n• Take regular tests"
            }
    
    def calculate_career_dna(
        self,
        test_scores: List[float],
        time_taken_list: List[int],
        accuracy_history: List[float]
    ) -> Dict[str, float]:
        """
        Calculate Career DNA dimensions from performance data
        """
        
        # Logical ability: Based on average score
        logical_ability = min(sum(test_scores) / len(test_scores) / 100, 1.0) if test_scores else 0.5
        
        # Problem-solving: Based on coding performance (assume last 30% of scores are coding)
        problem_solving = 0.5
        if len(test_scores) >= 3:
            recent_scores = test_scores[-3:]
            problem_solving = min(sum(recent_scores) / len(recent_scores) / 100, 1.0)
        
        # Speed: Based on time taken (faster = higher score)
        speed = 0.5
        if time_taken_list:
            avg_time = sum(time_taken_list) / len(time_taken_list)
            speed = min(max(1.0 - (avg_time / 120), 0.0), 1.0)  # Normalized to 2 hours
        
        # Consistency: Based on score variance
        consistency = 0.5
        if len(test_scores) >= 3:
            variance = sum((s - logical_ability * 100) ** 2 for s in test_scores) / len(test_scores)
            consistency = min(max(1.0 - (variance / 1000), 0.0), 1.0)
        
        # Learning efficiency: Based on accuracy improvement
        learning_efficiency = 0.5
        if len(accuracy_history) >= 2:
            improvement = accuracy_history[-1] - accuracy_history[0]
            learning_efficiency = min(max(0.5 + (improvement / 100), 0.0), 1.0)
        
        overall = (logical_ability + problem_solving + speed + consistency + learning_efficiency) / 5
        
        return {
            "logical_ability": round(logical_ability, 2),
            "problem_solving": round(problem_solving, 2),
            "speed": round(speed, 2),
            "consistency": round(consistency, 2),
            "learning_efficiency": round(learning_efficiency, 2),
            "overall_score": round(overall, 2)
        }
    
    def generate_career_forecast(
        self,
        career_dna_score: float,
        skills_mastered: List[Dict[str, float]],
        role_name: str
    ) -> Dict[str, Any]:
        """
        Generate career readiness forecast
        """
        
        # Calculate readiness scores
        avg_skill_mastery = sum(s['mastery_level'] for s in skills_mastered) / len(skills_mastered) if skills_mastered else 0.3
        
        internship_readiness = min((career_dna_score * 0.4 + avg_skill_mastery * 0.6), 1.0)
        placement_readiness = min((career_dna_score * 0.5 + avg_skill_mastery * 0.5), 1.0)
        project_readiness = min((avg_skill_mastery * 0.7 + career_dna_score * 0.3), 1.0)
        
        # Estimate timeline
        days_to_internship = max(int((1.0 - internship_readiness) * 90), 0)
        days_to_placement = max(int((1.0 - placement_readiness) * 180), 0)
        
        return {
            "internship_readiness": round(internship_readiness, 2),
            "placement_readiness": round(placement_readiness, 2),
            "project_readiness": round(project_readiness, 2),
            "estimated_days_to_internship": days_to_internship,
            "estimated_days_to_placement": days_to_placement,
            "success_probability": round((internship_readiness + placement_readiness) / 2, 2),
            "forecast_summary": f"You are {int(placement_readiness * 100)}% ready for {role_name} placement. Keep building your skills!",
            "recommended_actions": [
                "Focus on weak topics identified in tests",
                "Build 2-3 strong projects",
                "Practice coding daily",
                "Participate in mock interviews"
            ]
        }


# Global instance
phase6_ai_service = Phase6AIService()
