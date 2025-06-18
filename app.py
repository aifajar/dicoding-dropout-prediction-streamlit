import datetime
import numpy as np
import pandas as pd
import streamlit as st
import joblib

marital_status_mapping = {
    'Single': 1,
    'Married': 2,
    'Widower': 3,
    'Divorced': 4,
    'Facto Union': 5,
    'Legally Seperated': 6
}

application_mode_mapping = {
    '1st Phase - General Contingent': 1,
    '1st Phase - Special Contingent (Azores Island)': 5,
    '1st Phase - Special Contingent (Madeira Island)': 16,
    '2nd Phase - General Contingent': 17,
    '3rd Phase - General Contingent': 18,
    'Ordinance No. 612/93': 2,
    'Ordinance No. 854-B/99': 10,
    'Ordinance No. 533-A/99, Item B2 (Different Plan)': 26,
    'Ordinance No. 533-A/99, Item B3 (Other Institution)': 27,
    'International Student (Bachelor)': 15,
    'Over 23 Years Old': 39,
    'Transfer': 42,
    'Change of Course': 43,
    'Holders of Other Higher Courses': 7,
    'Short Cycle Diploma Holders': 53,
    'Technological Specialization Diploma Holders': 44,
    'Change of Institution/Course': 51,
    'Change of Institution/Course (International)': 57,
}

application_order_mapping = {
    'First Choice': 0,
    'Second Choice': 1,
    'Third Choice': 2,
    'Fourth Choice': 3,
    'Fifth Choice': 4,
    'Sixth Choice': 5,
    'Seventh Choice': 6,
    'Eighth Choice': 7,
    'Last Choice': 8
}

course_mapping = {
    'Biofuel Production Technologies': 33,
    'Animation and Multimedia Design': 171,
    'Social Service (evening attendance)': 8014,
    'Agronomy': 9003,
    'Communication Design': 9070,
    'Veterinary Nursing': 9085,
    'Informatics Engineering': 9119,
    'Equinculture': 9130,
    'Management': 9147,
    'Social Service': 9328,
    'Tourism': 9254,
    'Nursing': 9500,
    'Oral Hygiene': 9556,
    'Advertising and Marketing Management': 9670,
    'Journalism and Communication': 9773,
    'Basic Education': 9853,
    'Management (evening attendance)': 9991
}

daytime_evening_attendance_mapping = {
    'Evening': 0,
    'Daytime': 1
}

previous_qualification_mapping = {
    'Secondary Education': 1,
    'Higher Education - Bachelor Degree': 2,
    'Higher Education - Degree': 3,
    'Higher Education - Master': 4,
    'Higher Education - Doctorate': 5,
    'Frequency of Higher Education': 6,
    '12th Year of Schooling - Not Completed': 9,
    '11th Year of Schooling - Not Completed': 10,
    'Other - 11th Year of Schooling': 12,
    '10th Year of Schooling': 14,
    '10th Year of Schooling - Not Completed': 15,
    'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.': 19,
    'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.': 38,
    'Technological Specialization Course': 39,
    'Higher Education - Degree (1st Cycle)': 40,
    'Professional Higher Technical Course': 42,
    'Higher Education - Master (2nd Cycle)': 43
}

nacionality_mapping = {
    'Portuguese': 1,
    'German': 2,
    'Spanish': 6,
    'Italian': 11,
    'Dutch': 13,
    'English': 14,
    'Lithuanian': 17,
    'Angolan': 21,
    'Cape Verdean': 22,
    'Guinean': 24,
    'Mozambican': 25,
    'Santomean': 26,
    'Turkish': 32,
    'Brazilian': 41,
    'Romanian': 62,
    'Moldova (Republic of)': 100,
    'Mexican': 101,
    'Ukrainian': 103,
    'Russian': 105,
    'Cuban': 108,
    'Colombian': 109
}

mothers_qualification_mapping = {
    'Secondary Education - 12th Year of Schooling or Eq.': 1,
    'Higher Education - Bachelor Degree': 2,
    'Higher Education - Degree': 3,
    'Higher Education - Master': 4,
    'Higher Education - Doctorate': 5,
    'Frequency of Higher Education': 6,
    '12th Year of Schooling - Not Completed': 9,
    '11th Year of Schooling - Not Completed': 10,
    '7th Year (Old)': 11,
    'Other - 11th Year of Schooling': 12,
    '10th Year of Schooling': 14,
    'General Commerce Course': 18,
    'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.': 19,
    'Technical-Professional Course': 22,
    '7th Year of Schooling': 26,
    '2nd Cycle of the General High School Course': 27,
    '9th Year of Schooling - Not Completed': 29,
    '8th Year of Schooling': 30,
    'Unknown': 34,
    'Cannot Read or Write': 35,
    'Can Read Without Having a 4th Year of Schooling': 36,
    'Basic Education 1st Cycle (4th/5th Year) or Equiv.': 37,
    'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.': 38,
    'Technological Specialization Course': 39,
    'Higher Education - Degree (1st Cycle)': 40,
    'Specialized Higher Studies Course': 41,
    'Professional Higher Technical Course': 42,
    'Higher Education - Master (2nd Cycle)': 43,
    'Higher Education - Doctorate (3rd Cycle)': 44
}

fathers_qualification_mapping = {
    'Secondary Education - 12th Year of Schooling or Eq.': 1,
    'Higher Education - Bachelor Degree': 2,
    'Higher Education - Degree': 3,
    'Higher Education - Master': 4,
    'Higher Education - Doctorate': 5,
    'Frequency of Higher Education': 6,
    '12th Year of Schooling - Not Completed': 9,
    '11th Year of Schooling - Not Completed': 10,
    '7th Year (Old)': 11,
    'Other - 11th Year of Schooling': 12,
    '2nd Year Complementary High School Course': 13,
    '10th Year of Schooling': 14,
    'General Commerce Course': 18,
    'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.': 19,
    'Complementary High School Course': 20,
    'Technical-Professional Course': 22,
    'Complementary High School Course - Not Concluded': 25,
    '7th Year of Schooling': 26,
    '2nd Cycle of the General High School Course': 27,
    '9th Year of Schooling - Not Completed': 29,
    '8th Year of Schooling': 30,
    'General Course of Administration and Commerce': 31,
    'Supplementary Accounting and Administration': 33,
    'Unknown': 34,
    'Cannot Read or Write': 35,
    'Can Read Without Having a 4th Year of Schooling': 36,
    'Basic Education 1st Cycle (4th/5th Year) or Equiv.': 37,
    'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.': 38,
    'Technological Specialization Course': 39,
    'Higher Education - Degree (1st Cycle)': 40,
    'Specialized Higher Studies Course': 41,
    'Professional Higher Technical Course': 42,
    'Higher Education - Master (2nd Cycle)': 43,
    'Higher Education - Doctorate (3rd Cycle)': 44
}

mothers_occupation_mapping = {
    'Student': 0,
    'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers': 1,
    'Specialists in Intellectual and Scientific Activities': 2,
    'Intermediate Level Technicians and Professions': 3,
    'Administrative Staff': 4,
    'Personal Services, Security and Safety Workers and Sellers': 5,
    'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry': 6,
    'Skilled Workers in Industry, Construction and Craftsmen': 7,
    'Installation and Machine Operators and Assembly Workers': 8,
    'Unskilled Workers': 9,
    'Armed Forces Professions': 10,
    'Other Situation': 90,
    ' ': 99,
    'Health Professionals': 122,
    'Teachers': 123,
    'Specialists in Information and Communication Technologies (ICT)': 125,
    'Intermediate Level Science and Engineering Technicians and Professions': 131,
    'Technicians and Professionals, of Intermediate Level of Health': 132,
    'Intermediate Level Technicians from Legal, Social, Sports, Cultural and Similar Services': 134,
    'Office Workers, Secretaries in General and Data Processing Operators': 141,
    'Data, Accounting, Statistical, Financial Services and Registry-related Operators': 143,
    'Other Administrative Support Staff': 144,
    'Personal Service Workers': 151,
    'Sellers': 152,
    'Personal Care Workers and the Like': 153,
    'Skilled Construction Workers and the Like, Except Electricians': 171,
    'Skilled Workers in Printing, Precision Instrument Manufacturing, Jewelers, Artisans and the Like': 173,
    'Workers in Food Processing, Woodworking, Clothing and Other Industries and Crafts': 175,
    'Cleaning Workers': 191,
    'Unskilled Workers in Agriculture, Animal Production, Fisheries and Forestry': 192,
    'Unskilled Workers in Extractive Industry, Construction, Manufacturing and Transport': 193,
    'Meal Preparation Assistants': 194
}

fathers_occupation_mapping = {
    'Student': 0,
    'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers': 1,
    'Specialists in Intellectual and Scientific Activities': 2,
    'Intermediate Level Technicians and Professions': 3,
    'Administrative Staff': 4,
    'Personal Services, Security and Safety Workers and Sellers': 5,
    'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry': 6,
    'Skilled Workers in Industry, Construction and Craftsmen': 7,
    'Installation and Machine Operators and Assembly Workers': 8,
    'Unskilled Workers': 9,
    'Armed Forces Professions': 10,
    'Other Situation': 90,
    ' ': 99,
    'Armed Forces Officers': 101,
    'Armed Forces Sergeants': 102,
    'Other Armed Forces Personnel': 103,
    'Directors of Administrative and Commercial Services': 112,
    'Hotel, Catering, Trade and Other Services Directors': 114,
    'Specialists in the Physical Sciences, Mathematics, Engineering and Related Techniques': 121,
    'Health Professionals': 122,
    'Teachers': 123,
    'Specialists in Finance, Accounting, Administrative Organization, Public and Commercial Relations': 124,
    'Intermediate Level Science and Engineering Technicians and Professions': 131,
    'Technicians and Professionals, of Intermediate Level of Health': 132,
    'Intermediate Level Technicians from Legal, Social, Sports, Cultural and Similar Services': 134,
    'Information and Communication Technology Technicians': 135,
    'Office Workers, Secretaries in General and Data Processing Operators': 141,
    'Data, Accounting, Statistical, Financial Services and Registry-related Operators': 143,
    'Other Administrative Support Staff': 144,
    'Personal Service Workers': 151,
    'Sellers': 152,
    'Personal Care Workers and the Like': 153,
    'Protection and Security Services Personnel': 154,
    'Market-oriented Farmers and Skilled Agricultural and Animal Production Workers': 161,
    'Farmers, Livestock Keepers, Fishermen, Hunters and Gatherers, Subsistence': 163,
    'Skilled Construction Workers and the Like, Except Electricians': 171,
    'Skilled Workers in Metallurgy, Metalworking and Similar': 172,
    'Skilled Workers in Electricity and Electronics': 174,
    'Workers in Food Processing, Woodworking, Clothing and Other Industries and Crafts': 175,
    'Fixed Plant and Machine Operators': 181,
    'Assembly Workers': 182,
    'Vehicle Drivers and Mobile Equipment Operators': 183,
    'Unskilled Workers in Agriculture, Animal Production, Fisheries and Forestry': 192,
    'Unskilled Workers in Extractive Industry, Construction, Manufacturing and Transport': 193,
    'Meal Preparation Assistants': 194,
    'Street Vendors (Except Food) and Street Service Providers': 195
}

displaced_mapping = {
    'No': 0,
    'Yes': 1
}

educational_special_needs_mapping = {
    'No': 0,
    'Yes': 1
}

debtor_mapping = {
    'No': 0,
    'Yes': 1
}

tuition_fees_up_to_date_mapping = {
    'No': 0,
    'Yes': 1
}

gender_mapping = {
    'Male': 1,
    'Female': 0
}

scholarship_holder_mapping = {
    'No': 0,
    'Yes': 1
}

international_mapping = {
    'No': 0,
    'Yes': 1
}

df = pd.read_csv('data/data.csv', delimiter=';')

numeric_cols = ['Previous_qualification_grade', 'Admission_grade', 'Age_at_enrollment',
    'Curricular_units_1st_sem_credited', 'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_evaluations', 'Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_grade', 'Curricular_units_1st_sem_without_evaluations',
    'Curricular_units_2nd_sem_credited', 'Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_evaluations', 'Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade', 'Curricular_units_2nd_sem_without_evaluations',
    'Unemployment_rate', 'Inflation_rate', 'GDP']

bounds = {}
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    bounds[col] = (lower, upper)

numeric_indexes = [
    6,  # previous_qualification_grade
    12, # admission_grade
    19, # age
    21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31, 32,
    33, 34, 35  # unemployment_rate, inflation_rate, gdp
]

def load_model():
    return joblib.load('final_model.joblib')

def load_scaler():
    return joblib.load('scaler.joblib')

model = load_model()
scaler = load_scaler()

def main():
    st.title('Jaya Jaya Institute Students Prediction (Graduated / Dropout)')

    marital_status = st.selectbox('Marital Status:', options=list(marital_status_mapping.keys()))

    application_mode = st.selectbox('Application Mode:', options=list(application_mode_mapping.keys()))

    application_order = st.selectbox('Application Order:', options=list(application_order_mapping.keys()))

    course = st.selectbox('Course:', options=list(course_mapping.keys()))

    daytime_evening_attendance = st.radio('Daytime/Evening Attendance:', options=list(daytime_evening_attendance_mapping.keys()))

    previous_qualification = st.selectbox('Previous Qualification:', options=list(previous_qualification_mapping.keys()))

    previous_qualification_grade = st.number_input('Previous Qualification Grade:', min_value=0.0, max_value=200.0)

    nacionality = st.selectbox('Nacionality:', options=list(nacionality_mapping.keys()))

    mothers_qualification = st.selectbox('Mothers Qualification:', options=list(mothers_qualification_mapping.keys()))

    fathers_qualification = st.selectbox('Fathers Qualification:', options=list(fathers_qualification_mapping.keys()))

    mothers_occupation = st.selectbox('Mothers Occupation:', options=list(mothers_occupation_mapping.keys()))

    fathers_occupation = st.selectbox('Fathers Occupation:', options=list(fathers_occupation_mapping.keys()))

    admission_grade = st.number_input('Admission Grade:', min_value=0.0, max_value=200.0)

    displaced = st.radio('Displaced?', options=list(displaced_mapping.keys()))

    educational_special_needs = st.radio('Educational Special Needs?', options=list(educational_special_needs_mapping.keys()))

    debtor = st.radio('Debtor?', options=list(debtor_mapping.keys()))

    tuition_fees_up_to_date = st.radio('Tuition Fees Up to Date?', options=list(tuition_fees_up_to_date_mapping.keys()))

    gender = st.radio('Gender:', options=list(gender_mapping.keys()))

    scholarship_holder = st.radio('Scholarship Holder?', options=list(scholarship_holder_mapping.keys()))

    age = st.number_input('Age at Enrollment:', min_value=15, max_value=70, 
                help='The age of the student at the time of enrollment.')

    international = st.radio('International?', options=list(international_mapping.keys()))

    curricular_units_1st_sem_credited = st.number_input('Curricular Units 1st Sem. (Credited):', min_value=0, max_value=50)

    curricular_units_1st_sem_enrolled = st.number_input('Curricular Units 1st Sem. (Enrolled):', min_value=0, max_value=50)

    curricular_units_1st_sem_evaluations = st.number_input('Curricular Units 1st Sem. (Evaluations):', min_value=0, max_value=50)

    curricular_units_1st_sem_approved = st.number_input('Curricular Units 1st Sem. (Approved):', min_value=0, max_value=50)

    curricular_units_1st_sem_grade = st.number_input('Curricular Units 1st Sem. Grade:', min_value=0.0, max_value=50.0)

    curricular_units_1st_sem_without_evaluations = st.number_input('Curricular Units 1st Sem. Without Evaluation:', min_value=0, max_value=50)

    curricular_units_2nd_sem_credited = st.number_input('Curricular Units 2nd Sem. (Credited):', min_value=0, max_value=50)

    curricular_units_2nd_sem_enrolled = st.number_input('Curricular Units 2nd Sem. (Enrolled):', min_value=0, max_value=50)

    curricular_units_2nd_sem_evaluations = st.number_input('Curricular Units 2nd Sem. (Evaluations):', min_value=0, max_value=50)

    curricular_units_2nd_sem_approved = st.number_input('Curricular Units 2nd Sem. (Approved):', min_value=0, max_value=50)

    curricular_units_2nd_sem_grade = st.number_input('Curricular Units 2nd Sem. Grade:', min_value=0.0, max_value=50.0)

    curricular_units_2nd_sem_without_evaluations = st.number_input('Curricular Units 2nd Sem. Without Evaluation:', min_value=0, max_value=50)

    unemployment_rate = st.number_input('Unemployment Rate:', min_value=0.0, max_value=100.0)

    inflation_rate = st.number_input('Inflation Rate:', min_value=-1000.0, max_value=1000.0)

    gdp = st.number_input('GDP:', min_value=-1000.0, max_value=1000.0)

    col1, col2 = st.columns([1, 1])

    with col1:

        if st.button('Predict Retention Status'):

            input_data = np.array([
                marital_status_mapping[marital_status],
                application_mode_mapping[application_mode],
                application_order_mapping[application_order],
                course_mapping[course],
                daytime_evening_attendance_mapping[daytime_evening_attendance],
                previous_qualification_mapping[previous_qualification],
                previous_qualification_grade,
                nacionality_mapping[nacionality],
                mothers_qualification_mapping[mothers_qualification],
                fathers_qualification_mapping[fathers_qualification],
                mothers_occupation_mapping[mothers_occupation],
                fathers_occupation_mapping[fathers_occupation],
                admission_grade,
                displaced_mapping[displaced],
                educational_special_needs_mapping[educational_special_needs],
                debtor_mapping[debtor],
                tuition_fees_up_to_date_mapping[tuition_fees_up_to_date],
                gender_mapping[gender],
                scholarship_holder_mapping[scholarship_holder],
                age,
                international_mapping[international],
                curricular_units_1st_sem_credited,
                curricular_units_1st_sem_enrolled,
                curricular_units_1st_sem_evaluations,
                curricular_units_1st_sem_approved,
                curricular_units_1st_sem_grade,
                curricular_units_1st_sem_without_evaluations,
                curricular_units_2nd_sem_credited,
                curricular_units_2nd_sem_enrolled,
                curricular_units_2nd_sem_evaluations,
                curricular_units_2nd_sem_approved,
                curricular_units_2nd_sem_grade,
                curricular_units_2nd_sem_without_evaluations,
                unemployment_rate,
                inflation_rate,
                gdp
            ]).reshape(1, -1)

            numeric_values = input_data[0, numeric_indexes]

            for i, col in enumerate(numeric_cols):
                lower, upper = bounds[col]
                numeric_values[i] = np.clip(numeric_values[i], lower, upper)

            input_data[0, numeric_indexes] = numeric_values

            input_data_scaled = scaler.transform(input_data)

            #st.success(input_data_scaled)

            prediction = model.predict(input_data_scaled)[0]

            if prediction == 1:
                st.warning(f"Predicted Student Status: Dropout")
            else:
                st.success(f"Predicted Student Status: Graduated")

    with col2:
        if st.button('Reset Form'):
            st.rerun()

    year = datetime.date.today().year
    name = "[Ahmad Ibnu Fajar](http://linkedin.com/in/aifajar 'Ahmad Ibnu Fajar | LinkedIn')"
    copyright = 'Copyright © ' + str(year) + ' ' + name
    st.caption(copyright)

if __name__ == '__main__':
    main()