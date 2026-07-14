import json
import random
import string
from datetime import datetime
from pathlib import Path

class Student:
  database = 'data.json'
  data = []

  try:
    if Path(database).exists():
      with open(database, 'r') as fs:
        data = json.load(fs)
    else:
      print(f"No file found as {database}.")
  
  except Exception as e:
    print("Error while loading data from file:", e)
  
  @classmethod
  def IdGenerator(cls):
    alpha = random.choices(string.ascii_uppercase, k=2)
    num = random.choices(string.digits, k=3)
    id =  num + alpha
    return "".join(id)
  
  @classmethod
  def __update(cls):
    try:
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)
    except Exception as e:
        print("Error writing data to file:", e)

  def add_student(self):
    info = {
      "roll_no" : Student.IdGenerator(),
      "name" : input("Enter student name: "),
      "age" : int(input("Enter student age: ")),
      "course" : input("Enter student course: "),
      "marks" : {},
      "percentage" : 0.0,
      "grade" : ""
    }
    if info["age"] <= 16 and info["age"] >= 25:
      print("Age should be between 16 and 25.")
      return
    else:
      print("Student added successfully.")
      for i in info:
        print(f"{i}: {info[i]}")
      print(f"Student Roll Number is {info['roll_no']}. Please note it down for future references.")
      Student.data.append(info)
      Student.__update()
  
  def search_students(self):
    id = input("Enter student roll number to view details: ")

    userData = [i for i in Student.data if i["roll_no"] == id]

    if not userData:
        print("Student not found.")
        return

    for i in userData[0]:
        print(f"{i}: {userData[0][i]}")

  def update_student(self):
    id = input("Enter student roll number to update details: ")

    userData = [i for i in Student.data if i["roll_no"] == id]

    if not userData:
        print("Student not found.")
        return

    print("What do you want to update?")
    print("Press 1: To update name.")
    print("Press 2: To update age.")
    print("Press 3: To update course.")
    print("Press 4: To update marks.")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        new_name = input("Enter new name: ")
        userData[0]["name"] = new_name
        Student.__update()
        print("Name updated successfully.")
    elif choice == 2:
        new_age = int(input("Enter new age: "))
        if new_age <= 16 or new_age >= 25:
            print("Age should be between 16 and 25.")
            return
        userData[0]["age"] = new_age
        Student.__update()
        print("Age updated successfully.")
    elif choice == 3:
        new_course = input("Enter new course: ")
        userData[0]["course"] = new_course
        Student.__update()
        print("Course updated successfully.")
    elif choice == 4:
        subject = input("Enter subject name: ")
        marks = int(input("Enter marks: "))
        userData[0]["marks"][subject] = marks
        Student.__update()
        print("Marks updated successfully.")
    else:
        print("Invalid choice.")
        return

  def delete_student(self):
    id = input("Enter student roll number to delete details: ")

    userData = [i for i in Student.data if i["roll_no"] == id]

    if not userData:
        print("Student not found.")
        return

    Student.data.remove(userData[0])
    Student.__update()
    print("Student deleted successfully.")

  def add_marks(self):
    id = input("Enter student roll number to add marks: ")

    userData = [i for i in Student.data if i["roll_no"] == id]

    if not userData:
        print("Student not found.")
        return

    subject = input("Enter subject name: ")
    marks = int(input("Enter marks: "))
    userData[0]["marks"][subject] = marks
    Student.__update()
    print("Marks added successfully.")

  def calculate_grade(self):
    id = input("Enter student roll number to calculate grade: ")

    userData = [i for i in Student.data if i["roll_no"] == id]

    if not userData:
        print("Student not found.")
        return

    total_marks = sum(userData[0]["marks"].values())
    num_subjects = len(userData[0]["marks"])
    percentage = (total_marks / (num_subjects * 100)) * 100 if num_subjects > 0 else 0
    userData[0]["percentage"] = percentage

    if percentage >= 90:
        userData[0]["grade"] = "A"
    elif percentage >= 80:
        userData[0]["grade"] = "B"
    elif percentage >= 70:
        userData[0]["grade"] = "C"
    elif percentage >= 60:
        userData[0]["grade"] = "D"
    else:
        userData[0]["grade"] = "F"

    Student.__update()
    print(f"Percentage: {percentage:.2f}%")
    print(f"Grade: {userData[0]['grade']}")

  def generate_report_card(self):
    id = input("Enter student roll number to result of student: ")

    userData = [i for i in Student.data if i["roll_no"] == id]

    if not userData:
        print("Student not found.")
        return
    
    print("\nReport Card: \n")
    print("\nStudent Details:")
    print(f"Name of Student: {userData[0]['name']}")
    print(f"Roll Number: {userData[0]['roll_no']}")
    print(f"Enrolled Course: {userData[0]['course']}")
    print("\nSubjects and Marks: ")
    for i in userData[0]['marks']:
       print(f"{i} : {userData[0]['marks'][i]}")
    print("\nResult Analysis:")
    print(f"Percentage: {userData[0]['percentage']}%")
    print(f"Grade: {userData[0]['grade']}")
    result = ""
    if userData[0]['percentage'] > 34:
       result = "PASS"
    else:
       result = "FAIL"
    print(f"Status: {result}")

  def class_stats(self):
     print("\nClass Statistics are: ")
     total_std = len(Student.data)
     print(f"Total Students in class: {total_std}")
     add = 0
     total_sub = 0
     for i in Student.data:
        for j in i['marks'].values():
           add += j
           total_sub += 1
        
     avg = add / (total_sub*100)
     print(f"Class Average marks: {avg}")
     print(f"Class Average percentage: {avg*100}%")
     highest = Student.data[0]['percentage']
     lowest = Student.data[0]['percentage']
     passed = 0
     fail = 0
     for i in Student.data:
        if i['percentage'] > highest:
           highest = i['percentage']
        
        if i['percentage'] < lowest:
           lowest = i['percentage']
        
        if i['percentage'] > 34:
           passed += 1
           
        if i['percentage'] <= 34:
           fail += 1
      
     print(f"Highest Score: {highest}%")
     print(f"Lowest Score: {lowest}%")
     print(f"Students passed: {passed}")
     print(f"Students failed: {fail}")
     pass_rate = (passed / total_std)*100
     print(f"Pass Rate: {pass_rate}%")


user = Student()

print("Press 1: To add a new student.")
print("Press 2: To search a student by ID.")
print("Press 3: To update a student by ID.")
print("Press 4: To delete a student by ID.")
print("Press 5: To add marks to a student by ID.")
print("Press 6: To calculate grade of a student by ID.")
print("Press 7: To generate a report card of a student by ID.")
print("Press 8: To view class statistics.")

check = int(input("Enter your choice: "))

if check == 1:
  user.add_student()
if check == 2:
  user.search_students()
if check == 3:
  user.update_student()
if check == 4:
  user.delete_student()
if check == 5:
  user.add_marks()
if check == 6:
  user.calculate_grade()
if check == 7:
  user.generate_report_card()
if check == 8:
   user.class_stats()