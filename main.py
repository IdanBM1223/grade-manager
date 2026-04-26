
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade


    def describe(self):
        print(f"the name of student is {self.name} and the grade is {self.grade}")


    def __str__(self):
        return f"{self.name}: {self.grade}"

students = []


def add_student():
    while True:
        name = input("Enter name: ")
        grade = float(input("Enter grade: "))
        s = Student(name, grade)
        students.append(s)

        again = input("Y/N ")
        if again.upper() == "N":
            break

def save_students():
    with open("student.txt", "w") as f:
        for stud in students:
            f.write(f"{stud}\n")



def load_students():
    try:
        with open("student.txt", "r") as f:
            for line in f:
                parts =line.split(": ")
                s = Student(parts[0], float(parts[1].strip()))
                students.append(s)
    except FileNotFoundError:
        print("No saved student in found")



def show_stats():
    grade = [stud.grade for stud in students ]
    # for stud in students:
    #     grade.append(stud.grade)

    print(f"Average grade: {sum(grade)/len(grade)}")
    print(f"Highest grade: {max(grade)}")
    print(f"Lowest grade: {min(grade)}")





def menu():
    while True:
        print("1. Add students")
        print("2. Show all students")
        print("3. Show stats")
        print("4. Save and exit")
        
        choice = input("Choose: ")
        
        if choice == "1":
            add_student()
        elif choice == "2":
            for stud in students:
                print(stud)
        elif choice == "3":
            show_stats()
        elif choice == "4":
            save_students()
            break


menu()