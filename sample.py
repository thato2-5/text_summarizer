import os
import sys
import random
from datetime import datetime, timedelta
from faker import Faker
import requests
from bs4 import BeautifulSoup

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Summary

fake = Faker()

class SampleDataGenerator:
    def __init__(self):
        self.users = []
        self.summaries = []
        self.sample_texts = []
        
    def generate_sample_texts(self):
        """Generate or fetch sample texts for summarization"""
        print("Generating sample texts...")
        
        # Sample texts from various domains
        sample_texts = [
            # Technology
            """
            Artificial intelligence is transforming industries across the globe. Machine learning algorithms 
            are being used to analyze vast amounts of data, identify patterns, and make predictions with 
            unprecedented accuracy. Companies are leveraging AI to improve customer service through chatbots, 
            optimize supply chains, and develop innovative products. The field continues to evolve rapidly, 
            with new breakthroughs in natural language processing and computer vision emerging regularly.
            """,
            
            # Science
            """
            Climate change represents one of the most significant challenges facing humanity today. 
            Rising global temperatures are causing polar ice caps to melt, leading to sea level rise 
            that threatens coastal communities worldwide. Scientists warn that without immediate action 
            to reduce greenhouse gas emissions, we may reach a point of no return. Renewable energy 
            sources like solar and wind power offer promising alternatives to fossil fuels, but 
            widespread adoption requires substantial infrastructure investment and policy changes.
            """,
            
            # Business
            """
            The global economy is experiencing significant shifts due to digital transformation. 
            E-commerce has grown exponentially, with more consumers preferring online shopping 
            over traditional brick-and-mortar stores. Remote work has become increasingly common, 
            changing how companies operate and manage their workforce. Businesses that adapt quickly 
            to these changes are finding new opportunities for growth, while those that resist may 
            struggle to remain competitive in the evolving market landscape.
            """,
            
            # Health
            """
            Regular physical activity is essential for maintaining good health and well-being. 
            Exercise helps control weight, combat health conditions and diseases, improve mood, 
            boost energy, and promote better sleep. Most adults should aim for at least 150 minutes 
            of moderate-intensity aerobic activity or 75 minutes of vigorous-intensity activity 
            per week, along with muscle-strengthening activities on two or more days per week.
            """,
            
            # Education
            """
            Online learning has revolutionized education by making knowledge accessible to people 
            worldwide. Digital platforms offer courses on virtually every subject, allowing learners 
            to study at their own pace from anywhere with an internet connection. This democratization 
            of education has opened up opportunities for lifelong learning and skill development. 
            However, challenges remain in ensuring equal access and maintaining educational quality.
            """
        ]
        
        # Fetch additional real articles from Wikipedia
        wikipedia_topics = [
            "Renewable_energy", "Machine_learning", "Global_warming", 
            "E-commerce", "Artificial_intelligence", "Space_exploration"
        ]
        
        for topic in wikipedia_topics:
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'extract' in data:
                        sample_texts.append(data['extract'])
                print(f"Fetched Wikipedia article: {topic}")
            except Exception as e:
                print(f"Error fetching {topic}: {e}")
        
        self.sample_texts = sample_texts
        return sample_texts
    
    def generate_users(self, count=10):
        """Generate sample users"""
        print(f"Generating {count} sample users...")
        
        # Create test admin user
        admin = User(
            username='admin',
            email='admin@summarizer.com',
            created_at=datetime.utcnow() - timedelta(days=30)
        )
        admin.set_password('admin123')
        self.users.append(admin)
        
        # Create regular users
        for i in range(count - 1):
            user = User(
                username=fake.user_name() + str(i),
                email=fake.email(),
                created_at=fake.date_time_between(
                    start_date='-90d', 
                    end_date='now'
                )
            )
            user.set_password('password123')
            self.users.append(user)
            
        return self.users
    
    def generate_summary(self, text, user):
        """Generate a realistic summary for given text"""
        # Simple summarization logic for sample data
        sentences = text.split('. ')
        if len(sentences) <= 3:
            summary = text  # Too short to summarize
        else:
            # Take first, middle, and last sentences for variety
            summary_sentences = [
                sentences[0],
                sentences[len(sentences)//2],
                sentences[-1]
            ]
            summary = '. '.join([s for s in summary_sentences if s.strip()]) + '.'
        
        # Calculate metrics
        original_length = len(text.split())
        summary_length = len(summary.split())
        compression_ratio = original_length / summary_length if summary_length > 0 else 1.0
        
        return {
            'summary': summary,
            'original_length': original_length,
            'summary_length': summary_length,
            'compression_ratio': round(compression_ratio, 2)
        }
    
    def generate_summaries(self, summaries_per_user=5):
        """Generate sample summaries for all users"""
        print(f"Generating {summaries_per_user} summaries per user...")
        
        if not self.sample_texts:
            self.generate_sample_texts()
        
        for user in self.users:
            for i in range(summaries_per_user):
                # Select random text
                text = random.choice(self.sample_texts)
                
                # Generate summary
                summary_data = self.generate_summary(text, user)
                
                # Create random creation date (within user's account lifetime)
                days_since_joined = (datetime.utcnow() - user.created_at).days
                random_days = random.randint(0, min(days_since_joined, 90))
                created_at = user.created_at + timedelta(days=random_days)
                
                summary = Summary(
                    original_text=text,
                    summary_text=summary_data['summary'],
                    summary_length=summary_data['summary_length'],
                    original_length=summary_data['original_length'],
                    compression_ratio=summary_data['compression_ratio'],
                    user_id=user.id,
                    title=text[:97] + '...' if len(text) > 100 else text,
                    language='english',
                    created_at=created_at
                )
                
                self.summaries.append(summary)
        
        return self.summaries
    
    def create_sample_data(self, user_count=10, summaries_per_user=5):
        """Main method to create all sample data"""
        print("Starting sample data generation...")
        
        with app.app_context():
            # Clear existing data
            print("Clearing existing data...")
            db.drop_all()
            db.create_all()
            
            # Generate data
            self.generate_users(user_count)
            self.generate_sample_texts()
            self.generate_summaries(summaries_per_user)
            
            # Add to database
            print("Adding users to database...")
            for user in self.users:
                db.session.add(user)
            db.session.commit()
            
            print("Adding summaries to database...")
            for summary in self.summaries:
                db.session.add(summary)
            db.session.commit()
            
            print("Sample data generation completed successfully!")
            
            # Print summary
            self.print_summary()
    
    def print_summary(self):
        """Print summary of generated data"""
        print("\n" + "="*50)
        print("SAMPLE DATA GENERATION SUMMARY")
        print("="*50)
        print(f"Users created: {len(self.users)}")
        print(f"Summaries created: {len(self.summaries)}")
        print(f"Sample texts available: {len(self.sample_texts)}")
        
        # User credentials
        print("\nTEST USER CREDENTIALS:")
        print("-" * 30)
        for user in self.users[:3]:  # Show first 3 users
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Password: password123")
            print("-" * 30)
        
        # Database stats
        total_users = User.query.count()
        total_summaries = Summary.query.count()
        print(f"\nDatabase Statistics:")
        print(f"Total users in DB: {total_users}")
        print(f"Total summaries in DB: {total_summaries}")

def generate_large_text_corpus():
    """Generate a larger corpus of text samples for more variety"""
    print("Generating larger text corpus...")
    
    corpus = []
    
    # Business articles
    business_topics = [
        "The Impact of Digital Transformation on Traditional Retail",
        "Sustainable Business Practices in the 21st Century",
        "The Rise of Remote Work and Its Effects on Productivity",
        "Innovation Strategies for Startups in Competitive Markets",
        "Global Supply Chain Challenges and Solutions"
    ]
    
    for topic in business_topics:
        article = f"""
        {topic}. This comprehensive analysis examines the current trends and future prospects 
        in this important area. Recent developments have shown significant changes in how 
        organizations approach these challenges. Experts suggest that adaptation and innovation 
        are key to success in today's rapidly evolving business environment. Companies that 
        embrace change and invest in new technologies are more likely to thrive, while those 
        that resist may face difficulties. The data indicates a clear correlation between 
        proactive strategies and positive outcomes across various industry sectors.
        """
        corpus.append(article)
    
    # Technology articles
    tech_topics = [
        "Advances in Quantum Computing and Their Potential Applications",
        "The Evolution of Cybersecurity in the Age of IoT",
        "Blockchain Technology Beyond Cryptocurrency",
        "The Future of Artificial Intelligence in Healthcare",
        "5G Technology and Its Impact on Mobile Communications"
    ]
    
    for topic in tech_topics:
        article = f"""
        {topic}. This field has seen remarkable progress in recent years, with breakthroughs 
        occurring at an accelerating pace. Researchers and developers are pushing the boundaries 
        of what's possible, creating new opportunities and challenges alike. The implications 
        for society and industry are profound, requiring careful consideration of ethical 
        and practical concerns. As these technologies mature, we can expect to see even more 
        innovative applications emerge across different domains.
        """
        corpus.append(article)
    
    # Science articles
    science_topics = [
        "Recent Discoveries in Mars Exploration",
        "The Human Microbiome and Its Role in Health",
        "Renewable Energy Storage Solutions",
        "Genetic Engineering and CRISPR Technology",
        "Climate Change Mitigation Strategies"
    ]
    
    for topic in science_topics:
        article = f"""
        {topic}. Scientific research continues to provide new insights into this important 
        area of study. Recent findings have challenged previous assumptions and opened up 
        new avenues for investigation. The international scientific community is collaborating 
        to address these complex issues, sharing data and methodologies to accelerate progress. 
        While significant challenges remain, the potential benefits of this research are 
        substantial, offering hope for solving some of humanity's most pressing problems.
        """
        corpus.append(article)
    
    return corpus

def create_performance_test_data():
    """Create larger dataset for performance testing"""
    print("Creating performance test data...")
    
    generator = SampleDataGenerator()
    
    with app.app_context():
        # Create 50 users with 20 summaries each
        generator.generate_users(50)
        generator.sample_texts = generate_large_text_corpus()
        generator.generate_summaries(20)
        
        # Add to database
        for user in generator.users:
            db.session.add(user)
        db.session.commit()
        
        for summary in generator.summaries:
            db.session.add(summary)
        db.session.commit()
        
        print(f"Performance test data created:")
        print(f"- Users: {len(generator.users)}")
        print(f"- Summaries: {len(generator.summaries)}")

def export_sample_data():
    """Export sample data to JSON files for external use"""
    import json
    from datetime import datetime
    
    generator = SampleDataGenerator()
    generator.generate_sample_texts()
    
    # Export sample texts
    texts_data = {
        'generated_at': datetime.utcnow().isoformat(),
        'sample_texts': generator.sample_texts
    }
    
    with open('sample_texts.json', 'w', encoding='utf-8') as f:
        json.dump(texts_data, f, indent=2, ensure_ascii=False)
    
    print("Sample texts exported to sample_texts.json")

if __name__ == '__main__':
    # Install required packages if not already installed
    try:
        import faker
        import requests
        import bs4
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install required packages:")
        print("pip install faker requests beautifulsoup4")
        sys.exit(1)
    
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate sample data for Text Summarizer')
    parser.add_argument('--users', type=int, default=10, help='Number of users to create')
    parser.add_argument('--summaries', type=int, default=5, help='Summaries per user')
    parser.add_argument('--performance', action='store_true', help='Create larger dataset for performance testing')
    parser.add_argument('--export', action='store_true', help='Export sample texts to JSON')
    
    args = parser.parse_args()
    
    if args.export:
        export_sample_data()
    elif args.performance:
        create_performance_test_data()
    else:
        generator = SampleDataGenerator()
        generator.create_sample_data(
            user_count=args.users,
            summaries_per_user=args.summaries
        )

