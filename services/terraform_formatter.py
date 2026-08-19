import os
import subprocess
from config.settings import GENERATED_DIR

def format_terraform(code: str) -> str:
    """
    Saves the HCL code to a file and runs `terraform fmt`.
    Returns the formatted HCL code.
    """
    file_path = os.path.join(GENERATED_DIR, "main.tf")
    
    # Save the code
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
        
    try:
        # Run terraform fmt
        result = subprocess.run(
            ["terraform", "fmt", "main.tf"],
            cwd=GENERATED_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Read the formatted code back
        with open(file_path, "r", encoding="utf-8") as f:
            formatted_code = f.read()
            
        return formatted_code
    except subprocess.CalledProcessError as e:
        # If terraform fmt fails (e.g. invalid syntax), we might want to return the original code
        # or raise an exception. For formatting, we can just return the original code and let
        # validation catch the syntax error.
        return code
    except FileNotFoundError:
        raise Exception("Terraform CLI is not installed or not in PATH.")
