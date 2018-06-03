from e_database import importer

def voca_importer():
    fw1 = open('./a_builder/importer/data/voca', 'r', encoding='utf8')
    lines = fw1.readlines()
    for line in lines:
        line = line.replace('\n', '')
        arr = line.split("^")
        for i in range(len(arr)):
            if arr[i] == 'None':
                arr[i] = 'null'
        importer.import_voca(arr)
