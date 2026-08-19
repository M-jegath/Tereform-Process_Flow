from services.requirement_analyzer import analyze_requirements
from services.semantic_verifier import verify_semantics

req_text = 'Create an AWS EC2 instance in the us-east-1 region using the t2.micro instance type. Use Ubuntu as the operating system and name the instance WebServer.'
reqs = analyze_requirements(req_text)
print('REQUIREMENTS:', reqs.model_dump())

tf_code = """
provider "aws" {
  region = "us-east-1"
}
resource "aws_instance" "web_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  tags = {
    Name = "WebServer"
  }
}
"""

print('TF CODE:', tf_code)

is_valid, missing = verify_semantics(reqs, tf_code)
print('SEMANTIC VALID:', is_valid)
print('MISSING:', missing)
