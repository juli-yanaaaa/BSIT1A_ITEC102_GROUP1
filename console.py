import csv
import os

# =================================
#STUDENT GRADE MANAGEMENT SYSTEM
#==================================

students = []

#Grading formula:
#Quiz = 20%
#Assignment = 30%
#Examination = 50%

PASSING_GRADE = 75
QUIZ_WEIGHT = 0.2
ASSIGNMENT_WEIGHT = 0.3
EXAM_WEIGHT = 0.5

FILE_NAME = "student_records.csv"

# =================================
#CALCULATE FINAL GRADE
#==================================

def calculate_final_grade(quiz, assignment, exam):
    final_grade = (quiz * QUIZ_WEIGHT) + (assignment * ASSIGNMENT_WEIGHT) + (exam * EXAM_WEIGHT)
    return round(final_grade, 2)

# =================================
#ADD STUDENT RECORD
#==================================

def add_student():
    print("\n==== ADD STUDENT RECORD ====")

    student_number = input("Enter Student Number: ")

    #check duplicate student number
    for student in students:
        if student["student_number"] == student_number:
            print("Student number already exists!")
            return
        
    name = input("Enter Student Name: ")
    section = input("Enter Section: ")
        
    student = { 
        "student_number": student_number,
        "name": name,
        "section": section,
        "quiz": 0,
        "assignment": 0,
        "exam": 0,
        "final_grade": 0
    }

    students.append(student)

    print("Student record added successfully!")

#==================================
#RECORD STUDENT SCORES
#==================================

def record_scores():
    print("\n==== RECORD STUDENT SCORES ====")

    student_number = input("Enter Student Number: ")

    for student in students:
        if student["student_number"] == student_number:
            try:
                quiz = float(input("Enter Quiz Score (0-100): "))
                assignment = float(input("Enter Assignment Score (0-100): "))
                exam = float(input("Enter Exam Score (0-100): "))

                if not all(0 <= score <= 100 for score in [quiz, assignment, exam]):
                    print("Scores must be between 0 and 100.")
                    return

                student["quiz"] = quiz
                student["assignment"] = assignment
                student["exam"] = exam
                
                student["final_grade"] = calculate_final_grade(quiz, assignment, exam)

                print("\nScores recorded successfully!")
                print("Final Grade:", student["final_grade"])
                return
            
            except ValueError:
                print("Invalid input! Please enter numbers.")
                return
            
        print("Student not found.")
#=================================
#DISPLAY ALL STUDENTS
#==================================            
def display_students():
    print("\n==== STUDENT RECORDS ====")
    if not students:
        print("No student records available.")
        return

    print("-" * 105)
    print(f"{'Student No.':<15} {'Name':<20} {'Section':<12}" 
          f"{'Quiz':<10} {'Assignment':<13} {'Exam':<10}" 
          f"{'Grade':<10} {'Status'}")
        
    print("-" * 105)

    for student in students:

        grade = student["final_grade"]

        if grade >= PASSING_GRADE:
            status = "PASSED"
        else:
            status = "FAILED"

        print(
            f"{student['student_number']:<15} "
            f"{student['name']:<20}"
            f"{student['section']:<12}"
            f"{student['quiz']:<10.2f}"
            f"{student['assignment']:<13.2f}"
            f"{student['exam']:<10.2f}"
            f"{grade:<10.2f} "
            f"{status}"
        )

    print("-" * 105)
# =================================
#SEARCH STUDENT BY STUDENT NUMBER
#==================================

def search_student():
    print("\n==== SEARCH STUDENT ====")

    student_number = input("Enter Student Number: ")
    print("DEBUG: Student number entered:", student_number)
    print("DEBUG: Number of students", len(students))
    
    for student in students:
        if student["student_number"] == student_number:
            print("\nStudent Found!")
            print("Student Number:",  student["student_number"])
            print("Name:", student["name"])
            print("Section:", student["section"])
            print("Quiz Score:", student["quiz"])
            print("Assignment Score:", student["assignment"])
            print("Examination Score:", student["exam"])
            print("Final Grade:", student["final_grade"])

            if student["final_grade"] >= PASSING_GRADE:
                print("Status: PASSED")
            else:
                print("Status: FAILED")

            return

    print("Student not found.")

# =================================
#CLASS PERFORMANCE SUMMARY
#==================================

def class_summary():
    print("\n==== CLASS PERFORMANCE SUMMARY ====")

    if not students:
        print("No student records available.")
        return

    total_students = len(students)
    passed = 0
    failed = 0
    total_grade = 0

    for student in students:
        grade = student["final_grade"]

        total_grade += grade

        if grade >= PASSING_GRADE:
            passed += 1
        else:
            failed += 1

    average = total_grade / total_students 

    print("Total Students:", total_students)
    print("Number of  Students Passed:", passed)
    print("Number of Students Failed:", failed)
    print("Class Average:", round(average, 2))

    print("Passing Threshold:", PASSING_GRADE)

    print("\nClass Performance:")

    if average >= PASSING_GRADE:
        print("Overall Class Performance: SATISFACTORY")
    else:
        print("Overall Class Performance: NEEDS IMPROVEMENT")

# =================================
#SAVE STUDENT RECORDS TO CSV FILE
#==================================

def save_records():
    try:
        with open(FILE_NAME, "w", newline='') as file:

            fieldnames = [
                "student_number", 
                "name", 
                "section", 
                "quiz", 
                "assignment", 
                "exam", 
                "final_grade" 
            ]

            writer = csv.DictWriter(file, 
                fieldnames=fieldnames
                )
            writer.writeheader()

            writer.writerows(students)

        print("Student records saved successfully!")
    except OSError as error:
        print("Error saving records:", error)

# =================================
#LOAD STUDENT RECORDS FROM CSV FILE
#==================================

def load_records():
    global students

    if not os.path.exists(FILE_NAME):
        print("No saved student records found.")
        return

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            loaded_students = []
            for row in reader:
                loaded_students.append({
                    "student_number": row["student_number"],
                    "name": row["name"],
                    "section": row["section"],
                    "quiz": float(row["quiz"]),
                    "assignment": float(row["assignment"]),
                    "exam": float(row["exam"]),
                    "final_grade": float(row["final_grade"])
                })

            students = loaded_students
        print("Student records loaded successfully!")
    except (OSError, ValueError, KeyError) as error:
        print("Error loading records:", error)

# =================================
#MAIN MENU
#==================================

def main():
    load_records()
    while True:
        print("\n=================================")
        print("STUDENT GRADE MANAGEMENT SYSTEM")
        print("\n=================================")

        print("1. Add Student Record")
        print("2. Record Student Scores")
        print("3. Display All Students")
        print("4. Search Student by Student Number")
        print("5. Class Performance Summary")
        print("6. Save Student Records")
        print("7. Load Student Records")
        print("8. Exit")
        print("\n=================================")

        choice = input("Enter your choice (1-8): ")
        print("You entered:", choice)

        if choice == "1":
            add_student()
        elif choice == "2":
            record_scores()
        elif choice == "3":
            display_students()
        elif choice == "4":
            search_student()
        elif choice == "5":
            class_summary()
        elif choice == "6":
            save_records()
        elif choice == "7":
            load_records()
        elif choice == "8":
            save_records()
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice! Please select 1-8.")

# =================================
#RUN THE PROGRAM
#==================================

if __name__ == "__main__":
    main()