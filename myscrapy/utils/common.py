import hashlib 

def get_md5(i):
    md5=hashlib.md5()
    md5.update(i.encode('utf-8'))
    return md5.hexdigest()