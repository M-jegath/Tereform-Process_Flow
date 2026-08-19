import asyncio
from services.requirement_analyzer import analyze_requirements
from services.semantic_verifier import verify_semantics

req_text = '''Create an AWS web server infrastructure in the ap-south-1 region. Create a VPC with the CIDR block 10.0.0.0/16. Create a public subnet inside the VPC with the CIDR block 10.0.1.0/24. Create an Internet Gateway and attach it to the VPC. Create a route table with a default route 0.0.0.0/0 through the Internet Gateway and associate it with the public subnet. Create a security group named WebSecurityGroup that allows inbound HTTP traffic on port 80 and SSH traffic on port 22 from anywhere, and allows all outbound traffic. Finally, create an Ubuntu EC2 instance named WebServer using the t2.micro instance type inside the public subnet and attach the WebSecurityGroup to the EC2 instance. Assign a public IP address to the EC2 instance.'''

reqs = analyze_requirements(req_text)

tf_code = """
provider "aws" {
  region = "ap-south-1"
}
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
resource "aws_security_group" "web_security_group" {
  name = "web_security_group"
}
resource "aws_instance" "web_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  tags = {
    Name = "web_server"
  }
}
"""
is_valid, missing = verify_semantics(reqs, tf_code)
print('MISSING REQS:', missing)
