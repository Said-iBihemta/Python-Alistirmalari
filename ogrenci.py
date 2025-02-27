import json

class Student:
    def __init__(self, name, number, courses):
        self.name = name
        self.number = number
        self.courses = courses

    def calculate_average(self):
        total_weight = sum(course['akts'] for course in self.courses)
        weighted_sum = sum((course['exam1'] + course['exam2']) / 2 * course['akts'] for course in self.courses)
        return weighted_sum / total_weight if total_weight else 0

    def edit_info(self, name=None, number=None, courses=None):
        if name: self.name = name
        if number: self.number = number
        if courses: self.courses = courses

def main_menu():
    students = []
    while True:
        print("\n1. Yeni Öğrenci Ekle")
        print("2. Öğrencileri Görüntüle/Düzenle")
        print("3. Kaydet ve Çık")
        choice = input("Seçiminiz: ")
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_or_edit_students(students)
        elif choice == "3":
            save_and_exit(students)
            break

def add_student(students):
    name = input("Ad-Soyad: ")
    number = input("Numara: ")
    courses = []
    for i in range(3):
        course_name = input(f"Ders {i+1} adı: ")
        akts = int(input(f"Ders {i+1} AKTS: "))
        exam1 = int(input(f"Ders {i+1} Sınav 1: "))
        exam2 = int(input(f"Ders {i+1} Sınav 2: "))
        courses.append({"name": course_name, "akts": akts, "exam1": exam1, "exam2": exam2})
    students.append(Student(name, number, courses))
    print("Öğrenci başarıyla eklendi!")

def view_or_edit_students(students):
    if not students:
        print("Hiç öğrenci yok.")
        return
    for idx, student in enumerate(students, start=1):
        print(f"{idx}. {student.name} ({student.number})")
    choice = int(input("Düzenlemek için öğrenci numarasını girin: ")) - 1
    if 0 <= choice < len(students):
        student = students[choice]
        print(f"\nAd: {student.name}")
        print(f"Numara: {student.number}")
        print("Dersler ve Ortalamaları:")
        for course in student.courses:
            print(f" - {course['name']}: {(course['exam1'] + course['exam2']) / 2}")
        print(f"Genel Ortalama: {student.calculate_average():.2f}")
        edit = input("Bilgi düzenlemek ister misiniz? (E/H): ").lower()
        if edit == 'e':
            student.name = input("Yeni ad (boş bırak: değişme): ") or student.name
            student.number = input("Yeni numara (boş bırak: değişme): ") or student.number
            # Ders bilgileri düzenleme işlemleri eklenebilir.

def save_and_exit(students):
    data = [{"name": student.name, "number": student.number, "courses": student.courses} for student in students]
    with open("students.json", "w") as file:
        json.dump(data, file)
    print("Veriler kaydedildi. Program sonlandırılıyor.")

if __name__ == "__main__":
    main_menu()
