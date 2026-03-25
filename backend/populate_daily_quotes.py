"""
Populate daily_quotes table with motivational quotes
Run once to seed the database
"""

from app.core.database import SessionLocal
from app.models.mock_test_v2 import DailyQuote

def populate_quotes():
    db = SessionLocal()
    
    quotes = [
        {
            "quote_text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
            "category": "motivation"
        },
        {
            "quote_text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "author": "Winston Churchill",
            "category": "success"
        },
        {
            "quote_text": "Learning never exhausts the mind.",
            "author": "Leonardo da Vinci",
            "category": "learning"
        },
        {
            "quote_text": "The future belongs to those who believe in the beauty of their dreams.",
            "author": "Eleanor Roosevelt",
            "category": "motivation"
        },
        {
            "quote_text": "It does not matter how slowly you go as long as you do not stop.",
            "author": "Confucius",
            "category": "motivation"
        },
        {
            "quote_text": "Code is like humor. When you have to explain it, it's bad.",
            "author": "Cory House",
            "category": "learning"
        },
        {
            "quote_text": "First, solve the problem. Then, write the code.",
            "author": "John Johnson",
            "category": "learning"
        },
        {
            "quote_text": "Experience is the name everyone gives to their mistakes.",
            "author": "Oscar Wilde",
            "category": "learning"
        },
        {
            "quote_text": "The expert in anything was once a beginner.",
            "author": "Helen Hayes",
            "category": "motivation"
        },
        {
            "quote_text": "Success is the sum of small efforts repeated day in and day out.",
            "author": "Robert Collier",
            "category": "success"
        },
        {
            "quote_text": "Don't watch the clock; do what it does. Keep going.",
            "author": "Sam Levenson",
            "category": "motivation"
        },
        {
            "quote_text": "The only limit to our realization of tomorrow will be our doubts of today.",
            "author": "Franklin D. Roosevelt",
            "category": "motivation"
        },
        {
            "quote_text": "Strive not to be a success, but rather to be of value.",
            "author": "Albert Einstein",
            "category": "success"
        },
        {
            "quote_text": "Quality is not an act, it is a habit.",
            "author": "Aristotle",
            "category": "learning"
        },
        {
            "quote_text": "The best time to plant a tree was 20 years ago. The second best time is now.",
            "author": "Chinese Proverb",
            "category": "motivation"
        }
    ]
    
    # Check if quotes already exist
    existing = db.query(DailyQuote).count()
    if existing > 0:
        print(f"✓ Database already has {existing} quotes. Skipping.")
        db.close()
        return
    
    # Add all quotes
    for quote_data in quotes:
        quote = DailyQuote(**quote_data)
        db.add(quote)
    
    db.commit()
    print(f"✓ Successfully added {len(quotes)} motivational quotes to database")
    db.close()

if __name__ == "__main__":
    populate_quotes()
