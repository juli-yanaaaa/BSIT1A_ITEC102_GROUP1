
import csv
import os

students = []

FILENAME = "student_records.csv"

QUIZ_WEIGHT = 0.20
ASSIGNMENT_WEIGHT = 0.30
EXAM_WEIGHT = 0.50
PASSING_GRADE = 75


# ==============================
# STUDENT NUMBER VALIDATION
# ==============================

def get_student_number():
    while True:
        student_number = input("Enter Student Number (8 digits): ").strip()

        if not student_number.isascii() or not student_number.isdigit():
            print("ERROR: Student number must contain numbers only.")
        elif len(student_number) != 8:
            print("ERROR: Student number must contain exactly 8 digits.")
        else:
            return student_number


# ==============================
# GENERAL INPUT VALIDATION
# ==============================

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()

        if value == "":
            print("ERROR: This field cannot be empty.")
        else:
            return value


def get_score(prompt):
    while True:
        try:
            score = float(input(prompt))

            if 0 <= score <= 100:
                return score
            else:
                print("ERROR: Score must be between 0 and 100.")

        except ValueError:
            print("ERROR: Please enter a valid number.")


# ==============================
# FIND STUDENT
# ==============================

def find_student(student_number):
    for student in students:
        if student["student_number"] == student_number:
            return student

    return None


# ==============================
# CALCULATE FINAL GRADE
# ==============================

def calculate_final_grade(quiz, assignment, exam):
    return (
        quiz * QUIZ_WEIGHT
        + assignment * ASSIGNMENT_WEIGHT
        + exam * EXAM_WEIGHT
    )


# ==============================
# ADD STUDENT
# ==============================

def add_student():
    print("\n===== ADD STUDENT =====")
    print("DEBUG: add_student() was called.")

    student_number = get_student_number()

    if find_student(student_number):
        print("ERROR: Student number already exists.")
        return

    name = get_non_empty_input("Enter Student Name: ")
    section = get_non_empty_input("Enter Section: ")

    student = {
        "student_number": student_number,
        "name": name,
        "section": section,
        "quiz": None,
        "assignment": None,
        "exam": None,
        "final_grade": None
    }

    students.append(student)

    print("SUCCESS: Student added successfully.")
    print("DEBUG: Total students:", len(students))


# ==============================
# RECORD OR UPDATE SCORES
# ==============================

def record_scores():
    print("\n===== RECORD STUDENT SCORES =====")
    print("DEBUG: record_scores() was called.")

    student_number = get_student_number()
    student = find_student(student_number)

    if student is None:
        print("ERROR: Student not found.")
        return

    print("\nStudent:", student["name"])
    print("Section:", student["section"])

    quiz = get_score("Enter Quiz Score: ")
    assignment = get_score("Enter Assignment Score: ")
    exam = get_score("Enter Exam Score: ")

    final_grade = calculate_final_grade(
        quiz, assignment, exam
    )

    student["quiz"] = quiz
    student["assignment"] = assignment
    student["exam"] = exam
    student["final_grade"] = final_grade

    print("\nSUCCESS: Scores recorded successfully.")
    print(f"Final Grade: {final_grade:.2f}")

    if final_grade >= PASSING_GRADE:
        print("Status: PASSED")
    else:
        print("Status: FAILED")


# ==============================
# DISPLAY ALL STUDENTS
# ==============================

def display_students():
    print("\n===== STUDENT RECORDS =====")
    print("DEBUG: display_students() was called.")
    print("DEBUG: Number of records:", len(students))

    if len(students) == 0:
        print("WARNING: No student records found.")
        return

    for student in students:
        print("\n------------------------------")
        print("Student Number:", student["student_number"])
        print("Name:", student["name"])
        print("Section:", student["section"])

        if student["final_grade"] is None:
            print("Quiz: Not yet recorded")
            print("Assignment: Not yet recorded")
            print("Exam: Not yet recorded")
            print("Final Grade: PENDING")
            print("Status: PENDING")
        else:
            print("Quiz:", student["quiz"])
            print("Assignment:", student["assignment"])
            print("Exam:", student["exam"])
            print(f"Final Grade: {student['final_grade']:.2f}")

            if student["final_grade"] >= PASSING_GRADE:
                print("Status: PASSED")
            else:
                print("Status: FAILED")

    print("\nDEBUG: Finished displaying student records.")


# ==============================
# SEARCH STUDENT
# ==============================

def search_student():
    print("\n===== SEARCH STUDENT =====")
    print("DEBUG: search_student() was called.")

    student_number = get_student_number()
    student = find_student(student_number)

    if student is None:
        print("ERROR: No student found with that student number.")
        return

    print("\nSUCCESS: Student found!")
    print("Student Number:", student["student_number"])
    print("Name:", student["name"])
    print("Section:", student["section"])

    if student["final_grade"] is None:
        print("Final Grade: PENDING")
    else:
        print(f"Final Grade: {student['final_grade']:.2f}")


# ==============================
# EDIT STUDENT INFORMATION
# ==============================

def edit_student():
    print("\n===== EDIT STUDENT INFORMATION =====")
    print("DEBUG: edit_student() was called.")

    student_number = get_student_number()
    student = find_student(student_number)

    if student is None:
        print("ERROR: Student not found.")
        return

    print("\nCurrent Name:", student["name"])
    print("Current Section:", student["section"])

    new_name = get_non_empty_input("Enter New Name: ")
    new_section = get_non_empty_input("Enter New Section: ")

    student["name"] = new_name
    student["section"] = new_section

    print("SUCCESS: Student information updated.")


# ==============================
# DELETE STUDENT
# ==============================

def delete_student():
    print("\n===== DELETE STUDENT =====")
    print("DEBUG: delete_student() was called.")

    student_number = get_student_number()
    student = find_student(student_number)

    if student is None:
        print("ERROR: Student not found.")
        return

    print("\nStudent:", student["name"])
    confirmation = input("Are you sure you want to delete this student? (Y/N): ").strip().upper()

    if confirmation == "Y":
        students.remove(student)
        print("SUCCESS: Student record deleted.")
    elif confirmation == "N":
        print("WARNING: Deletion cancelled.")
    else:
        print("ERROR: Invalid confirmation. Deletion cancelled.")


# ==============================
# CLASS SUMMARY
# ==============================

def class_summary():
    print("\n===== CLASS SUMMARY =====")
    print("DEBUG: class_summary() was called.")

    if len(students) == 0:
        print("WARNING: No student records available.")
        return

    graded_students = [
        student for student in students
        if student["final_grade"] is not None
    ]

    pending_count = len(students) - len(graded_students)

    print("Total Students:", len(students))
    print("Students with Recorded Scores:", len(graded_students))
    print("Pending Students:", pending_count)

    if len(graded_students) == 0:
        print("WARNING: No grades available for summary.")
        return

    grades = [
        student["final_grade"]
        for student in graded_students
    ]

    average = sum(grades) / len(grades)
    highest = max(grades)
    lowest = min(grades)

    passing = sum(
        1 for grade in grades
        if grade >= PASSING_GRADE
    )

    failing = len(grades) - passing

    passing_percentage = (passing / len(grades)) * 100
    failing_percentage = (failing / len(grades)) * 100

    print(f"\nClass Average: {average:.2f}")
    print(f"Highest Grade: {highest:.2f}")
    print(f"Lowest Grade: {lowest:.2f}")
    print("Passed:", passing)
    print("Failed:", failing)
    print(f"Passing Percentage: {passing_percentage:.2f}%")
    print(f"Failing Percentage: {failing_percentage:.2f}%")


# ==============================
# SORT STUDENTS
# ==============================

def sort_students():
    print("\n===== SORT STUDENTS =====")
    print("DEBUG: sort_students() was called.")

    if len(students) == 0:
        print("WARNING: No student records to sort.")
        return

    graded_students = [
        student for student in students
        if student["final_grade"] is not None
    ]

    pending_students = [
        student for student in students
        if student["final_grade"] is None
    ]

    graded_students.sort(
        key=lambda student: student["final_grade"],
        reverse=True
    )

    students[:] = graded_students + pending_students

    print("SUCCESS: Students sorted by final grade.")
    print("DEBUG: Pending students are placed at the bottom.")

    display_students()


# ==============================
# SAVE RECORDS TO CSV
# ==============================

def save_records():
    print("\n===== SAVE RECORDS =====")
    print("DEBUG: save_records() was called.")

    file_path = os.path.abspath(FILENAME)

    try:
        fieldnames = [
            "student_number",
            "name",
            "section",
            "quiz",
            "assignment",
            "exam",
            "final_grade"
        ]

        with open(FILENAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(students)

        print("SUCCESS: Records saved successfully.")
        print("Total records saved:", len(students))
        print("CSV File Location:", file_path)

    except PermissionError:
        print("ERROR: Cannot save the CSV file.")
        print("Please close the CSV file if it is open in Excel.")

    except OSError as error:
        print("ERROR: An error occurred while saving.")
        print("Details:", error)


# ==============================
# LOAD RECORDS FROM CSV
# ==============================

def load_records():
    print("\n===== LOAD RECORDS =====")
    print("DEBUG: load_records() was called.")

    file_path = os.path.abspath(FILENAME)

    print("DEBUG: Checking CSV file...")
    print("CSV File Location:", file_path)

    if not os.path.exists(FILENAME):
        print("WARNING: CSV file does not exist yet.")
        print("A new CSV file will be created when you save records.")
        return

    loaded_students = []
    seen_numbers = set()

    try:
        with open(FILENAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "student_number",
                "name",
                "section",
                "quiz",
                "assignment",
                "exam",
                "final_grade"
            }

            if reader.fieldnames is None:
                print("ERROR: CSV file is empty or has no header.")
                return

            if not required_columns.issubset(set(reader.fieldnames)):
                print("ERROR: CSV file is missing required columns.")
                print("Found columns:", reader.fieldnames)
                print("Expected columns:", sorted(required_columns))
                return

            for row_number, row in enumerate(reader, start=2):
                try:
                    student_number = row["student_number"].strip()
                    name = row["name"].strip()
                    section = row["section"].strip()

                    if (
                        not student_number.isascii()
                        or not student_number.isdigit()
                        or len(student_number) != 8
                    ):
                        raise ValueError("Invalid student number.")

                    if not name or not section:
                        raise ValueError("Name or section is empty.")

                    if student_number in seen_numbers:
                        raise ValueError("Duplicate student number.")

                    quiz_text = row["quiz"].strip()
                    assignment_text = row["assignment"].strip()
                    exam_text = row["exam"].strip()
                    grade_text = row["final_grade"].strip()

                    # All scores and grade must be blank for a pending student.
                    if not quiz_text and not assignment_text and not exam_text and not grade_text:
                        quiz = None
                        assignment = None
                        exam = None
                        final_grade = None

                    else:
                        if not quiz_text or not assignment_text or not exam_text:
                            raise ValueError("One or more scores are missing.")

                        quiz = float(quiz_text)
                        assignment = float(assignment_text)
                        exam = float(exam_text)

                        for score in [quiz, assignment, exam]:
                            if not 0 <= score <= 100:
                                raise ValueError("A score is outside 0 to 100.")

                        final_grade = calculate_final_grade(
                            quiz, assignment, exam
                        )

                        if grade_text:
                            saved_grade = float(grade_text)

                            if abs(saved_grade - final_grade) > 0.01:
                                print(
                                    f"WARNING: Row {row_number} final grade "
                                    "does not match the calculated grade. "
                                    "The calculated grade will be used."
                                )

                    student = {
                        "student_number": student_number,
                        "name": name,
                        "section": section,
                        "quiz": quiz,
                        "assignment": assignment,
                        "exam": exam,
                        "final_grade": final_grade
                    }

                    loaded_students.append(student)
                    seen_numbers.add(student_number)

                except (ValueError, TypeError) as error:
                    print(f"ERROR: Could not load CSV row {row_number}.")
                    print("Details:", error)

        students.clear()
        students.extend(loaded_students)

        print("\nSUCCESS: CSV loading completed.")
        print("Total records loaded:", len(students))
        print("CSV File Location:", file_path)

        if len(students) == 0:
            print("WARNING: The CSV file contains no valid student records.")

    except PermissionError:
        print("ERROR: Cannot access the CSV file.")
        print("Please close the file if it is open in another program.")

    except (OSError, csv.Error) as error:
        print("ERROR: An error occurred while loading the CSV file.")
        print("Details:", error)


# ==============================
# MAIN MENU
# ==============================

def main():
    print("DEBUG: Program started.")
    print("DEBUG: Loading saved records...")

    load_records()

    while True:
        print("\n================================")
        print("     STUDENT GRADE SYSTEM")
        print("================================")
        print("1. Add Student")
        print("2. Record / Update Scores")
        print("3. Display Students")
        print("4. Search Student")
        print("5. Edit Student Information")
        print("6. Delete Student")
        print("7. Class Summary")
        print("8. Sort Students")
        print("9. Save Records")
        print("10. Load Records")
        print("11. Exit")
        print("================================")

        choice = input("Enter your choice: ").strip()

        print("DEBUG: Menu choice entered:", choice)

        if choice == "1":
            add_student()

        elif choice == "2":
            record_scores()

        elif choice == "3":
            display_students()

        elif choice == "4":
            search_student()

        elif choice == "5":
            edit_student()

        elif choice == "6":
            delete_student()

        elif choice == "7":
            class_summary()

        elif choice == "8":
            sort_students()

        elif choice == "9":
            save_records()

        elif choice == "10":
            load_records()

        elif choice == "11":
            print("\nDEBUG: Saving records before exit...")
            save_records()

            print("SUCCESS: Program closed.")
            break

        else:
            print("ERROR: Invalid choice. Please enter a number from 1 to 11.")

        input("\nPress Enter to return to the menu...")


# ==============================
# PROGRAM START
# ==============================

if __name__ == "__main__":
    main()
