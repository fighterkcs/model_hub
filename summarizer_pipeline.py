from transformers import pipeline

primary_summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

fallback_summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-xsum"
)

def summarizer(text):
    try:
        summary=primary_summarizer(text, max_length=150, min_length=40, do_sample=False)
    except Exception as e:
        summary=fallback_summarizer(text, max_length=150, min_length=40, do_sample=False)   
    return summary[0]['summary_text']

