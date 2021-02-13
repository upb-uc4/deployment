import json
import random
import os

from faker import Faker


################################################################################
# Some settings:
################################################################################

ADMIN_COUNT = 2
STUDENT_COUNT = 40
LECTURER_COUNT = 10
EXAM_REG_COUNT = 10
COURSE_COUNT = 20

ROLES = ["Student", "Admin", "Lecturer"]
FIELDS_OF_STUDY = ["Computer Science", "Chemistry", "Biology", "Physics", "Religion", "Sociology"]
MODULE_PREFICES = ["Topics of", "Introduction to", "Applied", "Theorotical", "Experimental"]
COURSE_TYPES = ["Lecture", "Project Group", "Seminar"]

fake = Faker("en-US")
fake.random.seed(4321)

################################################################################


basepath = os.path.join("defaults", "generated")
lecturer_ids = []
modules_by_field_of_study = {field: [] for field in FIELDS_OF_STUDY}  # Dict with modules mapped to their field of study (to let generated data appear less random)


def generate_user(role: str):
    assert role in ROLES

    profile = fake.simple_profile()
    while len(profile["name"].split(" ")) != 2:  # Some names where like Mr. John Smith...
        profile = fake.simple_profile()

    return {
        "governmentId": profile["username"] + fake.pystr(),
        "authUser": {
            "username": profile["username"],
            "password": profile["username"],  # more convenient than fake.password(),
            "role": role,
        },
        "user": {
            "username": profile["username"],
            "enrollmentIdSecret": "",
            "isActive": True,
            "role": role,
            "address": {
                "street": fake.street_name(),
                "houseNumber": fake.building_number(),
                "zipCode": fake.postcode(),
                "city": fake.city(),
                "country": fake.country(),
            },
            "firstName": profile["name"].split(" ")[0],
            "lastName": profile["name"].split(" ")[1],
            "email": profile["mail"],
            "phoneNumber": fake.phone_number(),
            "birthDate": profile["birthdate"].strftime("%m-%d-%Y"),
        },
    }


def generate_student():
    student = generate_user("Student")
    student["latestImmatriculation"] = ""
    student["matriculationId"] = str(fake.pyint(1000000, 9999999))
    return student


def generate_lecturer(all_lecturer_ids: list):
    lecturer = generate_user("Lecturer")
    lecturer["freeText"] = fake.paragraph()
    lecturer["researchArea"] = fake.job()
    all_lecturer_ids.append(lecturer["user"]["username"])
    return lecturer


def generate_admin():
    return generate_user("Admin")


def generate_exam_reg(all_modules: list):
    field_of_study = random.choice(FIELDS_OF_STUDY)
    my_modules = []
    count = random.randint(2, 5)  # Random number of modules for this exam reg
    for _ in range(count):
        # Choose existing or generate new module for this exam reg
        if random.random() < 0.8 or not my_modules:
            new_module = {
                "id": "M." + str(fake.pyint(0, 9999)).zfill(4) + "." + str(fake.pyint(0, 99999)).zfill(5),
                "name": random.choice(MODULE_PREFICES) + " " + field_of_study,
            }
            all_modules[field_of_study].append(new_module)
            my_modules.append(new_module)
        elif field_of_study in modules_by_field_of_study and modules_by_field_of_study[field_of_study]:
            module_cand = random.choice(modules_by_field_of_study[field_of_study])
            if module_cand and module_cand not in my_modules:
                my_modules.append(module_cand)
    return {
        "name": random.choice(["Bachelor", "Master"]) + " " + field_of_study + " v" + str(fake.pyint(1, 8)),
        "active": True,
        "modules": my_modules,
    }


def generate_course():
    lecturer = random.choice(lecturer_ids)
    flatten = lambda list_to_flatten: [item for sub_list in list_to_flatten for item in sub_list]
    all_module_ids = set(map(lambda module: module.get("id"), flatten(modules_by_field_of_study.values())))
    module_ids = random.sample(all_module_ids, random.randint(1, 4))

    return {
        "courseId": "",
        "moduleId": module_ids,
        "courseName": fake.catch_phrase(),
        "courseType": random.choice(COURSE_TYPES),
        "startDate": "2020-12-08",
        "endDate": "2020-12-08",
        "ects": random.randint(3, 10),
        "lecturerId": lecturer,
        "maxParticipants": 10 * random.randint(1, 20),
        "currentParticipants": 0,
        "courseLanguage": random.choice(["German", "English"]),
        "courseDescription": fake.paragraph(2),
    }


def write_to_file(data, _dir, filename):
    directory = os.path.join(os.path.dirname(__file__), basepath, _dir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, filename), "w+") as f:
        f.write(data)

def json_dump_dict(data: dict):
    return json.dumps(data, indent=4)

for i in range(ADMIN_COUNT):
    write_to_file(json_dump_dict(generate_student()), "admins", str(i).zfill(2) + ".json")

for i in range(STUDENT_COUNT):
    write_to_file(json_dump_dict(generate_student()), "students", str(i).zfill(2) + ".json")

for i in range(LECTURER_COUNT):
    write_to_file(json_dump_dict(generate_lecturer(lecturer_ids)), "lecturers", str(i).zfill(2) + ".json")

for i in range(EXAM_REG_COUNT):
    write_to_file(json_dump_dict(generate_exam_reg(modules_by_field_of_study)), "examRegs", str(i).zfill(2) + ".json")

for i in range(COURSE_COUNT):
    write_to_file(json_dump_dict(generate_course()), "courses", str(i).zfill(2) + ".json")

print("Done! 😎")
print("Generated: {} Admins, {} Students, {} Lecturers, {} Exam Regs and {} Courses".format(ADMIN_COUNT, STUDENT_COUNT, LECTURER_COUNT, EXAM_REG_COUNT, COURSE_COUNT))
