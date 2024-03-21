import pandas as pd
import random
import string
from names import get_first_name, get_last_name


# generate random ID
def random_id(length):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))


# generate random grades
def random_grade():
    grades = ['A', 'B', 'C', 'D', 'F']
    return random.choice(grades)


# Generate data for 5 students
data = {
    "First Name": [get_first_name() for _ in range(5)],
    "Last Name": [get_last_name() for _ in range(5)],
    "ID Number": [random_id(5) for _ in range(5)],
    "Email": [f"{get_first_name().lower()}.{get_last_name().lower()}@example.com" for _ in range(5)],
    "Completed Course": ["COMP 474" for _ in range(5)],
    "Grade": [random_grade() for _ in range(5)],
    "Retake Grade": [random_grade() for _ in range(5)]
}

df = pd.DataFrame(data)

excel_path = "StudentsData.xlsx"
df.to_excel(excel_path, index=False)
print(excel_path)
