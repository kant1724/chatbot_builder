from e_database import exporter

def vocab_dec_exporter():
    fw1 = open('./a_builder/exporter/data/vocab_dec', 'w', encoding='utf8')
    result = exporter.get_vocab_dec()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")

def vocab_enc_exporter():
    fw1 = open('./a_builder/exporter/data/vocab_enc', 'w', encoding='utf8')
    result = exporter.get_vocab_enc()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")


