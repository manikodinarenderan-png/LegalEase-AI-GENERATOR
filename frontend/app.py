import html
import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv

from document_utils.docx_formatter import (
    format_docx
)

from document_utils.pdf_formatter import (
    format_pdf
)

from document_utils.text_formatter import (
    sanitize_text
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


LOGO_PATH = os.path.join(
    PROJECT_ROOT,
    "assets",
    "logo.svg"
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .hero {
        text-align: center;
        padding: 20px 0 20px 0;
    }

    .hero h1 {
        font-size: 48px;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #777;
        font-size: 18px;
    }

    .preview {
        background: #171717;
        color: #f4f4f4;
        padding: 25px;
        border-radius: 12px;
        max-height: 650px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.7;
    }

    .notice {
        padding: 14px;
        border-left: 4px solid #777;
        background: #f5f5f5;
        border-radius: 6px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">

        <h1>⚖️ LegalEase</h1>

        <div class="subtitle">
            AI-Powered Legal Document Generator
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="notice">

    LegalEase creates draft legal documents
    for informational use.

    Review important documents with a qualified
    legal professional before signing or relying
    on them.

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "document" not in st.session_state:

    st.session_state.document = ""


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

left, right = st.columns(2)


with left:

    document_type = st.text_input(
        "Document Type",
        placeholder=(
            "Example: Freelance Work Contract"
        )
    )

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=130
    )


with right:

    effective_date = st.text_input(
        "Effective Date",
        value=date.today().isoformat()
    )

    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=130
    )


# --------------------------------------------------
# GENERATE
# --------------------------------------------------

generate = st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
)


if generate:

    if not document_type.strip():

        st.error(
            "Please enter the document type."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms."
        )

    elif not effective_date.strip():

        st.error(
            "Please enter the effective date."
        )

    else:

        payload = {

            "document_type":
                document_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                terms.strip(),

            "effective_date":
                effective_date.strip()
        }

        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                st.session_state.document = (
                    result["content"]
                )

                st.success(
                    "Document generated successfully!"
                )

            except requests.RequestException as error:

                st.error(
                    "Could not connect to the "
                    "FastAPI backend."
                )

                st.code(str(error))


# --------------------------------------------------
# DOCUMENT EDITOR
# --------------------------------------------------

if st.session_state.document:

    st.divider()

    st.subheader(
        "📝 Edit Document"
    )

    edited_document = st.text_area(
        "Generated Document",
        value=st.session_state.document,
        height=600
    )

    st.session_state.document = (
        edited_document
    )


    # --------------------------------------------------
    # PREVIEW
    # --------------------------------------------------

    st.subheader(
        "👁️ Document Preview"
    )

    safe_document = html.escape(
        edited_document
    )

    safe_document = safe_document.replace(
        "\n",
        "<br>"
    )

    st.markdown(
        f"""
        <div class="preview">
            {safe_document}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # EXPORT
    # --------------------------------------------------

    st.divider()

    st.subheader(
        "📥 Download Document"
    )


    txt_data = sanitize_text(
        edited_document
    ).encode("utf-8")


    docx_data = format_docx(
        text=edited_document,
        doc_type=document_type or "Legal Document",
        terms=terms,
        logo_path=LOGO_PATH
    )


    pdf_data = format_pdf(
        text=edited_document,
        doc_type=document_type or "Legal Document",
        terms=terms
    )


    download1, download2, download3 = st.columns(3)


    with download1:

        st.download_button(
            label="⬇️ Download TXT",
            data=txt_data,
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True
        )


    with download2:

        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_data,
            file_name="legalease_document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )


    with download3:

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_data,
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True
        )