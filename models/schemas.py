from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class TerraformResource(BaseModel):
    type: str = Field(description="The terraform resource type, e.g., aws_instance, aws_s3_bucket")
    name: str = Field(description="A logical name for the resource in terraform")
    explicit_properties: Dict[str, Any] = Field(description="Properties directly requested by the user. e.g. OS, region, specific instance type.")
    inferred_properties: Dict[str, Any] = Field(description="Logical properties inferred from the context. e.g. map_public_ip_on_launch=true for a public subnet.")
    default_properties: Dict[str, Any] = Field(description="Standard default properties assigned when information is missing.")

class TerraformRequirements(BaseModel):
    provider: str = Field(description="The cloud provider, e.g., aws, azurerm, google")
    region: Optional[str] = Field(None, description="The region to deploy resources in, if specified")
    resources: List[TerraformResource] = Field(description="List of terraform resources to create")
    variables: Optional[Dict[str, str]] = Field(None, description="Variables to define")
    outputs: Optional[Dict[str, str]] = Field(None, description="Outputs to return")
