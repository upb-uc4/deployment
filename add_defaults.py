import requests
import os
import sys

def post(url, directory, login_token):

    path = os.path.join("./defaults", directory)

    print()
    print("================================================================================")
    print("Create default " + directory + "s")
    print("================================================================================")

    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as file:
            
            response = requests.post(url, data=file.read(), headers = {"Authorization": "Bearer " + login_token, "Content-Type" : "application/json"})

            if response.status_code != 201 :
                print(filename.removesuffix(".json") + " => " + response.text)
            else:
                print(filename.removesuffix(".json") + " got created")



answer = requests.get("https://uc4.cs.uni-paderborn.de/api/experimental/authentication-management/login/machine", auth=(sys.argv[1], sys.argv[2]))
token = answer.json()["login"]

post("https://uc4.cs.uni-paderborn.de/api/experimental/user-management/users", "user", token)
post("https://uc4.cs.uni-paderborn.de/api/experimental/examreg-management/examination-regulations", "examreg", token)
post("https://uc4.cs.uni-paderborn.de/api/experimental/course-management/courses", "course", token)