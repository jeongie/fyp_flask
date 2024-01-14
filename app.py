from flask import Flask, jsonify, request
import pyodbc
import os
import re
import fitz
import pandas as pd

app = Flask(__name__)
# conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='fyp')
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=LAPTOP-24FKBFQ8\SQLEXPRESS;'
    r'DATABASE=fyp;'
    r'UID=root;'
    r'PWD=root;'
)

conn = pyodbc.connect(conn_str)
# if conn:
#     print ("Connected Successfully")
# else:
#     print ("Connection Not Established")

@app.route('/', methods=['POST','GET'])
def index():
    return "Hello"

def get_data():
    # Assuming df_new is your DataFrame containing processed data
    selected_data = request.get_json().get('data')
    document_list = request.get_json().get('filePath')
    print(selected_data)

    print(document_list)
    
    # dm_pattern = re.compile(r'\bDM\b.*?(Under OHA)', re.DOTALL)
    # dyslipidemia_pattern = re.compile(r'HbA1c:\s*(.*?)\n')
    # ihd_pattern = re.compile(r'\bIHD\b')
    
    cabg_pattern = re.compile(r'-Post CABG on (\d{1,2}/\d{1,2}/\d{4})')
    ef_pattern= re.compile(r'EF:\s*([0-9.]+)%')
    hba1c_pattern = re.compile(r'HbA1c:\s*([\d.]+)%')
    hr_pattern = re.compile(r'Resting HR:\s*([0-9]+)')
    peak_hr_pattern = re.compile(r'Peak HR:\s*([0-9]+)')
    hr_reserve_pattern= re.compile(r'HR reserve:\s*(.*?)\n')
    hr_recovery_pattern= re.compile(r'HR recovery:\s*(.*?)\n')
    hypertension_pattern= re.compile(r'Hypertension:\s*(.*?)\n')
    tc_pattern = re.compile(r'TC:\s*([0-9.]+)')
    smoking_pattern = re.compile(r'Smoking:\s*(.*?)\n')
    alcohol_pattern = re.compile(r'Alcohol:\s*(.*?)\n')
    family_ihd_pattern = re.compile(r'Family h/o IHD:\s*(.*?)\n')
    stress_pattern = re.compile(r'Stress:\s*(.*?)\n')
    pa_pattern = re.compile(r'PA:\s*(.*?)\n')
    exercise_pattern = re.compile(r'Exercise:\s*(.*?)\n')
    diet_pattern = re.compile(r'Diet:\s*(.*?)\n')
    bmi_pattern = re.compile(r'BMI:\s*(.*?)\n')
    resting_bp_pattern = r"Resting BP: (\d+/\d+)"
    peak_bp_pattern = r"Peak BP: (\d+/\d+)"
    mets_pattern = r"METS: ([0-9.]+)"
    

    df_new= pd.DataFrame()


    for document_path in document_list:
        try:
            path_with_backslashes = document_path.replace('/', '\\')
            print(path_with_backslashes)
 
            with fitz.open(document_path) as pdf_document:
                # Initialize an empty text string
                document = ""
                
                # Iterate through pages
                for page_number in range(pdf_document.page_count):
                    # Get the page
                    page = pdf_document[page_number]
                    
                    # Extract text from the page
                    document += page.get_text()
                    print(document)
        except Exception as e:
            print(f"Error processing document {document_path}: {e}")
            continue

        pid = os.path.basename(document_path)
        filename, extension = os.path.splitext(pid)
        listn = filename.split("_")

        if '_' in filename:
            pidn = f"{listn[0]}_{listn[-1]}"
        else:
            pidn = filename


        
        # Extract information using regular expressions
        # dm_match = dm_pattern.search(document)
        # dyslipidemia_match = dyslipidemia_pattern.search(document)
        # ihd_match = ihd_pattern.search(document)
        genderSearch= re.findall(r"female| male",document,re.IGNORECASE)
        cabg_match = cabg_pattern.search(document)
        ef_match = ef_pattern.search(document)
        hba1c_match = hba1c_pattern.search(document)
        hr_match= hr_pattern.search(document)
        peak_hr_match = peak_hr_pattern.search(document)
        hr_reserve_match= hr_reserve_pattern.search(document)
        hr_recovery_match= hr_recovery_pattern.search(document)
        hypertension_match = hypertension_pattern.search(document)
        tc_match = tc_pattern.search(document)
        smoking_match = smoking_pattern.search(document)
        alcohol_match = alcohol_pattern.search(document)
        family_ihd_match = family_ihd_pattern.search(document)
        stress_match = stress_pattern.search(document)
        pa_match = pa_pattern.search(document)
        exercise_match = exercise_pattern.search(document)
        diet_match = diet_pattern.search(document)
        bmi_match = bmi_pattern.search(document)
        resting_bp_match = re.search(resting_bp_pattern, document)
        peak_bp_match = re.search(peak_bp_pattern, document)
        mets_match = re.search(mets_pattern, document)

        print("File:", document_path)
        
        # if cabg_match:
        #     cabg= cabg_match.group(1)
        #     # print("Coronary Artery Bypass Grafting (CABG) Date:", cabg_match.group(1))

        # if hba1c_match:
        #     hb1ac= hba1c_match.group(1).strip()
        
        gender = ', '.join(g.capitalize() for g in genderSearch) if genderSearch else None
        cabg= cabg_match.group(1) if cabg_match else None
        ef= float(ef_match.group(1)) if ef_match else None
        hb1ac= float(hba1c_match.group(1)) if hba1c_match else None
        rest_hr= int(hr_match.group(1).strip()) if hr_match else None
        print(type(rest_hr))
        peak_hr= int(peak_hr_match.group(1).strip()) if peak_hr_match else None
        hr_reserve= hr_reserve_match.group(1) if hr_reserve_match else None
        hr_recovery= hr_recovery_match.group(1) if hr_recovery_match else None
        hyper= hypertension_match.group(1).strip() if hypertension_match else None
        cholesterol= float(tc_match.group(1)) if tc_match else None
        smoking= smoking_match.group(1).strip() if smoking_match else None
        alcohol= alcohol_match.group(1).strip() if alcohol_match else None
        diet= diet_match.group(1).strip() if diet_match else None
        bmi= float(bmi_match.group(1).strip()) if bmi_match else None
        # bmi=float(bmi)
        print(type(bmi))
        rest_bp= resting_bp_match.group(1) if resting_bp_match else None
        peak_bp= peak_bp_match.group(1) if peak_bp_match else None
        mets= float(mets_match.group(1)) if mets_match else None

        # Create a dictionary to append to the DataFrame
        data = {
        'PID': [pidn],
        'gender':[gender],
        'cabg': [cabg],
        'ef':[ef],
        'hb1ac': [hb1ac],
        'Rest HR':[rest_hr],
        'Peak HR':[peak_hr],
        'HR reserve':[hr_reserve],
        'HR recovery':[hr_recovery],
        'hypertension':[hyper],
        'cholestrol': [cholesterol],
        'smoking':[smoking],
        'alcohol':[alcohol],
        'diet':[diet],
        'bmi':[bmi],
        'Rest BP':[rest_bp],
        'Peak BP':[peak_bp],
        'METS':[mets],
        }

        # Append the dictionary to the master DataFrame
        df_new = df_new.append(pd.DataFrame(data), ignore_index=True)
    
    # Display the resulting DataFrame
        print(df_new)

#     # Filter the DataFrame based on selected data
    df_selected = df_new[selected_data + ['PID']+['gender']]

#     # Convert the filtered DataFrame to a dictionary
    data = df_selected.to_dict(orient='records')
    print(df_selected)
    return jsonify(data)


if __name__ == '__main__':
    app.run (debug=True)
    # app.run (debug=True, port=os.getenv("PORT",default=5000))
