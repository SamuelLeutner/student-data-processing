import re
import pandas as pd

def clean_cpf(cpf):
    if pd.isna(cpf):
        return cpf
    return re.sub(r'[^\d]', '', str(cpf))

def validate_required_fields(df, required_fields):
    missing_fields = {}
    records_with_issues = []
    
    column_map = {col.lower(): col for col in df.columns}
    
    field_matches = {}
    for req_field in required_fields:
        req_field_lower = req_field.lower()
        matches = [col for col in column_map.keys() if req_field_lower in col]
        if matches:
            field_matches[req_field] = column_map[matches[0]]
        else:
            missing_fields[req_field] = "Column not found"
    
    for idx, row in df.iterrows():
        issues = []
        for req_field, actual_col in field_matches.items():
            if pd.isna(row[actual_col]) or str(row[actual_col]).strip() == '':
                issues.append(req_field)
        
        if issues:
            row_copy = row.copy()
            row_copy['Missing_Fields'] = ', '.join(issues)
            row_copy['Record_Index'] = idx
            records_with_issues.append(row_copy)
    
    return pd.DataFrame(records_with_issues) if records_with_issues else None, missing_fields
