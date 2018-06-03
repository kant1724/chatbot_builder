from e_database import synonym as db_synonym

def get_synonym_nm_list_by_voca_nm(voca_nm):
    synonym_list = db_synonym.search_synonym_nm_list_by_synonym_nm(voca_nm)
    if len(synonym_list) > 0:
        synonym = '' 
        for i in range(len(synonym_list)):
            synonym += synonym_list[i]['synonym_nm']
            if i < len(synonym_list) - 1:
                synonym += "^"
    else:
        synonym = voca_nm
    
    return synonym
