from controller.controller import Controller
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import askyesno, showinfo, showerror


class View:

    def __init__(self):
        self._controller = Controller()

    def action_window(self, root_window, default_target_name, action_name, action_method):

        def set_target_path(target, length):
            def callback(target):
                c = target.get()[0:length - 1]
                target.set(c)
                if not self._controller.target_event(target.get()):
                    ent_password.configure(state='disabled')
                    btn_action.configure(state='disabled')
                else:
                    ent_password.configure(state='normal')

            target.trace("w", lambda name, index, mode, target=target: callback(target))

        def set_password_str(str_var, length):
            def callback(str_var):
                c = str_var.get()[0:length - 1]
                str_var.set(c)
                if len(str_var.get()) > 7:
                    self._controller.password = c
                    btn_action.configure(state='normal')
                else:
                    btn_action.configure(state='disabled')

            str_var.trace("w", lambda name, index, mode, str_var=str_var: callback(str_var))

        def set_source_path():
            filename = filedialog.askopenfilename(initialdir="/",
                                                  title="Select a File",
                                                  filetypes=(("Any",
                                                              "*.*"),
                                                             ("all files",
                                                              "*.*")))
            self._controller.source_event(filename)
            self._controller.target_event(default_target_name)
            ent_source_path.configure(state='normal')
            ent_source_path.delete(0, tk.END)
            ent_source_path.insert(0, filename)
            ent_source_path.configure(state='disabled')
            ent_target_path.configure(state='normal')

        def perform_action():
            answer = askyesno(title='Confirmation',
                              message=f"¿Desea {action_name} ahora?")
            if answer:
                if not action_method() == 0:
                    showerror(f"{action_name}", "Error inesperado, inténtelo de nuevo")
                else:
                    showinfo(f"{action_name}", "Operación realizada satisfactoriamente")

        window = tk.Toplevel(root_window)
        window.grab_set()
        window.title(action_name.capitalize())
        window.geometry("500x500")
        window.update_idletasks()
        View.center_frame(window)
        window.resizable(False, False)
        window.configure(background="#1c1b1b")
        window.columnconfigure(0, weight=1)
        window.rowconfigure([0, 1, 2, 3], weight=1)

        frame_1 = tk.Frame(window, width=500, height=500, background="#1c1b1b")
        frame_1.rowconfigure([0, 1], weight=1)
        frame_1.columnconfigure([0, 1], weight=1)
        lbl_source = tk.Label(master=frame_1, text="Archivo fuente", fg="white", font=('Helvetica', 13),
                              background="#1c1b1b")
        btn_explore = tk.Button(frame_1,
                                text="Browse File",
                                command=set_source_path, font=('Helvetica', 13),
                                bg="#333", bd=0, fg="white", padx=5, pady=5)
        ent_source_path = tk.Entry(frame_1, fg="white", bg="#333", width=45, font=('Helvetica', 11), bd=0,
                                   state="disabled", disabledbackground="#333")
        ent_source_path.configure()

        lbl_source.grid(column=0, row=0, padx=0)
        ent_source_path.grid(column=1, row=1, pady=(40, 0))
        btn_explore.grid(column=0, row=1, padx=(0, 10), pady=(30, 0))
        frame_1.grid(column=0, row=0)

        frame_2 = tk.Frame(window, width=500, background="#1c1b1b")
        frame_2.rowconfigure([0, 1, 2], weight=2)
        frame_2.columnconfigure(0, weight=1)
        lbl_target = tk.Label(master=frame_2, text=f"Nombre de archivo {default_target_name} (puede quedar vacío)",
                              fg="white",
                              font=('Helvetica', 13),
                              background="#1c1b1b")
        lbl_target2 = tk.Label(master=frame_2, text="Nombre por defecto: " + default_target_name, fg="white",
                               font=('Helvetica', 13),
                               background="#1c1b1b")
        target = tk.StringVar(window)
        set_target_path(target, 49)
        ent_target_path = tk.Entry(frame_2, textvariable=target, fg="white", bg="#333", width=45,
                                   font=('Helvetica', 11), bd=0,
                                   state='disabled', disabledbackground="#333")

        lbl_target.grid(column=0, row=0, padx=(0, 60), pady=(0, 10), sticky="w")
        lbl_target2.grid(column=0, row=1, padx=0, sticky="w")
        ent_target_path.grid(column=0, row=2, padx=(0, 50), pady=(20, 0), sticky="w")
        frame_2.grid(column=0, row=1)

        frame_3 = tk.Frame(window, width=500, background="#1c1b1b")
        frame_3.rowconfigure([0, 1], weight=2)
        frame_3.columnconfigure(0, weight=1)
        lbl_password = tk.Label(master=frame_3, text="Contraseña", fg="white",
                                font=('Helvetica', 13),
                                background="#1c1b1b")
        password = tk.StringVar(window)
        set_password_str(password, 16)
        ent_password = tk.Entry(frame_3, textvariable=password, show="•", fg="white", bg="#333", width=45,
                                font=('Helvetica', 11), bd=0, disabledbackground="#333")
        lbl_password.grid(column=0, row=0, sticky="w")
        ent_password.grid(column=0, row=1, padx=(0, 115), pady=(20, 0), sticky="w")
        frame_3.grid(column=0, row=2)

        frame_4 = tk.Frame(window, width=500, background="#1c1b1b")
        frame_4.rowconfigure(0, weight=1)
        frame_4.columnconfigure(0, weight=1)
        btn_action = tk.Button(frame_4,
                               text=action_name.capitalize(), font=('Helvetica', 13),
                               bg="#333", bd=0, fg="white", padx=5, pady=5, state="disabled", command=perform_action)
        btn_action.grid(column=0, row=0, pady=(30, 30))
        frame_4.grid(column=0, row=4)

    def center_frame(window):
        windowWidth = window.winfo_width()
        windowHeight = window.winfo_height()
        positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 2)
        window.geometry("+{}+{}".format(positionRight, positionDown))

    def menu(self):
        window = tk.Tk()
        window.title("Menu")
        window.geometry("500x500")
        window.update_idletasks()
        View.center_frame(window)
        window.resizable(False, False)
        window.configure(background="#1c1b1b")
        frame = tk.Frame(window, width=250, height=400, background="#1c1b1b")
        frame.place(relx=.5, rely=.5, anchor=tk.CENTER)
        frame.grid_rowconfigure([0, 1], weight=1)
        frame.grid_columnconfigure(1, weight=1)
        btn_encrypt_window = tk.Button(master=frame, text="Encriptar", width=20, height=2, font=('Helvetica', 15),
                                       bg="#333", bd=0, fg="white",
                                       command=lambda: View.action_window(self, window, "encriptado",
                                                                           "encriptar", self._controller.encrypt))
        btn_encrypt_window.grid(row=0, column=0, padx=10, pady=20)
        btn_decrypt_window = tk.Button(master=frame, text="Desencriptar", width=20, height=2, font=('Helvetica', 15),
                                       bg="#333", bd=0, fg="white",
                                       command=lambda: View.action_window(self, window, "desencriptado",
                                                                           "desencriptar", self._controller.decrypt))
        btn_decrypt_window.grid(row=1, column=0, padx=10, pady=(0, 20))
        window.mainloop()
