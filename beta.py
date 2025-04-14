import yaml


data  ={}
with open("beta.yaml","r")as f:
  data = yaml.safe_load(f)
  
print(data) 