import requests
import os
import sys
import json

def post(url, directory, login_token):

    path = os.path.join("./defaults", directory)
    headline = os.getenv('HEADLINE', "================================================================================")

    print()
    print(headline)
    print("Create default " + directory + "s")
    print(headline)

    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', encoding="utf-8") as file:

            response = requests.post(url, json=json.load(file), headers={"Authorization": "Bearer " + login_token, "Content-Type" : "application/json;charset=utf-8"}, timeout=60)

            if response.status_code != 201:
                print(os.path.splitext(filename)[0] + " => ")
                print(json.dumps(json.loads(response.text), indent=4))
            else:
                print(os.path.splitext(filename)[0] + " got created")

cluster = sys.argv[3].strip()

if cluster == "development":
    cluster = "develop"

url_prefix = "https://uc4.cs.uni-paderborn.de/api/" + cluster

answer = requests.get(url_prefix + "/authentication-management/login/machine", auth=(sys.argv[1], sys.argv[2]), timeout=60)
token = answer.json()["login"]

post(url_prefix + "/user-management/users", "user", token)
post(url_prefix + "/examreg-management/examination-regulations", "examreg", token)
post(url_prefix + "/course-management/courses", "course", token)

# Generated files
post(url_prefix + "/user-management/users", os.path.join("generated", "admins"), token)
post(url_prefix + "/user-management/users", os.path.join("generated", "students"), token)
post(url_prefix + "/user-management/users", os.path.join("generated", "lecturers"), token)
post(url_prefix + "/examreg-management/examination-regulations", os.path.join("generated", "examRegs"), token)
post(url_prefix + "/course-management/courses", os.path.join("generated", "courses"), token)
