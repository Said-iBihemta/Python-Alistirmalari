import tkinter as tk
from tkinter import messagebox
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

def add_student_window():
    def save_student():
        name = name_entry.get()
        number = number_entry.get()
        courses = []
        for i in range(3):
            course_name = course_entries[i][0].get()
            akts = int(course_entries[i][1].get())
            exam1 = int(course_entries[i][2].get())
            exam2 = int(course_entries[i][3].get())
            courses.append({"name": course_name, "akts": akts, "exam1": exam1, "exam2": exam2})
        students.append(Student(name, number, courses))
        messagebox.showinfo("Başarılı", "Öğrenci başarıyla eklendi!")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Yeni Öğrenci Ekle")

    tk.Label(add_window, text="Ad Soyad:").grid(row=0, column=0)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1)

    tk.Label(add_window, text="Numara:").grid(row=1, column=0)
    number_entry = tk.Entry(add_window)
    number_entry.grid(row=1, column=1)

    course_entries = []
    for i in range(3):
        tk.Label(add_window, text=f"Ders {i+1} Adı:").grid(row=2+i*4, column=0)
        course_name_entry = tk.Entry(add_window)
        course_name_entry.grid(row=2+i*4, column=1)

        tk.Label(add_window, text="AKTS:").grid(row=3+i*4, column=0)
        akts_entry = tk.Entry(add_window)
        akts_entry.grid(row=3+i*4, column=1)

        tk.Label(add_window, text="Sınav 1:").grid(row=4+i*4, column=0)
        exam1_entry = tk.Entry(add_window)
        exam1_entry.grid(row=4+i*4, column=1)

        tk.Label(add_window, text="Sınav 2:").grid(row=5+i*4, column=0)
        exam2_entry = tk.Entry(add_window)
        exam2_entry.grid(row=5+i*4, column=1)

        course_entries.append((course_name_entry, akts_entry, exam1_entry, exam2_entry))

    tk.Button(add_window, text="Kaydet", command=save_student).grid(row=14, column=0, columnspan=2)

def view_students_window():
    def display_student_info(student):
        info_window = tk.Toplevel(root)
        info_window.title(f"{student.name} - {student.number}")

        tk.Label(info_window, text=f"Ad Soyad: {student.name}").pack()
        tk.Label(info_window, text=f"Numara: {student.number}").pack()
        tk.Label(info_window, text="Dersler:").pack()

        for course in student.courses:
            tk.Label(info_window, text=f"{course['name']} - Ortalama: {(course['exam1'] + course['exam2']) / 2:.2f}").pack()

        avg = student.calculate_average()
        tk.Label(info_window, text=f"Genel Ortalama: {avg:.2f}").pack()

    view_window = tk.Toplevel(root)
    view_window.title("Öğrencileri Görüntüle")

    for idx, student in enumerate(students):
        tk.Button(view_window, text=f"{student.name} ({student.number})",
                  command=lambda s=student: display_student_info(s)).pack()

def save_and_exit():
    data = [{"name": student.name, "number": student.number, "courses": student.courses} for student in students]
    with open("students.json", "w") as file:
        json.dump(data, file)
    messagebox.showinfo("Başarılı", "Veriler kaydedildi. Program kapatılıyor.")
    root.destroy()

# Ana Pencere
root = tk.Tk()
root.title("Öğrenci Yönetim Sistemi")

students = []

tk.Label(root, text="Öğrenci Yönetim Sistemi", font=("Helvetica", 16)).pack(pady=10)
tk.Button(root, text="Yeni Öğrenci Ekle", command=add_student_window).pack(pady=5)
tk.Button(root, text="Öğrencileri Görüntüle", command=view_students_window).pack(pady=5)
tk.Button(root, text="Kaydet ve Çık", command=save_and_exit).pack(pady=5)

root.mainloop()
