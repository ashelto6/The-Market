from tda import auth, client
import config

#create a config.py file for your authentication credentials
try:
  c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
  from selenium import webdriver
  with webdriver.Chrome(executable_path='/mnt/c/Users/ajshe/Desktop/projects/unJumble/chromedriver.exe') as driver:
      c = auth.client_from_login_flow(
          driver, config.api_key, config.redirect_uri, config.token_path)