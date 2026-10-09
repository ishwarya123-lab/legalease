from google import genai
from app.config import settings
import json

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_document(document_type: str, data: dict) -> tuple[str, str]:
    prompt = f"""
    You are an expert full-stack AI legal engineer. Generate a highly professional, strictly formatted {document_type} agreement.
    
    Here are the details provided:
    {json.dumps(data, indent=2)}

    Format the output strictly as follows:
    ---TERMS---
    Create a clean Markdown table summarizing the key terms (Term | Value).
    ---DOCUMENT---
    Write the full legal document in Markdown. Include clear clause numbering, definitions, recitals, and clear placeholder-free drafting.
    Ensure professional formatting with appropriate headings (use Markdown headers #, ##, ###). Do NOT use #### headers, do NOT use HTML tags (like <br>), do NOT use markdown tables or horizontal rules (---) in the document body. Use standard numbered lists and clean paragraphs. Do not include any placeholders; use the provided details directly.
    IMPORTANT: Format all monetary values in Indian Rupees (INR / ₹) unless the user explicitly provided a different currency symbol in the details. Do not use USD or $ by default.
    """
    
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=prompt
    )
    text = interaction.output_text
    
    # Simple parser
    parts = text.split("---DOCUMENT---")
    if len(parts) == 2:
        terms_part = parts[0].replace("---TERMS---", "").strip()
        doc_part = parts[1].strip()
        return doc_part, terms_part
    elif "---TERMS---" in text:
        terms_part = text.split("---TERMS---")[1].split("---DOCUMENT---")[0].strip()
        doc_part = text.split("---DOCUMENT---")[1].strip() if "---DOCUMENT---" in text else text
        return doc_part, terms_part
    
    return text, "Term table could not be generated."
