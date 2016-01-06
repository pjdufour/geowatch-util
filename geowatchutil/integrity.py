import hashlib


def calc_md5sum(data, block_size=128**4):
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


def calc_md5sum_file(filename, block_size=128**4):
    md5 = hashlib.md5()
    with open(filename, "r") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()
