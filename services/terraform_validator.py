import os
import subprocess
from typing import Tuple, Optional
from config.settings import GENERATED_DIR

def validate_terraform() -> Tuple[bool, Optional[str]]:
    """
    Runs `terraform init` and `terraform validate` on the generated code.
    Returns (is_valid, error_message)
    """
    try:
        # Initialize Terraform (needed for validate to check provider requirements)
        init_result = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=GENERATED_DIR,
            capture_output=True,
            text=True,
            check=False # Don't raise immediately so we can get error output
        )
        
        if init_result.returncode != 0:
            return False, f"Terraform Init Failed:\n{init_result.stderr or init_result.stdout}"
            
        # Validate Terraform
        val_result = subprocess.run(
            ["terraform", "validate", "-json"],
            cwd=GENERATED_DIR,
            capture_output=True,
            text=True,
            check=False
        )
        
        if val_result.returncode == 0:
            return True, None
        else:
            # We could parse the JSON output to get a cleaner message, 
            # but stderr or stdout will have the raw output.
            import json
            try:
                error_data = json.loads(val_result.stdout)
                error_msgs = [diag["summary"] + ": " + diag["detail"] for diag in error_data.get("diagnostics", [])]
                return False, "\n".join(error_msgs)
            except:
                return False, val_result.stderr or val_result.stdout
                
    except FileNotFoundError:
        raise Exception("Terraform CLI is not installed or not in PATH.")
    except Exception as e:
        return False, str(e)
