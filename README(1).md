# VisaReady - Streamlit Visa Document Checklist

VisaReady is an educational Streamlit app that creates a visitor/tourist visa document-readiness checklist for Canada, the United States, the United Kingdom, Australia, the Schengen Area, the United Arab Emirates, and Saudi Arabia.

## What the app does
- Takes applicant/trip inputs: nationality, destination, purpose, employment status, sponsorship, minor status, and travel date.
- Builds a destination-specific core checklist plus conditional documents.
- Lets the user mark documents as ready and calculates a readiness percentage.
- Adds application-quality checks for identity, purpose, finances, home circumstances, and document quality.
- Links users to the relevant official government guidance.

## What the app does NOT do
It does not predict visa approval, provide legal advice, submit applications, or replace a government/embassy checklist.

## Local run
1. Install Python 3.10+.
2. Create a virtual environment (recommended).
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.

## Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and this README.
3. Sign in to Streamlit Community Cloud.
4. Create a new app and select the repository, branch, and `app.py`.
5. Deploy.

## Maintenance
Visa requirements change. Review every destination entry against its official government website before a release. Keep the app framed as a document-readiness assistant, not an eligibility/approval engine.
