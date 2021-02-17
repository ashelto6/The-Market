#check_creds() is called in the "auth.signup ['POST']" view function
def check_creds(first_name, last_name, email, password, repassword):
 credentials = [first_name, last_name, email, password, repassword]
 x = 0
 for c in credentials: 
  if c == "":
   x = x+1
 return x
