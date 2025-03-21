import pandas as pd
from utils import clean_cpf

def load_data(first_file_path, second_file_path):
    first_file_data = pd.read_excel(first_file_path, engine='xlrd')
    second_file_data = pd.read_excel(second_file_path, engine='openpyxl')
    return first_file_data, second_file_data

def get_columns(first_file_data, second_file_data):
    first_file_cpf_col = next((col for col in first_file_data.columns if 'cpf' in col.lower()), None)
    second_file_cpf_col = next((col for col in second_file_data.columns if 'cpf' in col.lower()), None)
    first_file_status_col = next((col for col in first_file_data.columns if 'status' in col.lower()), None)
    second_file_status_col = next((col for col in second_file_data.columns if 'status' in col.lower()), None)
    return first_file_cpf_col, second_file_cpf_col, first_file_status_col, second_file_status_col

def clean_data(first_file_data, second_file_data, first_file_cpf_col, second_file_cpf_col):
    first_file_data['CPF_Cleaned'] = first_file_data[first_file_cpf_col].apply(clean_cpf)
    second_file_data['CPF_Cleaned'] = second_file_data[second_file_cpf_col].apply(clean_cpf)
    return first_file_data, second_file_data

def remove_duplicates(first_file_data, second_file_data):
    first_file_data_without_duplicates = first_file_data.drop_duplicates(subset=['CPF_Cleaned'])
    second_file_data_without_duplicates = second_file_data.drop_duplicates(subset=['CPF_Cleaned'])
    return first_file_data_without_duplicates, second_file_data_without_duplicates

def compare_students(first_file_data, second_file_data):
    first_file_cpfs = set(first_file_data['CPF_Cleaned'].dropna())
    second_file_cpfs = set(second_file_data['CPF_Cleaned'].dropna())
    
    registered_students = second_file_cpfs.intersection(first_file_cpfs)
    not_registered_students = second_file_cpfs - first_file_cpfs
    first_file_extra_students = first_file_cpfs - second_file_cpfs
    
    return registered_students, not_registered_students, first_file_extra_students

def filter_status_data(first_file_data, second_file_data, first_file_status_col, second_file_status_col):
    remove_status = ['trancado', 'cancelado', 'desistente', 'formado', 'transferido', 'finalizado']
    status_pattern = '|'.join(remove_status)
    
    first_file_data = first_file_data[~first_file_data[first_file_status_col].str.lower().str.contains(status_pattern)]
    
    active_status_second_file = ['matriculado', 'rematriculado']
    active_status_pattern = '|'.join(active_status_second_file)
    
    second_file_data = second_file_data[second_file_data[second_file_status_col].str.lower().str.contains(active_status_pattern)]
    
    cancel_status_second_file = ['trancado', 'cancelado', 'transferido', 'desistente']
    cancel_status_pattern = '|'.join(cancel_status_second_file)
    
    second_file_data_invalid = second_file_data[~second_file_data[second_file_status_col].str.lower().str.contains(cancel_status_pattern)]
    
    return first_file_data, second_file_data, second_file_data_invalid