from e_database import exporter

def synonym_list_exporter():
    fw1 = open('./a_builder/exporter/data/synonym_list', 'w', encoding='utf8')
    result = exporter.get_synonym_list()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")

def category_list_exporter():
    fw1 = open('./a_builder/exporter/data/category_list', 'w', encoding='utf8')
    result = exporter.get_category_list()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")

def voca_exporter():
    fw1 = open('./a_builder/exporter/data/voca', 'w', encoding='utf8')
    result = exporter.get_voca()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")
     
def tag_list():
    fw1 = open('./a_builder/exporter/data/tag_list', 'w', encoding='utf8')
    result = exporter.get_tag_list()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")
