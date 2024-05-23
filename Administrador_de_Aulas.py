import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import json
import os

# Define la ruta de acceso a los archivos usando relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')
BACKGROUND_IMAGE = os.path.join(BASE_DIR, 'background.jpg')
BACKGROUND_IMAGE_2 = os.path.join(BASE_DIR, 'background_2.jpg')

# Cargar datos de archivo JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Guardar datos en archivo JSON
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

# Función para calcular el promedio y estado del estudiante
def calculate_average_and_status(notes):
    average = sum(notes) / len(notes)
    status = "Aprobado" if average >= 51 else "Reprobado"
    return round(average, 2), status

# Clase principal de la aplicación
class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Alumnos")
        self.root.state('zoomed')  # Configurar ventana maximizada
        self.data = load_data()
        self.current_user = None
        self.current_classroom = None

        self.background_image = None

        self.login_screen()

    # Pantalla de inicio de sesión
    def login_screen(self):
        self.clear_window()
        
        # Imagen de fondo
        self.set_background_image(BACKGROUND_IMAGE)
        
        logo_label = tk.Label(self.root, text="Sistema de Gestión de Estudiantes", font=("Arial", 24), bg="steel blue", fg="white")
        logo_label.pack(pady=20)

        form_frame = tk.Frame(self.root, bg="steel blue")
        form_frame.pack(pady=10)

        username_label = tk.Label(form_frame, text="Nombre de Usuario:", bg="white")
        username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        password_label = tk.Label(form_frame, text="Contraseña:", bg="white")
        password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(form_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self.root, bg="steel blue")
        button_frame.pack(pady=20)

        create_user_button = tk.Button(button_frame, text="Crear Usuario", command=self.create_user)
        create_user_button.grid(row=0, column=0, padx=10)
        login_button = tk.Button(button_frame, text="Iniciar Sesión", command=self.login)
        login_button.grid(row=0, column=1, padx=10)

    # Crear nuevo usuario
    def create_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Advertencia", "Debe llenar todos los campos.")
            return

        if username in self.data:
            messagebox.showwarning("Advertencia", "Este Usuario ya existe, Inicia Sesión.")
        else:
            self.data[username] = {'password': password, 'classrooms': {}}
            save_data(self.data)
            messagebox.showinfo("Información", "Usuario creado exitosamente. Inicia sesión.")
    
    # Iniciar sesión
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username in self.data and self.data[username]['password'] == password:
            self.current_user = username
            self.user_screen()
        else:
            messagebox.showwarning("Advertencia", "Usuario o contraseña incorrectos.")

    # Pantalla principal de usuario
    def user_screen(self):
        self.clear_window()

        # Imagen de fondo
        self.set_background_image(BACKGROUND_IMAGE)
    
        top_frame = tk.Frame(self.root, bg="steel blue")
        top_frame.pack(fill=tk.X)

        welcome_label = tk.Label(top_frame, text=f"Bienvenido {self.current_user}!", font=("Arial", 35), bg="steel blue", fg="white")
        welcome_label.pack(pady=20, side=tk.TOP)
    
        logout_button = tk.Button(top_frame, text="Cerrar Sesión", command=self.logout)
        logout_button.pack(side=tk.LEFT, padx=10)

        create_classroom_button = tk.Button(top_frame, text="Crear Aula", command=self.create_classroom)
        create_classroom_button.pack(side=tk.LEFT, padx=10)

        if self.data[self.current_user]['classrooms']:
            classrooms_frame = tk.Frame(self.root, bg="steel blue")
            classrooms_frame.pack(pady=5)
            tk.Label(classrooms_frame, text="Aulas disponibles:", font=("Arial", 15), bg="steel blue", fg="white").pack(pady=5)
            for classroom in self.data[self.current_user]['classrooms']:
                classroom_frame = tk.Frame(classrooms_frame, bg="white")
                classroom_frame.pack(fill="x")
                classroom_button = tk.Button(classroom_frame, text=classroom, command=lambda c=classroom: self.classroom_screen(c))
                classroom_button.pack(side=tk.LEFT, padx=5, pady=2)
                delete_button = tk.Button(classroom_frame, text="Eliminar", command=lambda c=classroom: self.delete_classroom_confirmation(c))
                delete_button.pack(side=tk.RIGHT, padx=5, pady=2)

    # Confirmación de eliminación de aula
    def delete_classroom_confirmation(self, classroom_name):
        confirm = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar esta aula?")
        if confirm:
            del self.data[self.current_user]['classrooms'][classroom_name]
            save_data(self.data)
            self.user_screen()

    # Cerrar sesión
    def logout(self):
        self.current_user = None
        self.login_screen()

    # Crear nuevo aula
    def create_classroom(self):
        classroom_name = simpledialog.askstring("Crear Aula", "Nombre del Aula:")
        if classroom_name:
            self.data[self.current_user]['classrooms'][classroom_name] = []
            save_data(self.data)
            self.user_screen()

    # Pantalla de lista de alumnos en el aula
    def classroom_screen(self, classroom_name):
        self.clear_window()
        
        # Imagen de fondo
        self.set_background_image(BACKGROUND_IMAGE_2)

        self.current_classroom = classroom_name

        top_frame = tk.Frame(self.root, bg="steel blue")
        top_frame.pack(fill=tk.X)

        back_button = tk.Button(top_frame, text="Menu Principal", command=self.user_screen)
        back_button.pack(side=tk.LEFT, padx=10, pady=10)

        add_student_button = tk.Button(top_frame, text="Agregar Estudiante", command=self.add_student_form)
        add_student_button.pack(side=tk.LEFT, padx=10, pady=10)

        search_label = tk.Label(top_frame, text="Buscar:", bg="white")
        search_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.search_entry = tk.Entry(top_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=10)
        self.search_entry.bind("<KeyRelease>", self.search_student)

        self.sort_order = tk.StringVar()
        self.sort_order.set("Ordenar Promedio")
        sort_menu = tk.OptionMenu(top_frame, self.sort_order, "De menor a mayor", "De mayor a menor", command=self.sort_students)
        sort_menu.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(self.root, text=classroom_name, font=("Arial", 24), bg="steel blue", fg="white").pack(pady=20)

        self.student_list_frame = tk.Frame(self.root, bg="white")
        self.student_list_frame.pack(pady=20)

        self.display_students(self.data[self.current_user]['classrooms'][classroom_name])

    # Mostrar lista de estudiantes
    def display_students(self, students):
        for widget in self.student_list_frame.winfo_children():
            widget.destroy()

        headers = ["Estudiante", "Nota 1", "Nota 2", "Nota 3", "Nota 4", "Promedio", "Estado", "Acción"]
        for i, header in enumerate(headers):
            tk.Label(self.student_list_frame, text=header, borderwidth=1, relief="solid", width=10, bg="white", anchor="s").grid(row=0, column=i)

        for i, student in enumerate(students):
            tk.Label(self.student_list_frame, text=student['name'], borderwidth=1, relief="solid", bg="white", anchor="s").grid(row=i + 1, column=0)
            for j in range(1, 5):
                tk.Label(self.student_list_frame, text=student['notes'][j-1], borderwidth=1, relief="solid", bg="white").grid(row=i + 1, column=j)
            tk.Label(self.student_list_frame, text=student['average'], borderwidth=1, relief="solid", bg="white").grid(row=i + 1, column=5)
            if student['status'] == "Aprobado":
                tk.Label(self.student_list_frame, text=student['status'], borderwidth=1, relief="solid", bg="green", fg="white").grid(row=i + 1, column=6)
            else:
                tk.Label(self.student_list_frame, text=student['status'], borderwidth=1, relief="solid", bg="red", fg="white").grid(row=i + 1, column=6)
            tk.Button(self.student_list_frame, text="Eliminar", command=lambda s=student: self.delete_student(s)).grid(row=i + 1, column=7)

    # Ordenar lista de estudiantes
    def sort_students(self, order):
        students = self.data[self.current_user]['classrooms'][self.current_classroom]
        reverse = order == "De mayor a menor"
        students.sort(key=lambda x: x['average'], reverse=reverse)
        self.display_students(students)

    # Buscar estudiante
    def search_student(self, event):
        query = self.search_entry.get().upper()
        students = self.data[self.current_user]['classrooms'][self.current_classroom]
        filtered_students = [s for s in students if query in s['name'].upper()]
        self.display_students(filtered_students)

    # Formulario para agregar estudiante
    def add_student_form(self):
        form = tk.Toplevel(self.root)
        form.title("Agregar Estudiante")
        form.geometry("255x150")

        tk.Label(form, text="Nombre Completo:").grid(row=0, column=0)
        name_entry = tk.Entry(form)
        name_entry.grid(row=0, column=1)

        notes_entries = []
        for i in range(1, 5):
            tk.Label(form, text=f"Nota {i}:").grid(row=i, column=0)
            note_entry = tk.Entry(form)
            note_entry.grid(row=i, column=1)
            notes_entries.append(note_entry)

        def add_student():
            name = name_entry.get().strip()
            try:
                notes = [float(note_entry.get()) for note_entry in notes_entries]
                if any(note < 0 or note > 100 for note in notes):
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Advertencia", "Las notas deben estar entre 0 y 100 con un máximo de 2 decimales.")
                return

            average, status = calculate_average_and_status(notes)
            student = {'name': name, 'notes': notes, 'average': average, 'status': status}
            self.data[self.current_user]['classrooms'][self.current_classroom].append(student)
            save_data(self.data)
            form.destroy()
            self.display_students(self.data[self.current_user]['classrooms'][self.current_classroom])

        add_button = tk.Button(form, text="Agregar", command=add_student)
        add_button.grid(row=5, column=1)
        cancel_button = tk.Button(form, text="Cancelar", command=form.destroy)
        cancel_button.grid(row=5, column=0)

    # Eliminar estudiante
    def delete_student(self, student):
        self.data[self.current_user]['classrooms'][self.current_classroom].remove(student)
        save_data(self.data)
        self.display_students(self.data[self.current_user]['classrooms'][self.current_classroom])

    # Limpiar la ventana
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Establecer imagen de fondo
    def set_background_image(self, image_path):
        image = Image.open(image_path)
        self.background_image = ImageTk.PhotoImage(image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.lower()

# Inicializar la aplicación
root = tk.Tk()
app = StudentManagementApp(root)
root.mainloop()
