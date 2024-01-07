from flask import Flask, jsonify, request
import mysql.connector
import os
import re
import docx2txt
import pandas as pd

app = Flask(__name__)
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='fyp')


        
@app.route('/', methods=['POST','GET'])
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
    ef_pattern= re.compile(r'EF:\s*(.*?)\n')
    hba1c_pattern = re.compile(r'HbA1c:\s*(.*?)\n')
    hr_pattern = re.compile(r'Resting HR:\s*(.*?)\n')
    peak_hr_pattern = re.compile(r'Peak HR:\s*(.*?)\n')
    hr_reserve_pattern=  re.compile(r'HR reserve:\s*(.*?)\n')
    hr_recovery_pattern=  re.compile(r'HR recovery:\s*(.*?)\n')
    hypertension_pattern= re.compile(r'Hypertension:\s*(.*?)\n')
    tc_pattern = re.compile(r'TC:\s*(.*?)\n')
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
            # Read each file using docx2txt and convert to text
            path_with_backslashes = document_path.replace('/', '\\')
            print(path_with_backslashes)
            document = docx2txt.process(document_path)
            # print(document)
        except Exception as e:
            print(f"Error processing document {document_path}: {e}")
            continue

        pid = os.path.basename(document_path)
        listn = pid.split("_")
        pidn = listn[0] if 1 < len(listn) <= 3 else None
        
        # Extract information using regular expressions
        # dm_match = dm_pattern.search(document)
        # dyslipidemia_match = dyslipidemia_pattern.search(document)
        # ihd_match = ihd_pattern.search(document)
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

        cabg= cabg_match.group(1) if cabg_match else None
        ef= ef_match.group(1) if ef_match else None
        hb1ac= hba1c_match.group(1) if hba1c_match else None
        rest_hr= hr_match.group(1).strip() if hr_match else None
        peak_hr= peak_hr_match.group(1).strip() if peak_hr_match else None
        hr_reserve= hr_reserve_match.group(1) if hr_reserve_match else None
        hr_recovery= hr_recovery_match.group(1).strip() if hr_recovery_match else None
        hyper= hypertension_match.group(1).strip() if hypertension_match else None
        cholesterol= tc_match.group(1).strip() if tc_match else None
        smoking= smoking_match.group(1).strip() if smoking_match else None
        alcohol= alcohol_match.group(1).strip() if alcohol_match else None
        bmi= bmi_match.group(1).strip() if bmi_match else None
        rest_bp= resting_bp_match.group(1) if resting_bp_match else None
        peak_bp= peak_bp_match.group(1) if peak_bp_match else None
        mets= mets_match.group(1) if mets_match else None

        # Create a dictionary to append to the DataFrame
        data = {
        'PID': [pidn],
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
    df_selected = df_new[selected_data + ['PID']]

#     # Convert the filtered DataFrame to a dictionary
    data = df_selected.to_dict(orient='records')
    print(df_selected)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)


# *** LATEST suppose to get selected data and extract accordingly
# from flask import Flask, jsonify, request
# import mysql.connector
# import os
# import re
# import docx2txt
# import pandas as pd
# from docx import Document

# app = Flask(__name__)
# conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='fyp')

# # Define regular expressions for extraction
# cabg_pattern = re.compile(r'\bCABG\b.*?(\d{1,2}/\d{1,2}/\d{2,4})', re.DOTALL)
# hba1c_pattern = re.compile(r'HbA1c:\s*(.*?)\n')
# bmi_pattern = re.compile(r'BMI:\s*(.*?)\n')


# directory_path = "C:/Users/hui_c/Downloads/report"

# # EMPTY LIST TO FILL IN ALL WORD DOCUMENTS
# document_list = []

# # # FUNCTION TO LIST ALL WORD DOCUMENT IN THE FOLDER
# for path, subdirs, files in os.walk(directory_path):
#     for name in files:
#         # For each file we find, we need to ensure it is a .docx file before adding it to our list
#         if os.path.splitext(os.path.join(path, name))[1] == ".docx":
#             if not name.startswith('~$'):
#                 document_list.append(os.path.join(path, name))

# @app.route('/', methods=['POST'])
#     # if 'data[]' in request.form:
#     #         data = request.form.getlist('data[]')
#     #         print("Selected data:", data)

# def get_data():
#     print("Hello")
#     selected_data = request.form.getlist('data[]')
#     print(selected_data)
    
#     df_new = pd.DataFrame()

#     for document_path in document_list:
#         try:
#             # Read each file using docx2txt and convert to text
#             document = docx2txt.process(document_path)
#         except Exception as e:
#             print(f"Error processing document {document_path}: {e}")
#             continue

#         cabg_match = cabg_pattern.search(document)
#         hba1c_match = hba1c_pattern.search(document)
#         bmi_match= bmi_pattern.search(document)

#         pidn = None  # You need to define pidn or extract it from the document

#         if cabg_match:
#             cabg = cabg_match.group(1)
#         else:
#             cabg = None

#         if hba1c_match:
#             hb1ac = hba1c_match.group(1).strip()
#         else:
#             hb1ac = None

#         if bmi_match:
#             bmi = bmi_match.group(1).strip()
#         else:
#             bmi = None

#         # Create a dictionary to append to the DataFrame
#         data = {'PID': [pidn], 'cabg': [cabg], 'hb1ac': [hb1ac], 'bmi':[bmi]}

#         # Append the dictionary to the master DataFrame
#         df_new = df_new.append(pd.DataFrame(data), ignore_index=True)

#     # Filter DataFrame based on selected data
#     df_filtered = df_new[selected_data]

#     # Convert filtered DataFrame to dictionary
#     result_data = df_filtered.to_dict(orient='records')
#     print(result_data)
#     return jsonify(result_data)


# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, jsonify, request
# import os
# import re
# import docx2txt
# import pandas as pd

# app = Flask(__name__)

# # Define regular expressions for extraction (You can add your patterns here)
# cabg_pattern = re.compile(r'-Post CABG on (\d{1,2}/\d{1,2}/\d{4})')
# hba1c_pattern = re.compile(r'HbA1c:\s*(.*?)\n')
# hr_pattern = re.compile(r'Resting HR:\s*(.*?)\n')
# hypertension_pattern = re.compile(r'Hypertension:\s*(.*?)\n')
# tc_pattern = re.compile(r'TC:\s*(.*?)\n')
# smoking_pattern = re.compile(r'Smoking:\s*(.*?)\n')
# alcohol_pattern = re.compile(r'Alcohol:\s*(.*?)\n')
# bmi_pattern = re.compile(r'BMI:\s*(.*?)\n')
# resting_bp_pattern = r"Resting BP: (\d+/\d+)"
# peak_bp_pattern = r"Peak BP: (\d+/\d+)"
# mets_pattern = r"METS: ([0-9.]+)"

# # Directory containing clinical report files
# directory_path = "C:/Users/hui_c/Downloads/report"

# # EMPTY LIST TO FILL IN ALL WORD DOCUMENTS
# document_list = []
# df_new = pd.DataFrame()

# # FUNCTION TO LIST ALL WORD DOCUMENT IN THE FOLDER
# for path, subdirs, files in os.walk(directory_path):
#     for name in files:
#         if os.path.splitext(os.path.join(path, name))[1] == ".docx":
#             if not name.startswith('~$'):
#                 document_list.append(os.path.join(path, name))

# for document_path in document_list:
#     try:
#         # Read each file using docx2txt and convert to text
#         document = docx2txt.process(document_path)
#     except Exception as e:
#         print(f"Error processing document {document_path}: {e}")
#         continue

#     pid = os.path.basename(document_path)
#     listn = pid.split("_")
#     pidn = listn[0] if 1 < len(listn) <= 3 else None

#     cabg_match = cabg_pattern.search(document)
#     hba1c_match = hba1c_pattern.search(document)
#     hr_match = hr_pattern.search(document)
#     hypertension_match = hypertension_pattern.search(document)
#     tc_match = tc_pattern.search(document)
#     smoking_match = smoking_pattern.search(document)
#     alcohol_match = alcohol_pattern.search(document)
#     bmi_match = bmi_pattern.search(document)
#     resting_bp_match = re.search(resting_bp_pattern, document)
#     peak_bp_match = re.search(peak_bp_pattern, document)
#     mets_match = re.search(mets_pattern, document)

#     if cabg_match:
#         cabg = cabg_match.group(1)
#     if hba1c_match:
#         hb1ac = hba1c_match.group(1).strip()
#     if hr_match:
#         rest_hr = hr_match.group(1).strip()
#     if hypertension_match:
#         hyper = hypertension_match.group(1).strip()
#     if tc_match:
#         cholesterol = tc_match.group(1).strip()
#     if smoking_match:
#         smoking = smoking_match.group(1).strip()
#     if alcohol_match:
#         alcohol = alcohol_match.group(1).strip()
#     if bmi_match:
#         bmi = bmi_match.group(1).strip()
#     rest_bp = resting_bp_match.group(1) if resting_bp_match else None
#     peak_bp = peak_bp_match.group(1) if peak_bp_match else None
#     mets = mets_match.group(1) if mets_match else None

#     data = {
#         'PID': [pidn],
#         'cabg': [cabg],
#         'hb1ac': [hb1ac],
#         'Rest HR': [rest_hr],
#         'hypertension': [hyper],
#         'cholestrol': [cholesterol],
#         'smoking': [smoking],
#         'alcohol': [alcohol],
#         'bmi': [bmi],
#         'Rest BP': [rest_bp],
#         'Peak BP': [peak_bp],
#         'METS': [mets]
#     }

#     df_new = df_new.append(pd.DataFrame(data), ignore_index=True)

# # Display the resulting DataFrame
# print(df_new)


# @app.route('/', methods=['POST'])
# def get_data():
#     # Get the selected data from the form
#     # selected_data = request.form.getlist('data[]')
#     selected_data= data['bmi','alcohol']

#     # Filter the DataFrame based on selected data
#     df_selected = df_new[selected_data]
#     # print(df_selected)

#     # Convert the filtered DataFrame to a dictionary
#     data = df_new.to_dict(orient='records')

#     return jsonify(data)


# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, jsonify
# import mysql.connector
# import docx2txt
# import os
# app= Flask(__name__)

# conn = mysql.connector.connect(user='root', password='',
#                               host='127.0.0.1',database='fyp')


# if conn:
#     print ("Connected Successfully")
# else:
#     print ("Connection Not Established")

# select_files = """SELECT id, name FROM files WHERE type='docx'"""
# cursor = conn.cursor()
# cursor.execute(select_files)
# files = cursor.fetchall()

# if(conn.is_connected()):
#     # cursor.close()
#     # conn.close()
#     print("MySQL connection is closed.")  
#     print(files)

# for file_info in files:
#     id, name = file_info
#     document_path = os.path.join(app.config['127.0.0.1:5000/storage/files/'],name )
    
#     try:
#         document = docx2txt.process(document_path)
#         print(document)
#     except Exception as e:
#         print(f"Error processing document {document_path}: {e}")
#         continue
        
