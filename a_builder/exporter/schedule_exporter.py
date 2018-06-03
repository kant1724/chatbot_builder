from e_database import exporter

def schedule_exporter():
    fw1 = open('./a_builder/exporter/data/schedule', 'w', encoding='utf8')
    result = exporter.get_schedule()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")

