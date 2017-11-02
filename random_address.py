import uuid

# utility to generate an un used uuid address
def get_unique_addr():
    while True:
        yield uuid.uuid4().hex
