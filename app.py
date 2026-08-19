import streamlit as st
import os

# Page config
st.set_page_config(
    page_title="AI Terraform Code Generator",
    page_icon="🏗️",
    layout="wide"
)

def main():
    st.title("AI TERRAFORM CODE GENERATOR")
    st.markdown("Convert infrastructure requirements into Terraform configuration automatically.")
    st.divider()
    
    from config.settings import GROQ_API_KEY, GROQ_MODEL
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        st.error("⚠️ GROQ_API_KEY is missing or invalid. Please configure it in your `.env` file.")
        st.stop()

    st.subheader("Input Method")
    
    input_method = st.radio(
        "Choose how to provide requirements:",
        ("Text Input", "PDF Upload"),
        horizontal=True
    )

    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    if input_method == "Text Input":
        input_text = st.text_area(
            "Enter your Terraform requirements...",
            height=200,
            value=st.session_state.input_text,
            placeholder="e.g. Create an AWS EC2 instance using Ubuntu. Use t2.micro and deploy it in us-east-1."
        )
        if input_text:
            st.session_state.input_text = input_text
    else:
        from services.pdf_processor import extract_text_from_pdf
        uploaded_file = st.file_uploader("Upload a PDF containing Terraform requirements", type="pdf")
        if uploaded_file is not None:
            try:
                extracted_text = extract_text_from_pdf(uploaded_file)
                st.session_state.input_text = extracted_text
                st.success("PDF extracted successfully!")
                st.text_area("Extracted Text Preview", value=extracted_text, height=150, disabled=True)
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        
    st.markdown("---")
    
    if st.button("Generate Terraform", type="primary"):
        if not st.session_state.input_text.strip():
            st.warning("Please provide requirements via text or PDF first.")
        else:
            from services.text_processor import clean_text, is_terraform_relevant
            
            from services.requirement_analyzer import analyze_requirements
            
            st.info("Processing requirements...")
            
            with st.spinner("Step 1: Cleaning text and checking relevance..."):
                # Step 1: Clean Text
                cleaned_text = clean_text(st.session_state.input_text)
                st.session_state.cleaned_text = cleaned_text
                
                # Step 2: Relevance Check
                if not is_terraform_relevant(cleaned_text):
                    st.error("⚠️ The provided input does not appear to contain Terraform infrastructure requirements.")
                    st.stop()
                    
                st.success("Input is valid.")
            
            with st.spinner("Step 2: Analyzing Requirements via AI..."):
                try:
                    requirements = analyze_requirements(cleaned_text)
                    st.session_state.requirements = requirements
                    st.success("Requirements analyzed successfully!")
                    st.json(requirements.model_dump())
                except Exception as e:
                    st.error(f"Error during requirement analysis: {e}")
                    st.stop()
            
            with st.spinner("Step 3: Generating Terraform Code..."):
                from services.terraform_generator import generate_terraform
                try:
                    terraform_code = generate_terraform(st.session_state.requirements)
                    st.session_state.terraform_code = terraform_code
                    st.success("Terraform code generated successfully!")
                    st.code(terraform_code, language="hcl")
                except Exception as e:
                    st.error(f"Error during Terraform generation: {e}")
                    st.stop()
                    
            # Formatting and validation logic
            with st.spinner("Step 4: Formatting and Syntactic/Semantic Validation..."):
                from services.terraform_formatter import format_terraform
                from services.terraform_validator import validate_terraform
                from services.terraform_generator import correct_terraform
                from services.semantic_verifier import verify_semantics, correct_semantics
                
                max_retries = 3
                current_code = st.session_state.terraform_code
                is_valid = False
                error_msg = None
                
                for attempt in range(max_retries + 1):
                    # Format
                    formatted_code = format_terraform(current_code)
                    st.session_state.terraform_code = formatted_code
                    
                    # 1. Syntactic Validation
                    syn_valid, syn_error_msg = validate_terraform()
                    
                    if not syn_valid:
                        if attempt < max_retries:
                            st.warning(f"Syntax validation failed on attempt {attempt + 1}. Attempting auto-correction...")
                            current_code = correct_terraform(st.session_state.requirements, formatted_code, syn_error_msg)
                            continue
                        else:
                            error_msg = f"Syntax Validation failed after {max_retries + 1} attempts.\nError:\n{syn_error_msg}"
                            break
                            
                    # 2. Semantic Verification
                    st.info(f"Syntax valid (Attempt {attempt + 1}). Running Semantic Verification...")
                    sem_valid, missing_reqs = verify_semantics(st.session_state.requirements, formatted_code)
                    
                    if not sem_valid:
                        if attempt < max_retries:
                            st.warning(f"Semantic verification failed on attempt {attempt + 1}. Attempting auto-correction...\nMissing: {missing_reqs}")
                            req_json_str = requirements.model_dump_json(indent=2)
                            current_code = correct_semantics(formatted_code, missing_reqs, req_json_str)
                            continue
                        else:
                            error_msg = f"Semantic Verification failed after {max_retries + 1} attempts.\nMissing requirements: {missing_reqs}"
                            break
                            
                    # If both pass
                    is_valid = True
                    st.success(f"Syntax and Semantic Validation successful! (Attempt {attempt + 1})")
                    break
                            
                st.session_state.is_valid = is_valid
                st.session_state.validation_error = error_msg if not is_valid else None
                
            # Final Output Display
            st.markdown("---")
            st.subheader("Final Terraform Configuration")
            if st.session_state.get("is_valid"):
                st.success("Terraform configuration is valid ✓")
            else:
                st.error("Terraform configuration is invalid ✗")
                
            st.code(st.session_state.terraform_code, language="hcl")
            
            # Download button
            st.download_button(
                label="Download main.tf",
                data=st.session_state.terraform_code,
                file_name="main.tf",
                mime="text/plain"
            )





if __name__ == "__main__":
    main()
