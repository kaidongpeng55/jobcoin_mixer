import uuid

def get_unique_addr():
    ''' utility to generate an un used uuid address '''
    while True:
        yield uuid.uuid4().hex

