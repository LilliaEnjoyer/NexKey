import customtkinter as ctk
from tkinter import messagebox, filedialog
from cryptography.fernet import Fernet
import os
import random
import string
import hashlib
import base64

COLOR_FONDO = ("#F0F2F5", "#0F0F0F")
COLOR_TARJETA = ("#FFFFFF", "#1A1A1A")
COLOR_ACCENTO = "#00B4D8"
COLOR_EXITO = "#2D6A4F"
COLOR_PELIGRO = "#E63946"

ctk.set_appearance_mode("dark")

class CryptoVaultApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NexKey")
        self.geometry("900x750")
        self.configure(fg_color=COLOR_FONDO)

        self.user_name = ""
        self.nfc_id = ""
        self.bio_pin = ""
        self.recovery_code = ""

        self.config_file = "user_config.bin"
        self.vault_folder = "Boveda_Privada"
        
        if not os.path.exists(self.vault_folder):
            os.makedirs(self.vault_folder)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.verificar_estado_inicial()

    def verificar_estado_inicial(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    datos = f.read().split("|")
                    if len(datos) == 4:
                        self.user_name, self.nfc_id, self.bio_pin, self.recovery_code = datos
                        self.mostrar_pantalla_acceso()
                    else:
                        self.mostrar_pantalla_registro()
            except Exception:
                self.mostrar_pantalla_registro()
        else:
            self.mostrar_pantalla_registro()

    def limpiar_pantalla(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def obtener_llave_maestra(self):
        combinacion = f"{self.nfc_id}{self.bio_pin}".encode()
        hash_seguro = hashlib.sha256(combinacion).digest()
        return Fernet(base64.urlsafe_b64encode(hash_seguro))

    def mostrar_pantalla_registro(self):
        self.limpiar_pantalla()
        frame = ctk.CTkFrame(self.main_container, fg_color=COLOR_TARJETA, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8)

        ctk.CTkLabel(frame, text="Registro de Bóveda", font=("Helvetica", 26, "bold"), text_color=COLOR_ACCENTO).pack(pady=20)
        
        self.reg_user = ctk.CTkEntry(frame, placeholder_text="Nombre de Usuario...", width=350, height=40)
        self.reg_user.pack(pady=10)

        self.reg_nfc = ctk.CTkEntry(frame, placeholder_text="ID de tu Tarjeta NFC...", width=350, height=40)
        self.reg_nfc.pack(pady=10)

        self.reg_bio = ctk.CTkEntry(frame, placeholder_text="Tu PIN de Seguridad...", show="*", width=350, height=40)
        self.reg_bio.pack(pady=10)

        ctk.CTkButton(
            frame,
            text="ACTIVAR CIFRADO",
            fg_color=COLOR_EXITO,
            height=50,
            width=300,
            command=self.guardar_registro
        ).pack(pady=30)

    def guardar_registro(self):
        u = self.reg_user.get()
        n = self.reg_nfc.get()
        b = self.reg_bio.get()

        if u and n and b:
            rec = ''.join(random.choices(string.digits, k=6))
            try:
                with open(self.config_file, "w") as f:
                    f.write(f"{u}|{n}|{b}|{rec}")
                messagebox.showinfo("Código de emergencia", f"Tu código es: {rec}")
                self.verificar_estado_inicial()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Error", "Completa todos los datos.")

    def mostrar_pantalla_acceso(self):
        self.limpiar_pantalla()
        frame = ctk.CTkFrame(self.main_container, fg_color=COLOR_TARJETA, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.6)

        ctk.CTkLabel(frame, text=f"Hola, {self.user_name}", font=("Helvetica", 24, "bold")).pack(pady=20)

        self.acc_nfc = ctk.CTkEntry(frame, placeholder_text="ID NFC...", width=350, height=45)
        self.acc_nfc.pack(pady=10)

        self.acc_bio = ctk.CTkEntry(frame, placeholder_text="PIN...", show="*", width=350, height=45)
        self.acc_bio.pack(pady=10)

        ctk.CTkButton(
            frame,
            text="DESCIFRAR Y ENTRAR",
            fg_color=COLOR_ACCENTO,
            height=50,
            width=300,
            command=self.verificar_acceso
        ).pack(pady=20)

        ctk.CTkButton(
            frame,
            text="Recuperar acceso",
            fg_color="transparent",
            text_color=COLOR_PELIGRO,
            command=self.recuperar
        ).pack()

    def verificar_acceso(self):
        if self.acc_nfc.get() == self.nfc_id and self.acc_bio.get() == self.bio_pin:
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def recuperar(self):
        dialogo = ctk.CTkInputDialog(text="Introduce código de 6 dígitos:", title="Recuperación")
        if dialogo.get_input() == self.recovery_code:
            self.mostrar_dashboard()

    def mostrar_dashboard(self):
        self.limpiar_pantalla()

        sidebar = ctk.CTkFrame(self.main_container, width=220, fg_color=COLOR_TARJETA, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(sidebar, text="NexKey", font=("Helvetica", 22, "bold"), text_color=COLOR_ACCENTO).pack(pady=30)

        ctk.CTkButton(sidebar, text="Archivos", fg_color="transparent", command=self.mostrar_dashboard).pack(fill="x", padx=10)
        ctk.CTkButton(sidebar, text="Ajustes", fg_color="transparent", command=self.mostrar_configuracion).pack(fill="x", padx=10)
        ctk.CTkButton(sidebar, text="Salir", fg_color=COLOR_PELIGRO, command=self.mostrar_pantalla_acceso).pack(side="bottom", pady=20)

        content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkLabel(header, text="Bóveda Cifrada", font=("Helvetica", 24, "bold")).pack(side="left")
        ctk.CTkButton(header, text="CIFRAR ARCHIVO", fg_color=COLOR_EXITO, command=self.subir_y_cifrar).pack(side="right")

        self.file_list = ctk.CTkScrollableFrame(content, fg_color=COLOR_TARJETA, corner_radius=15)
        self.file_list.pack(fill="both", expand=True, pady=20)

        self.actualizar_lista()

    def actualizar_lista(self):
        for w in self.file_list.winfo_children():
            w.destroy()

        for arch in os.listdir(self.vault_folder):
            f = ctk.CTkFrame(self.file_list, fg_color=("#F9F9F9", "#2A2A2A"), height=50)
            f.pack(fill="x", pady=5, padx=10)

            ctk.CTkLabel(f, text=arch[:30]).pack(side="left", padx=15)
            ctk.CTkButton(f, text="VER", width=60, command=lambda a=arch: self.abrir_y_descifrar(a)).pack(side="right", padx=5)

    def subir_y_cifrar(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            try:
                fernet = self.obtener_llave_maestra()
                with open(ruta, "rb") as f:
                    datos = f.read()

                datos_cifrados = fernet.encrypt(datos)

                destino = os.path.join(self.vault_folder, os.path.basename(ruta))
                with open(destino, "wb") as f:
                    f.write(datos_cifrados)

                self.actualizar_lista()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def abrir_y_descifrar(self, nombre):
        try:
            fernet = self.obtener_llave_maestra()
            ruta = os.path.join(self.vault_folder, nombre)

            with open(ruta, "rb") as f:
                datos = f.read()

            datos_claros = fernet.decrypt(datos)

            temp = os.path.join(os.environ.get("TEMP", "."), nombre)
            with open(temp, "wb") as f:
                f.write(datos_claros)

            if os.name == "nt":
                os.startfile(temp)
            else:
                os.system(f'open "{temp}"')

        except Exception:
            messagebox.showerror("Error", "No se pudo descifrar el archivo.")

    def mostrar_configuracion(self):
        self.limpiar_pantalla()

        f = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_TARJETA, corner_radius=20)
        f.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        ctk.CTkLabel(f, text="Ajustes de Perfil", font=("Helvetica", 24, "bold"), text_color=COLOR_ACCENTO).pack(pady=20)

        menu = ctk.CTkOptionMenu(
            f,
            values=["Dark", "Light", "System"],
            command=self.cambiar_tema,
            fg_color=COLOR_ACCENTO
        )
        menu.set(ctk.get_appearance_mode())
        menu.pack(pady=10)

        ctk.CTkLabel(
            f,
            text=f"Usuario: {self.user_name}\nNFC: {self.nfc_id}\nCódigo: {self.recovery_code}",
            justify="left"
        ).pack(pady=20)

        ctk.CTkButton(f, text="VOLVER", command=self.mostrar_dashboard).pack(pady=10)

    def cambiar_tema(self, tema):
        ctk.set_appearance_mode(tema)
        self.update()

if __name__ == "__main__":
    app = CryptoVaultApp()
    app.mainloop()