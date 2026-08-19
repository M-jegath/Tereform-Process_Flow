import json
from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL
from models.schemas import TerraformRequirements
from prompts.semantic_prompt import (
    SEMANTIC_VERIFIER_SYSTEM_PROMPT,
    build_semantic_verifier_prompt,
    SEMANTIC_CORRECTION_SYSTEM_PROMPT,
    build_semantic_correction_prompt
)
from services.terraform_generator import extract_hcl

# Setup Groq client
client = Groq(api_key=GROQ_API_KEY)

def verify_semantics(requirements: TerraformRequirements, terraform_code: str) -> tuple[bool, list[str]]:
    """
    Verifies if the Terraform code semantically meets the requirements.
    Returns (is_valid, list_of_missing_requirements).
    """
    try:
        req_json_str = requirements.model_dump_json(indent=2)
        user_prompt = build_semantic_verifier_prompt(req_json_str, terraform_code)
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SEMANTIC_VERIFIER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        
        is_valid = result.get("is_valid", False)
        missing = result.get("missing_requirements", [])
        
        return is_valid, missing
        
    except Exception as e:
        raise Exception(f"Failed to verify semantics: {str(e)}")

def correct_semantics(terraform_code: str, missing_requirements: list[str], requirements_json: str = "{}") -> str:
    """
    Corrects the Terraform code based on the missing semantic requirements.
    """
    try:
        user_prompt = build_semantic_correction_prompt(terraform_code, missing_requirements, requirements_json)
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SEMANTIC_CORRECTION_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        
        raw_code = response.choices[0].message.content
        return extract_hcl(raw_code)
        
    except Exception as e:
        raise Exception(f"Failed to correct semantics: {str(e)}")
