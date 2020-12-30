from faker import Faker
import json
import random
import os

fake = Faker('en-US')
fake.random.seed(4321)  

roles = ["Student", "Admin", "Lecturer"]
lecturer_ids = []

fields_of_study = ["Computer Science", 'Chemistry', "Biology", "Physics", 'Religion', "Sociology"]
modules = {field: [] for field in fields_of_study}
module_prefices = ["Topics of", 'Introduction to', "Applied", "Theorotical", "Experimental"]
course_types = ["Lecture", "Project Group", "Seminar"]


def getFakeUser(role):
    assert role in roles

    profile = fake.simple_profile()
    while len(profile["name"].split(" ")) != 2:  # Some names where like Mr. John Smith...
        profile = fake.simple_profile()

    return {
        'governmentId': profile['username'] + fake.pystr(),
        'authUser': {
            'username': profile['username'],
            'password': fake.password(),
            'role': role,
        },
        'user': {
            'username': profile['username'],
            'enrollmentIdSecret': '',
            'isActive': True,
            'role': role,
            'address': {
                'street': fake.street_name(),
                'houseNumber': fake.building_number(),
                'zipCode': fake.postcode(),
                'city': fake.city(),
                'country': fake.country(),
            },
            'firstName': profile['name'].split(" ")[0],
            'lastName': profile['name'].split(" ")[1],
            'email': profile['mail'],
            'phoneNumber': fake.phone_number(),
            'birthDate': profile['birthdate'].strftime('%m-%d-%Y'),
        }
    }

def getFakeStudent():
    student = getFakeUser("Student")
    student['latestImmatriculation'] = ''
    student['matriculationId'] = str(fake.pyint(1000000, 9999999))
    return student

def getFakeLecturer():
    global lecturer_ids
    lecturer = getFakeUser("Lecturer")
    lecturer['freeText'] = fake.paragraph()
    lecturer['researchArea'] = fake.job()
    lecturer_ids.append(lecturer['user']['username'])
    return lecturer 

def getFakeAdmin():
    return getFakeUser("Admin")
    

def getFakeExamReg():
    global modules

    field_of_study = random.choice(fields_of_study)
    my_modules = []
    count = random.randint(2, 5)
    for _ in range(count):
        if random.random() < 0.8 or not my_modules:
            new_module = {
                    'id': 'M.' + str(fake.pyint(0,9999)).zfill(4) + "." + str(fake.pyint(0,99999)).zfill(5),
                    'name': random.choice(module_prefices) + ' ' + field_of_study,
                }
            modules[field_of_study].append(new_module)
            my_modules.append(new_module)
        elif field_of_study in modules and modules[field_of_study]:
            module_cand = random.choice(modules[field_of_study])
            if module_cand and module_cand not in my_modules:
                my_modules.append(module_cand)
    return {
        'name': random.choice(["Bachelor", 'Master']) + " " + field_of_study + ' v' + str(fake.pyint(1, 8)),
        'active': True,
        'modules': my_modules,
    }

def getFakeCourse():
    lecturer = random.choice(lecturer_ids)
    all_module_ids = list(map(lambda course_modules: list(map(lambda m: m.get("id"), course_modules)), modules.values()))
    all_module_ids = [module for module_list in all_module_ids for module in module_list ]
    moduleIds = random.sample(all_module_ids, random.randint(1,4))

    return {
        "courseId": "",
        "moduleId": moduleIds,
        "courseName": fake.catch_phrase(),
        "courseType": random.choice(course_types),
        "startDate": "2020-12-08",
        "endDate": "2020-12-08",
        "ects": random.randint(3,10),
        "lecturerId": lecturer,
        "maxParticipants": 10 * random.randint(1,20),
        "currentParticipants": 0,
        "courseLanguage": random.choice(["German", "English", "Spanish", "Chinese"]),
        "courseDescription": fake.paragraph(1),
    }

basepath = os.path.join("defaults", "generated")
def writeToFile(data, _dir, filename):
    directory = os.path.join(os.path.dirname(__file__), basepath, _dir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, filename), "w+") as f:
        f.write(data)

for i in range(20):
    writeToFile(json.dumps(getFakeStudent()), "students", str(i).zfill(2) + ".json")

for i in range(5):
    writeToFile(json.dumps(getFakeLecturer()), "lecturers", str(i).zfill(2) + ".json")

for i in range(8):
    writeToFile(json.dumps(getFakeExamReg()), "examRegs", str(i).zfill(2) + ".json")

for i in range(20):
    writeToFile(json.dumps(getFakeCourse()), "courses", str(i).zfill(2) + ".json")