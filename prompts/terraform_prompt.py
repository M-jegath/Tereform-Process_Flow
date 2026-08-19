import json
from models.schemas import TerraformRequirements

TERRAFORM_SYSTEM_PROMPT = """
You are an expert Terraform Developer.
Your task is to generate valid Terraform (HCL) code from structured JSON requirements.

Follow these rules:
1. ONLY return the valid HCL code.
2. DO NOT return any markdown formatting like ```hcl or ```. Just the raw code.
3. Ensure syntax is correct and all required fields are present.
4. Synthesize the resource configuration by combining `explicit_properties`, `inferred_properties`, and `default_properties`. 
5. **CRITICAL:** If an OS (like Ubuntu) is specified for an instance in the `explicit_properties`, you MUST use a `data "aws_ami"` block to dynamically fetch the correct AMI instead of hardcoding an AMI string. If a specific OS version (e.g., Ubuntu 22.04) is requested, make sure your data block's `filter { values = [...] }` explicitly narrows it down to that specific version, rather than a broad wildcard wildcard.
6. **CRITICAL:** If a name is specified for an instance, you MUST apply it as a `tags = { Name = "..." }` block, rather than just the logical Terraform resource name.
"""

def build_terraform_user_prompt(requirements: TerraformRequirements) -> str:
    return f"""
Generate Terraform configuration based on the following structured requirements:

{json.dumps(requirements.model_dump(), indent=2)}
"""

TERRAFORM_CORRECTION_PROMPT = """
You are an expert Terraform Developer.
The generated Terraform failed validation.

Original requirements:
{requirements}

Generated Terraform:
{terraform_code}

Terraform validation error:
{error_message}

Correct the Terraform configuration based on the error.
Ensure that:
1. You use the correct provider and region blocks.
2. You create the corresponding resources.
3. You map all properties accurately based on the requirements, combining `explicit_properties`, `inferred_properties`, and `default_properties`.
4. **CRITICAL:** If an OS (like Ubuntu) is specified for an instance in the `explicit_properties`, you MUST use a `data "aws_ami"` block to dynamically fetch the correct AMI instead of hardcoding an AMI string. If a specific OS version (e.g., Ubuntu 22.04) is requested, make sure your data block's `filter { values = [...] }` explicitly narrows it down to that specific version, rather than a broad wildcard wildcard.
5. **CRITICAL:** If a name is specified for an instance, you MUST apply it as a `tags = { Name = "..." }` block, rather than just the logical Terraform resource name.

Output ONLY valid Terraform HCL code. Do not include any explanations.
"""
