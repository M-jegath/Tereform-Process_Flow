import re

def clean_text(raw_text: str) -> str:
    """
    Cleans the raw text by removing unnecessary whitespace, 
    empty lines, and normalizing formatting.
    """
    if not raw_text:
        return ""
        
    # Split into lines
    lines = raw_text.splitlines()
    
    # Strip whitespace and remove empty lines
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    
    # Join with single spaces
    text = " ".join(cleaned_lines)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def is_terraform_relevant(text: str) -> bool:
    """
    Simple heuristic check to see if the text is relevant to Terraform or Infrastructure.
    """
    text_lower = text.lower()
    
    keywords = [
        "terraform", "infrastructure", "aws", "gcp", "azure", 
        "ec2", "s3", "vpc", "security group", "instance",
        "cloud", "provider", "resource", "bucket", "deploy"
    ]
    
    # Count how many keywords appear in the text
    matches = sum(1 for kw in keywords if kw in text_lower)
    
    # If we have at least one keyword, we assume it's relevant enough to try parsing.
    # We can adjust this threshold as needed.
    return matches > 0
