
def read(namaFIle,typeFile,typeAction):
    """Function untuk membaca list IP device dari file"""
    with open("./ListFile/"+namaFIle+"."+typeFile, typeAction) as listFile:
        return listFile.read().split("\n")