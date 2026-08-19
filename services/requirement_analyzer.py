import json
from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL
from models.schemas import TerraformRequirements
from prompts.requirement_prompt import REQUIREMENT_SYSTEM_PROMPT, build_requirement_user_prompt

# Setup Groq client
client = Groq(api_key=GROQ_API_KEY)

def analyze_requirements(cleaned_text: str) -> TerraformRequirements:
    """
    Sends the cleaned text to the LLM and returns structured TerraformRequirements.
    """
    try:
        user_prompt = build_requirement_user_prompt(cleaned_text)
        
        # Inject schema into the prompt because Groq JSON mode requires it
        schema_str = json.dumps(TerraformRequirements.model_json_schema(), indent=2)
        system_content = f"{REQUIREMENT_SYSTEM_PROMPT}\\n\\nYou MUST strictly adhere to this exact JSON schema:\\n{schema_str}\\n\\nRespond strictly in valid JSON."

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        req_data = json.loads(content)
        return TerraformRequirements(**req_data)
        
    except Exception as e:
        raise Exception(f"Failed to analyze requirements: {str(e)}")
