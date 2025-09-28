import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from textblob import TextBlob
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class TextSummarizer:
    def __init__(self):
        self.available_methods = {
            'lsa': LsaSummarizer(),
            'text_rank': TextRankSummarizer(),
            'luhn': LuhnSummarizer(),
            'lex_rank': LexRankSummarizer()
        }
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        return text.strip()
    
    def get_sentences_count(self, text, sentences_count=None):
        """Calculate appropriate number of sentences for summary"""
        if sentences_count:
            return min(sentences_count, 20)  # Limit to 20 sentences max
        
        # Default: 30% of original sentences, min 3, max 10
        original_sentences = len(nltk.sent_tokenize(text))
        calculated = max(3, min(10, int(original_sentences * 0.3)))
        return calculated
    
    def summarize(self, text, method='lsa', sentences_count=None, language='english'):
        """Summarize text using specified method"""
        try:
            # Clean the text
            text = self.clean_text(text)
            
            if len(text.split()) < 50:
                return text, len(text.split()), len(text.split()), 1.0
            
            # Calculate sentences count
            sentences_count = self.get_sentences_count(text, sentences_count)
            
            # Parse text
            parser = PlaintextParser.from_string(text, Tokenizer(language))
            
            # Get summarizer
            summarizer = self.available_methods.get(method, self.available_methods['lsa'])
            
            # Generate summary
            summary_sentences = summarizer(parser.document, sentences_count)
            summary = ' '.join(str(sentence) for sentence in summary_sentences)
            
            # Calculate metrics
            original_length = len(text.split())
            summary_length = len(summary.split())
            compression_ratio = original_length / summary_length if summary_length > 0 else 1.0
            
            return summary, summary_length, original_length, compression_ratio
            
        except Exception as e:
            # Fallback to simple summary
            sentences = nltk.sent_tokenize(text)
            summary_sentences = sentences[:min(5, len(sentences))]
            summary = ' '.join(summary_sentences)
            
            original_length = len(text.split())
            summary_length = len(summary.split())
            compression_ratio = original_length / summary_length if summary_length > 0 else 1.0
            
            return summary, summary_length, original_length, compression_ratio
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        blob = TextBlob(text)
        return blob.sentiment.polarity
    
    def get_text_stats(self, text):
        """Get basic text statistics"""
        words = text.split()
        sentences = nltk.sent_tokenize(text)
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0
        }

summarizer = TextSummarizer()

