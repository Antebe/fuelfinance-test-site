import uuid
import datetime
import string
# Printing random id using uuid1()
def create_id():
    result = int((str(datetime.datetime.now()).translate(str.maketrans('', '', string.punctuation))).replace(" ", ""))
    return result

print(create_id())