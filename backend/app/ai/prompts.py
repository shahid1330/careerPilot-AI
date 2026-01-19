"""
AI Prompt Templates
Structured prompts for LLM interactions
"""


class PromptTemplates:
    """
    Centralized prompt templates for AI services
    """
    
    @staticmethod
    def roadmap_generation(role_name: str, duration_days: int = 90) -> str:
        """
        Generate a prompt for creating a career roadmap
        
        Args:
            role_name: The job role or career path
            
        Returns:
            Formatted prompt string
        """
        return f"""You are a career guidance expert. Generate a comprehensive career roadmap for: {role_name}

Your response MUST be a valid JSON object with this EXACT structure:
{{
    "role": "{role_name}",
    "required_skills": [
        "skill1",
        "skill2",
        "skill3"
    ],
    "learning_path": [
        {{
            "phase": "Fundamentals",
            "topics": ["topic1", "topic2"],
            "duration_weeks": 4
        }},
        {{
            "phase": "Intermediate",
            "topics": ["topic3", "topic4"],
            "duration_weeks": 8
        }},
        {{
            "phase": "Advanced",
            "topics": ["topic5", "topic6"],
            "duration_weeks": 8
        }}
    ],
    "recommended_projects": [
        "project1",
        "project2"
    ]
}}

Generate a detailed and practical roadmap. Return ONLY the JSON object, no additional text."""
    
    @staticmethod
    def daily_plan_generation(role_name: str, duration_days: int) -> str:
        """
        Generate a prompt for creating a daily learning plan
        
        Args:
            role_name: The job role or career path
            duration_days: Number of days for the plan
            
        Returns:
            Formatted prompt string
        """
        return f"""You are a learning plan expert. Create a {duration_days}-day study plan for: {role_name}

Your response MUST be a valid JSON object with this EXACT structure:
{{
    "total_days": {duration_days},
    "daily_plan": [
        {{
            "day": 1,
            "topic": "Introduction to {role_name} - Overview and Setup",
            "estimated_hours": 3
        }},
        {{
            "day": 2,
            "topic": "Core Concepts Part 1",
            "estimated_hours": 4
        }}
    ]
}}

Requirements:
- Create exactly {duration_days} daily entries
- Each day should have a focused topic
- Estimated hours should be realistic (2-6 hours per day)
- Topics should build progressively
- Cover fundamentals to advanced concepts

Return ONLY the JSON object, no additional text."""
    
    @staticmethod
    def teach_topic(topic: str, context: str = None) -> str:
        """
        Generate a prompt for teaching a specific topic
        
        Args:
            topic: The topic to explain
            context: Optional additional context
            
        Returns:
            Formatted prompt string
        """
        context_text = f"\n\nAdditional context: {context}" if context else ""
        topic_encoded = topic.replace(' ', '+')
        
        return f"""You are an expert teacher. Explain the following topic: {topic}{context_text}

CRITICAL: Your response must be ONLY a JSON object. NO code examples, NO markdown, NO explanations outside the JSON.

Return this EXACT JSON structure:
{{
    "topic": "{topic}",
    "explanation": "A clear, detailed explanation of the topic. Use \\n for line breaks within this string.",
    "examples": [
        "Example 1: Brief description of the example",
        "Example 2: Brief description of the example", 
        "Example 3: Brief description of the example"
    ],
    "resources": [
        "Official Documentation: [actual official docs URL for {topic}]",
        "GeeksforGeeks Tutorial: https://www.geeksforgeeks.org/{topic_encoded}/",
        "W3Schools Guide: https://www.w3schools.com/[relevant-section]",
        "Code With Harry Video: https://www.youtube.com/watch?v=[video-id]",
        "Apna College Video: https://www.youtube.com/watch?v=[video-id]",
        "Chai aur Code Video: https://www.youtube.com/watch?v=[video-id]",
        "Scaler Article: https://www.scaler.com/topics/[relevant-topic]"
    ]
}}

CRITICAL REQUIREMENTS FOR RESOURCES:
1. Official Documentation (1st resource):
   - For JavaScript/Web: https://developer.mozilla.org/en-US/docs/Web/JavaScript/[specific-topic]
   - For Python: https://docs.python.org/3/library/[module].html or https://docs.python.org/3/tutorial/[topic].html
   - For React: https://react.dev/reference/react/[component-or-hook]
   - For Node.js: https://nodejs.org/api/[module].html
   - For Java: https://docs.oracle.com/en/java/javase/[version]/docs/api/
   - Provide the EXACT real documentation URL for the specific topic

2. GeeksforGeeks (2nd resource):
   - Use format: https://www.geeksforgeeks.org/[topic-name-with-hyphens]/
   - Example: For "Binary Search" → https://www.geeksforgeeks.org/binary-search/
   - For "React Hooks" → https://www.geeksforgeeks.org/reactjs-hooks/

3. W3Schools (3rd resource):
   - Use real sections like: /js/, /python/, /react/, /sql/, /css/, /html/
   - Example: For JavaScript → https://www.w3schools.com/js/js_[specific_topic].asp

4. YouTube Videos (4th, 5th, 6th resources):
   Use YouTube search URLs that will show videos from specific channels about the topic.
   These URLs will ALWAYS work and show relevant videos:
   
   a) Code With Harry:
      Format: "Code With Harry - {topic}: https://www.youtube.com/results?search_query=code+with+harry+{topic_encoded}"
   
   b) Apna College:
      Format: "Apna College - {topic}: https://www.youtube.com/results?search_query=apna+college+{topic_encoded}"
   
   c) Chai aur Code:
      Format: "Chai aur Code - {topic}: https://www.youtube.com/results?search_query=chai+aur+code+{topic_encoded}"
   
   Example for topic "React Hooks":
   - "Code With Harry - React Hooks: https://www.youtube.com/results?search_query=code+with+harry+react+hooks"
   - "Apna College - React Hooks: https://www.youtube.com/results?search_query=apna+college+react+hooks"
   - "Chai aur Code - React Hooks: https://www.youtube.com/results?search_query=chai+aur+code+react+hooks"

5. Scaler (7th resource):
   - Format: https://www.scaler.com/topics/[language]/[topic-name]/
   - Example: https://www.scaler.com/topics/python/python-variables/

IMPORTANT:
- Replace [placeholders] with actual topic-specific paths
- For YouTube, try to use actual video IDs if you know them, otherwise use channel search URLs
- All URLs must follow the actual URL structure of these platforms
- Construct real URLs based on the topic given

RULES:
1. Return ONLY valid JSON - no code blocks, no markdown, no extra text
2. Do NOT include code examples in the response - only descriptions
3. Keep examples as text descriptions, not actual code
4. Use \\n for line breaks inside JSON strings
5. Ensure proper JSON escaping for quotes and special characters

Your entire response must be parseable by JSON.parse(). Start with {{ and end with }}.
- Do NOT include actual line breaks inside string values
- Return ONLY the JSON object, no markdown code blocks, no additional text
- Ensure the JSON is complete and valid

Make the explanation practical and actionable. Return ONLY the JSON object, no additional text."""
