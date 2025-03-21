import os
import pandas as pd
from config import get_file_paths
from utils import validate_required_fields
from data_processing import load_data, get_columns, clean_data, remove_duplicates, compare_students, filter_status_data

output_folder, first_file_path, second_file_path = get_file_paths()
os.makedirs(output_folder, exist_ok=True)

first_file_data, second_file_data = load_data(first_file_path, second_file_path)
first_file_cpf_col, second_file_cpf_col, first_file_status_col, second_file_status_col = get_columns(first_file_data, second_file_data)
first_file_data, second_file_data = clean_data(first_file_data, second_file_data, first_file_cpf_col, second_file_cpf_col)
first_file_data, second_file_data, second_file_invalid_data = filter_status_data(first_file_data, second_file_data, first_file_status_col, second_file_status_col)
first_file_data_without_duplicates, second_file_data_without_duplicates = remove_duplicates(first_file_data, second_file_data)
registered_students, not_registered_students, first_file_extra_students = compare_students(first_file_data_without_duplicates, second_file_data_without_duplicates)

print(f"Total students in first file: {len(first_file_data)}")
print(f"Total students in second file: {len(second_file_data)}\n")
print(f"Second file students registered in first file: {len(registered_students)}")
print(f"Second file students NOT registered in first file: {len(not_registered_students)}\n")

required_columns = [
    "ALUNO", "E-MAIL", "SEXO", "CPF", "ESTADO CIVIL", "RG", "EMISSOR", "RG Org. Expedidor",
    "BAIRRO", "LOGRADOURO", "NUMERO", "ESTADO", "CIDADE", "NASCIMENTO",
]

first_file_issues_df, first_file_missing_cols = validate_required_fields(first_file_data, required_columns)
second_file_issues_df, second_file_missing_cols = validate_required_fields(second_file_data, required_columns)

first_file_valid_data = first_file_data[~first_file_data['CPF_Cleaned'].isin(first_file_issues_df['CPF_Cleaned'])]
second_file_valid_data = second_file_data[~second_file_data['CPF_Cleaned'].isin(second_file_issues_df['CPF_Cleaned'])]

first_file_invalid_data = first_file_issues_df
second_file_invalid_data = second_file_issues_df

first_file_valid_data.to_excel(os.path.join(output_folder, 'first_file_valid_records.xlsx'), index=False)
second_file_valid_data.to_excel(os.path.join(output_folder, 'second_file_valid_records.xlsx'), index=False)

combined_valid_data = pd.concat([first_file_valid_data, second_file_valid_data], ignore_index=True)
combined_valid_data.to_excel(os.path.join(output_folder, 'combined_valid_records.xlsx'), index=False)

first_file_invalid_data.to_excel(os.path.join(output_folder, 'first_file_invalid_records.xlsx'), index=False)
second_file_invalid_data.to_excel(os.path.join(output_folder, 'second_file_invalid_records.xlsx'), index=False)

combined_invalid_data = pd.concat([first_file_invalid_data, second_file_invalid_data], ignore_index=True)
combined_invalid_data.to_excel(os.path.join(output_folder, 'combined_invalid_records.xlsx'), index=False)

print("\n--- Files exported ---")
print(f"Valid records for first file: 'first_file_valid_records.xlsx' ({len(first_file_valid_data)})")
print(f"Valid records for second file: 'second_file_valid_records.xlsx' ({len(second_file_valid_data)})")
print(f"Combined valid records: 'combined_valid_records.xlsx' ({len(combined_valid_data)})\n\n")
print(f"Invalid records for first file: 'first_file_invalid_records.xlsx' ({len(first_file_invalid_data)})")
print(f"Invalid records for second file: 'second_file_invalid_records.xlsx' ({len(second_file_invalid_data)})")
print(f"Combined invalid records: 'combined_invalid_records.xlsx' ({len(combined_invalid_data)})")
