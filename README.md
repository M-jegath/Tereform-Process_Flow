# Terraform AI Generator

A Natural Language to Terraform Code Generator powered by Streamlit and AI (Groq). 

This application allows you to input requirements as raw text or upload a PDF document containing infrastructure requirements. The system intelligently extracts the core requirements, generates valid Terraform HCL code, semantically verifies that all explicit requirements were met, and validates the output syntax using the Terraform CLI.

## Prerequisites

Before running this application on a new system, ensure you have the following installed:
1. **Python 3.9+**
2. **Terraform CLI**: Must be installed and available in your system's PATH. (The application uses `terraform fmt` and `terraform validate` behind the scenes).
   - [Download Terraform](https://developer.hashicorp.com/terraform/downloads)

## Installation Steps

1. **Clone or copy the project repository** to your local machine.
   ```bash
   git clone <repository_url>
   cd terraform-ai-generator
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install the Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory (where `app.py` is located) and add your Groq API key and preferred model. 
   
   Example `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=openai/gpt-oss-120b
   ```

## Running the Application

Once the dependencies are installed and the `.env` file is configured, start the Streamlit application by running:

```bash
streamlit run app.py
```

This will automatically open the web application in your default browser at `http://localhost:8501`.

## How it Works

The pipeline executes the following stages:
1. **Text Extraction & Cleaning**: Reads raw text or extracts content from uploaded PDFs.
2. **Requirement Analysis**: An AI agent translates the unstructured text into a highly structured JSON mapping of AWS/Azure/GCP resources.
3. **Terraform Generation**: The JSON is converted into raw HCL code.
4. **Validation & Semantic Verification**: The system formats the code, validates syntax using the local Terraform CLI, and uses an AI QA Agent to semantically verify that the generated code perfectly matches the original requirements. If it misses something, it self-corrects in a loop until it passes.
