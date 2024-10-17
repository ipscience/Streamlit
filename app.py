import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv('特実_国内文献.csv')

# Streamlit app setup
st.set_page_config(page_title="特許庁データ分析", layout="wide")
st.title("🛍️ 特許庁データ分析")

# Sidebar Filters
st.sidebar.header("Filter Patents")
selected_stage = st.sidebar.multiselect(
    "Select Patent Stage:",
    options=data['ステージ'].unique(),
    default=data['ステージ'].unique()
)
selected_applicant = st.sidebar.multiselect(
    "Select Applicant(s):",
    options=data['出願人/権利者'].unique(),
    default=data['出願人/権利者'].unique()
)

# Filter Data
filtered_data = data[
    (data['ステージ'].isin(selected_stage)) &
    (data['出願人/権利者'].isin(selected_applicant))
]

# Visualization 1: Top Applicants
top_applicants = filtered_data['出願人/権利者'].value_counts().head(10).reset_index()
top_applicants.columns = ['Applicant', 'Count']
fig_applicant = px.bar(
    top_applicants, x='Applicant', y='Count',
    title="📈 Top 10 Applicants",
    labels={'Applicant': 'Applicant', 'Count': 'Number of Patents'},
    template="plotly_white"
)
st.plotly_chart(fig_applicant, use_container_width=True)

# Visualization 2: Patents by Stage
patent_stage_count = filtered_data['ステージ'].value_counts().reset_index()
patent_stage_count.columns = ['Stage', 'Count']
fig_stage = px.bar(
    patent_stage_count, x='Stage', y='Count',
    title="💡 Patents by Stage",
    labels={'Stage': 'Patent Stage', 'Count': 'Number of Patents'},
    template="plotly_white"
)
st.plotly_chart(fig_stage, use_container_width=True)  # Ensure the correct variable is used.

# Visualization 3: Publication Year Analysis
filtered_data['公知日'] = pd.to_datetime(filtered_data['公知日'], errors='coerce')
filtered_data['Publication Year'] = filtered_data['公知日'].dt.year
yearly_publications = filtered_data['Publication Year'].value_counts().reset_index()
yearly_publications.columns = ['Year', 'Count']
fig_year = px.line(
    yearly_publications.sort_values('Year'), x='Year', y='Count',
    title="📏 Publications Over the Years",
    labels={'Year': 'Year', 'Count': 'Number of Publications'},
    template="plotly_white"
)
st.plotly_chart(fig_year, use_container_width=True)

# Function to determine the identifier (15 for patents and utility models, 11 for publications)
def get_identifier(patent_number):
    if patent_number.startswith('特許') or patent_number.startswith('実登'):
        return '15'  # Patent or Utility Model identifier
    elif patent_number.startswith('特開') or patent_number.startswith('特表'):
        return '11'  # Publication identifier
    else:
        return 'unknown'

# Function to exclude the first two characters from doc_number and create links
def modify_doc_number(doc_number):
    # Exclude the first two characters
    modified_doc_number = doc_number[2:]
    return modified_doc_number

# Display links to patents with the modified document number
st.write("### Patent Links (Modified Doc Number)")
for _, row in filtered_data.iterrows():
    # Extract patent number from the 文献番号 column
    doc_number = row['文献番号']
    identifier = get_identifier(doc_number)

    # Modify the document number by removing the first two characters
    modified_doc_number = modify_doc_number(doc_number)

    # Construct the URL with the modified document number
    doc_url = f"https://www.j-platpat.inpit.go.jp/c1801/PU/JP-{modified_doc_number}/{identifier}/ja"
    
    # Display the link with the modified 文献番号 and 発明の名称
    st.markdown(f"[{row['文献番号']} - {row['発明の名称']}]({doc_url})")
