import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title='VisaReady - Document Checklist', page_icon='🛂', layout='wide')

COUNTRIES = {
    'Canada': {
        'visa':'Visitor Visa (TRV)',
        'official':'https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/visitor-visa.html',
        'core':['Valid passport / travel document','Online application / personalized document checklist','Purpose of travel / itinerary','Proof of funds / bank statements','Travel history (recommended where applicable)','Employment / study / business evidence','Invitation letter (if visiting person/business)','Biometrics, if requested'],
        'notes':'IRCC creates a personalized checklist. Local visa-office requirements may add documents.'
    },
    'United States': {
        'visa':'B-1/B-2 Visitor Visa',
        'official':'https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html',
        'core':['Passport valid for travel','DS-160 confirmation page','Visa fee receipt, if required before interview','Visa photo meeting requirements','Interview appointment confirmation','Evidence of trip purpose','Evidence of ability to pay trip costs','Evidence supporting intent to depart after visit'],
        'notes':'Embassy/consulate instructions can add location-specific requirements.'
    },
    'United Kingdom': {
        'visa':'Standard Visitor Visa',
        'official':'https://www.gov.uk/standard-visitor',
        'core':['Passport / travel document valid for the stay','Online application information','Travel dates and accommodation details','Estimated trip cost and income details','Evidence of funds and financial circumstances','Employment / study / business evidence','Travel history where applicable','Sponsor / invitation evidence where applicable'],
        'notes':'Supporting evidence depends on purpose and personal circumstances.'
    },
    'Australia': {
        'visa':'Visitor Visa (Subclass 600 - Tourist)',
        'official':'https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/visitor-600',
        'core':['Current passport identity pages','National identity card, if applicable','Proof of funds','Travel plans / itinerary','Evidence of reasons to return home','Employment / study / business evidence','Invitation and sponsor funds, if applicable','English translations of non-English documents'],
        'notes':'Health, character and minor-child documents may be requested depending on circumstances.'
    },
    'Schengen Area': {
        'visa':'Short-stay Schengen Visa (Type C)',
        'official':'https://home-affairs.ec.europa.eu/policies/schengen/visa-policy/applying-schengen-visa_en',
        'core':['Valid passport','Completed visa application form','ICAO-compliant photograph','Travel medical insurance','Flight / transport reservation','Accommodation evidence','Proof of financial means','Employment / study / business evidence and home-country ties'],
        'notes':'The competent Member State and applicant country can have additional harmonized supporting-document lists.'
    },
    'United Arab Emirates': {
        'visa':'Tourist / Visit Entry Permit',
        'official':'https://u.ae/en/information-and-services/visa-and-emirates-id/visa-information',
        'core':['Passport with required validity','Recent personal photograph','Completed sponsor/airline/agent/authority application as applicable','Confirmed travel details where required','Accommodation / host details where required','Proof of relationship for family visit where applicable','Travel/health insurance where required by visa channel','Additional sponsor or guarantor documents where applicable'],
        'notes':'Eligibility and channel vary by nationality, emirate, airline, sponsor and visa type. Verify before applying.'
    },
    'Saudi Arabia': {
        'visa':'Tourist Visa / eVisa (where eligible)',
        'official':'https://www.visitsaudi.com/en/plan-your-trip/visa-regulations/',
        'core':['Passport meeting validity requirement','Personal photograph','Completed visa/eVisa application','Eligibility evidence for the chosen visa route','Travel and accommodation details where required','Ability to support yourself during the visit','Medical insurance where required','Additional package/sponsor/embassy documents if your nationality is not on the standard eVisa route'],
        'notes':'Visa route depends strongly on nationality and other eligibility. Check the official Saudi visa tool.'
    },
}

st.title('🛂 VisaReady - Visitor Visa Document Checklist')
st.caption('Educational document-readiness tool. It does not determine visa eligibility, approval probability, or replace official government instructions.')

with st.sidebar:
    st.header('Applicant & Trip')
    nationality = st.text_input('Nationality', 'Pakistan')
    country = st.selectbox('Destination', list(COUNTRIES))
    purpose = st.selectbox('Purpose', ['Tourism','Family/Friends Visit','Business Visit','Conference/Event'])
    employment = st.selectbox('Current status', ['Employed','Self-employed / Business','Student','Retired','Unemployed / Other'])
    sponsor = st.checkbox('Trip is sponsored by another person/company')
    minor = st.checkbox('Applicant is under 18')
    travel_date = st.date_input('Planned departure', value=date.today()+timedelta(days=60), min_value=date.today())

cfg = COUNTRIES[country]
st.subheader(f'{country} — {cfg["visa"]}')
st.info(cfg['notes'])

base = list(cfg['core'])
conditional=[]
if employment == 'Employed': conditional += ['Employer letter / NOC and approved leave evidence','Recent payslips / salary evidence']
elif employment == 'Self-employed / Business': conditional += ['Business registration / ownership evidence','Business bank/tax evidence where relevant']
elif employment == 'Student': conditional += ['Enrollment / student-status letter','Approved leave / academic schedule where relevant']
elif employment == 'Retired': conditional += ['Retirement / pension evidence where relevant']
if sponsor: conditional += ['Sponsor letter explaining support','Sponsor identity/status and financial evidence']
if purpose == 'Family/Friends Visit': conditional += ['Invitation / host letter','Proof of relationship where relevant','Host immigration/status document where relevant']
elif purpose == 'Business Visit': conditional += ['Business invitation letter','Employer/business letter explaining visit','Meeting/event agenda or registration']
elif purpose == 'Conference/Event': conditional += ['Conference/event registration or invitation','Event schedule / agenda']
if minor: conditional += ['Birth certificate / proof of parentage','Parental consent / custody documents as applicable']

all_docs=[]
for x in base+conditional:
    if x not in all_docs: all_docs.append(x)

left,right=st.columns([1.5,1])
with left:
    st.markdown('### Interactive checklist')
    checked=[]
    for i,doc in enumerate(all_docs):
        if st.checkbox(doc, key=f'doc_{country}_{i}'):
            checked.append(doc)
with right:
    completed=len(checked); total=len(all_docs); pct=round(completed/total*100) if total else 0
    st.metric('Document readiness', f'{pct}%')
    st.progress(pct/100)
    st.write(f'**{completed} of {total}** checklist items marked ready.')
    days=(travel_date-date.today()).days
    st.metric('Days until planned travel', days)
    if days < 30: st.warning('Your planned travel is relatively soon. Check official processing/appointment times immediately.')
    st.link_button('Open official visa guidance', cfg['official'])

st.markdown('### Readiness summary')
missing=[d for d in all_docs if d not in checked]
if not missing:
    st.success('All items in this planning checklist are marked ready. Re-check the official personalized/consular checklist before submission.')
else:
    st.warning(f'{len(missing)} item(s) remain in this planning checklist.')
    for d in missing: st.write('•', d)

st.markdown('### Application quality checks')
quality = {
    'Identity consistency':'Names, dates, passport details and civil documents are consistent.',
    'Purpose consistency':'Purpose, itinerary, invitation and requested duration tell the same story.',
    'Financial clarity':'Funding source, account activity and trip budget are understandable and documented.',
    'Home circumstances':'Employment/study/business/family circumstances are accurately evidenced where relevant.',
    'Document quality':'Scans are clear, complete, correctly oriented and translated where required.',
}
qcols=st.columns(2)
for idx,(title,desc) in enumerate(quality.items()):
    with qcols[idx%2]: st.checkbox(f'{title}: {desc}', key=f'q_{idx}')

st.markdown('### Important')
st.write('Visa requirements change and may depend on nationality, residence, purpose, age, sponsor, travel history and the specific embassy/consulate or application channel. Always use the official destination-government checklist as the final authority.')
