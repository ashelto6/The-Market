
def ef5count(field1, field2, field3, field4, field5): #counts how many of 5 fields are empty - return int
  credentials = [field1, field2, field3, field4, field5]
  x = 0
  for c in credentials: 
    c=c.strip()
    if c == "":
      x = x+1
  return x

def ef3count(field1, field2, field3):
  credentials = [field1, field2, field3]
  x = 0
  for c in credentials:
    c=c.strip()  
    if c == "":
      x = x+1
  return x