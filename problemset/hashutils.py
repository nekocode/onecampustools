import hashlib
__author__ = 'nekocode'


def md5(content):
    import hashlib
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()

