from transformers import pipeline

class NewsProcessor:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization", 
            model="facebook/bart-large-cnn"
        )
    
    def summarize(self, text):
        """Generate a summary of the article"""
        try:
            summary = self.summarizer(
                text,
                max_length=150,
                min_length=30,
                do_sample=False
            )
            return summary[0]['summary_text']
        except:
            return "Summary unavailable"
    
    def clean_text(self, text):
        """Basic text cleaning"""
        text = text.replace("\n", " ").replace("\t", " ")
        return ' '.join(text.split())  # Remove extra spaces