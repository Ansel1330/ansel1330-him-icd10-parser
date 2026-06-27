import streamlit as st
import PyPDF2
import os
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="HIM Coding Assistant",
    page_icon="🏥",
    layout="centered"
)

# 2. Display Department Logo prominently at the top
LOGO_PATH = "OIP.webp"
if os.path.exists(LOGO_PATH):
    try:
        logo_img = Image.open(LOGO_PATH)
        # Display the logo centered or left-aligned
        st.image(logo_img, width=150, caption="Health Information Management Department")
    except Exception as e:
        st.warning(f"Could not load logo image: {e}")

# 3. App Title & Subtitle
st.title("🏥 Health Information Management")
st.subheader("ICD-10 Diagnostic Lead/Subterm Parser")
st.markdown("---")

# 4. File Paths (Now safely looking relative to the current app folder)
VOL1_PATH = "ICD-10_Volume_1.pdf"
VOL3_PATH = "ICD-10_Volume_3 (2).pdf"

# 5. Search Optimized Extraction Function
def search_pdf_for_terms(pdf_path, lead_term, subterms):
    results = []
    if not os.path.exists(pdf_path):
        return f"Error: '{pdf_path}' file missing from app repository."
    
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            # Scan up to 350 pages for solid real-time web performance
            max_pages = min(len(reader.pages), 350)
            
            for page_num in range(max_pages):
                text = reader.pages[page_num].extract_text()
                if not text:
                    continue
                
                if lead_term.lower() in text.lower():
                    # Confirm all subterms are present on the page if they exist
                    match_subterms = all(sub.lower() in text.lower() for sub in subterms) if subterms else True
                    
                    if match_subterms:
                        lines = text.split('\n')
                        for line in lines:
                            if lead_term.lower() in line.lower():
                                results.append(f"**[Page {page_num + 1}]** {line.strip()}")
    except Exception as e:
        return f"An error occurred while reading the PDF: {str(e)}"
    
    if not results:
        return "No matching records found within the evaluated book range."
    return "\n\n".join(results[:20])

# 6. User Input Section
raw_input = st.text_input(
    "Enter Diagnostic Condition:",
    placeholder="e.g., Diabetes coma or Appendicitis acute"
)

if raw_input:
    # Parsing input text into Lead and Subterms
    input_tokens = raw_input.strip().split()
    lead_term = input_tokens[0]
    subterms = input_tokens[1:] if len(input_tokens) > 1 else []
    
    # Showcase Extracted Identifiers in a beautiful clean alert panel
    subterm_display = ", ".join([f"'{s}'" for s in subterms]) if subterms else "None"
    
    st.info(f"""
    **HIM Token Parser Results:**
    * 🔍 **Detected Lead Term:** `{lead_term.upper()}`
    * ⛓️ **Detected Subterm(s):** `{subterm_display.upper()}`
    """)
    
    # 7. Step-by-Step Methodology Section
    st.markdown("### 📋 Official HIM Conventional Coding Steps")
    st.markdown(f"""
    1. **Locate Lead Term:** Search the primary alphabetical term **'{lead_term.upper()}'** in Volume 3.
    2. **Follow Subterms:** Read downward tracking parenthetical modifiers and indented subterms ({subterm_display}).
    3. **Instructional Instructions:** Look out for instructions like *'see'* or *'see also'*.
    4. **Tabular Verification:** Take your target index code from Volume 3 and verify it in Volume 1 (Tabular List).
    5. **Exclusions & Inclusions:** Review Chapter and Block rules to make sure the condition isn't explicitly excluded.
    6. **Assign Code:** Finalize your code to the highest level of specificity (4th or 5th character).
    """)
    
    # 8. Run Search & Create Responsive Layout Tabs
    st.markdown("### 🔍 Extracted ICD-10 Content Matches")
    tab1, tab2 = st.tabs(["Index Search (Volume 3)", "Tabular Context (Volume 1)"])
    
    with st.spinner("Parsing manuals... Please wait."):
        vol3_output = search_pdf_for_terms(VOL3_PATH, lead_term, subterms)
        vol1_output = search_pdf_for_terms(VOL1_PATH, lead_term, subterms)
        
    with tab1:
        st.markdown("#### Volume 3 - Alphabetical Matches")
        st.write(vol3_output)
        
    with tab2:
        st.markdown("#### Volume 1 - Tabular List Confirmation")
        st.write(vol1_output)