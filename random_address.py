from uuid import uuid4

def get_unique_addr():
    ''' utility to generate an un used uuid address '''
    while True:
        yield uuid4().hex

