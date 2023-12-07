import streamlit as st
import streamlit.components.v1 as components
from prediction import application_scorecard
import pandas as pd
import requests

req1 = requests.Request()

df = pd.read_csv("merge_data_imputed.csv")
print(df['occupation_type'].unique())

st.set_page_config(page_title=df['occupation_type'][0], layout="wide", page_icon="")
st.header("IRB Application Scorecard")
st.write(
    "Machine Learning Model for creating Application scorecard using Internal Ratings Based(IRB) methodology for deriving Master Credit Rating for the customer, this model output will help in decision making for following business outcomes.	Approve/Reject a loan.	Select optimal interest rate for the loan depending on customer credit Rating.")

output2 = ""
check_prediction = 0

with st.sidebar:
    from PIL import Image

    image = Image.open('refract.png')
    st.image(image)
    st.sidebar.header("Select your input Parameters")

    amt_credit_Input = st.slider('amt_credit', float(df['amt_credit'].min()), float(df['amt_credit'].max()),
                                 float(df['amt_credit'].mean()))
    amt_goods_price_Input = st.slider('amt_goods_price', float(df['amt_goods_price'].min()),
                                      float(df['amt_goods_price'].max()), float(df['amt_goods_price'].mean()))
    credit_agency_1_rating_Input = st.slider('credit_agency_1_rating', float(df['credit_agency_1_rating'].min()),
                                             float(df['credit_agency_1_rating'].max()),
                                             float(df['credit_agency_1_rating'].mean()))
    credit_agency_2_rating_Input = st.slider('credit_agency_2_rating', float(df['credit_agency_2_rating'].min()),
                                             float(df['credit_agency_2_rating'].max()),
                                             float(df['credit_agency_2_rating'].mean()))
    credit_agency_3_rating_Input = st.slider('credit_agency_3_rating', float(df['credit_agency_3_rating'].min()),
                                             float(df['credit_agency_3_rating'].max()),
                                             float(df['credit_agency_3_rating'].mean()))

    days_credit_Input = st.slider('days_credit', float(df['days_credit'].min()), float(df['days_credit'].max()),
                                  float(df['days_credit'].mean()))
    days_credit_enddate_Input = st.slider('days_credit_enddate', float(df['days_credit_enddate'].min()),
                                          float(df['days_credit_enddate'].max()),
                                          float(df['days_credit_enddate'].mean()))
    remaining_installment_Input = st.slider('remaining_installment', float(df['remaining_installment'].min()),
                                            float(df['remaining_installment'].max()),
                                            float(df['remaining_installment'].mean()))
    buro_avg_amt_instalment_Input = st.slider('buro_avg_amt_instalment', float(df['buro_avg_amt_instalment'].min()),
                                              float(df['buro_avg_amt_instalment'].max()),
                                              float(df['buro_avg_amt_instalment'].mean()))
    buro_max_amt_instalment_Input = st.slider('buro_max_amt_instalment', float(df['buro_max_amt_instalment'].min()),
                                              float(df['buro_max_amt_instalment'].max()),
                                              float(df['buro_max_amt_instalment'].mean()))

    occupation_type_Input = st.selectbox(
        'please select the Occupation type',
        df['occupation_type'].unique())

    organization_type_Input = st.selectbox(
        'please select the organization type',
        df['organization_type'].unique())

    code_gender_Input = st.selectbox(
        'please select the Gender',
        df['code_gender'].unique())

    days_birth_Input = st.slider('Days since Birth', float(df['days_birth'].min()),
                                              float(df['days_birth'].max()),
                                              float(df['days_birth'].mean()))
    days_id_publish_Input = st.slider('days_id_publish', float(df['days_id_publish'].min()),
                                      float(df['days_id_publish'].max()), float(df['days_id_publish'].mean()))
    customer_since_Input = st.slider('customer_since', float(df['customer_since'].min()),
                                     float(df['customer_since'].max()), float(df['customer_since'].mean()))
    annual_income_Input = st.slider('annual_income', float(df['annual_income'].min()), float(df['annual_income'].max()),
                                    float(df['annual_income'].mean()))
    days_employed_Input = st.slider('days_employed', float(df['days_employed'].min()), float(df['days_employed'].max()),
                                    float(df['days_employed'].mean()))

    name_contract_type_Input = st.selectbox(
        'please select the contract type',
        df['name_contract_type'].unique())

    # ====================================================

    if st.button('Predict'):
        check_prediction = 1
        inp1 = {"amt_credit": amt_credit_Input,
                "amt_goods_price": amt_goods_price_Input,
                "credit_agency_1_rating": credit_agency_1_rating_Input,
                "credit_agency_2_rating": credit_agency_2_rating_Input,
                "credit_agency_3_rating": credit_agency_3_rating_Input,
                "days_credit": days_credit_Input,
                "days_credit_enddate": days_credit_enddate_Input,
                "remaining_installment": remaining_installment_Input,
                "buro_avg_amt_instalment": buro_avg_amt_instalment_Input,
                "buro_max_amt_instalment": buro_max_amt_instalment_Input,
                "occupation_type": occupation_type_Input,
                "organization_type": organization_type_Input,
                "code_gender": code_gender_Input,
                "days_birth": days_birth_Input,
                "days_id_publish": days_id_publish_Input,
                "customer_since": customer_since_Input,
                "annual_income": annual_income_Input,
                "days_employed": days_employed_Input,
                "name_contract_type": name_contract_type_Input
                }
    #  req1.json = {
    #      "payload": inp1.to_json()
    #   }

    else:
        st.write('Please submit once you are ready!')

tab1, tab2 = st.tabs(["Data Profile", "Prediction"])
with tab1:
    HtmlFile = open("data_profile.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=600, scrolling=True)

with tab2:
    if check_prediction > 0:
        st.subheader("Application Scorecard Input data")
        data_1 = inp1
        st.table(data_1)
        inp2={"payload":inp1}
        output1 = application_scorecard(inp2)
        st.text_input('Application Scorecard Output', output1)
        st.write("#")
        st.write("#")

    else:
        st.write("Submit to check the model prediction")