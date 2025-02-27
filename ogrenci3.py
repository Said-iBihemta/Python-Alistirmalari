import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QMessageBox, QSpinBox
)

class Student:
    def __init__(self, name, number, courses):
        self.name = name
        self.number = number
        self.courses = courses

    def calculate_average(self):
        total_weight = sum(course['akts'] for course in self.courses)
        weighted_sum = sum((course['exam1'] + course['exam2']) / 2 * course['akts'] for course in self.courses)
        return weighted_sum / total_weight if total_weight else 0

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.students = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Öğrenci Yönetim Sistemi")
        self.setGeometry(100, 100, 600, 400)

        # Ana Widget ve Layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Başlık
        title = QLabel("Öğrenci Yönetim Sistemi")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        # Butonlar
        add_button = QPushButton("Yeni Öğrenci Ekle")
        add_button.clicked.connect(self.add_student_window)
        main_layout.addWidget(add_button)

        view_button = QPushButton("Öğrencileri Görüntüle")
        view_button.clicked.connect(self.view_students_window)
        main_layout.addWidget(view_button)

        save_button = QPushButton("Kaydet ve Çık")
        save_button.clicked.connect(self.save_and_exit)
        main_layout.addWidget(save_button)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def add_student_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Öğrenci Ekle")
        dialog.setGeometry(150, 150, 400, 300)

        layout = QFormLayout()

        name_input = QLineEdit()
        layout.addRow("Ad Soyad:", name_input)

        number_input = QLineEdit()
        layout.addRow("Numara:", number_input)

        course_inputs = []
        for i in range(3):
            course_name = QLineEdit()
            course_akts = QSpinBox()
            course_akts.setRange(1, 10)
            course_exam1 = QSpinBox()
            course_exam1.setRange(0, 100)
            course_exam2 = QSpinBox()
            course_exam2.setRange(0, 100)
            layout.addRow(f"Ders {i+1} Adı:", course_name)
            layout.addRow(f"Ders {i+1} AKTS:", course_akts)
            layout.addRow(f"Ders {i+1} Sınav 1:", course_exam1)
            layout.addRow(f"Ders {i+1} Sınav 2:", course_exam2)
            course_inputs.append((course_name, course_akts, course_exam1, course_exam2))

        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(lambda: self.save_student(dialog, name_input, number_input, course_inputs))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_student(self, dialog, name_input, number_input, course_inputs):
        name = name_input.text()
        number = number_input.text()
        courses = []
        for course_name, course_akts, course_exam1, course_exam2 in course_inputs:
            courses.append({
                "name": course_name.text(),
                "akts": course_akts.value(),
                "exam1": course_exam1.value(),
                "exam2": course_exam2.value()
            })
        self.students.append(Student(name, number, courses))
        QMessageBox.information(self, "Başarılı", "Öğrenci başarıyla eklendi!")
        dialog.close()

    def view_students_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Öğrencileri Görüntüle")
        dialog.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()
        table = QTableWidget()
        table.setRowCount(len(self.students))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Ad Soyad", "Numara", "Ortalama"])

        for row, student in enumerate(self.students):
            table.setItem(row, 0, QTableWidgetItem(student.name))
            table.setItem(row, 1, QTableWidgetItem(student.number))
            table.setItem(row, 2, QTableWidgetItem(f"{student.calculate_average():.2f}"))

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()

    def save_and_exit(self):
        data = [{"name": student.name, "number": student.number, "courses": student.courses} for student in self.students]
        with open("students.json", "w") as file:
            json.dump(data, file)
        QMessageBox.information(self, "Başarılı", "Veriler kaydedildi. Program kapatılıyor.")
        self.close()

# Uygulamayı Çalıştır
app = QApplication(sys.argv)
main_app = MainApp()
main_app.show()
sys.exit(app.exec_())
