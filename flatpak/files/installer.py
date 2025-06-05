import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.font as tkfont
import threading
import subprocess
import sys
import os

font_family = "courier"
cache_dir = "/tmp/TrackMyPrompt-pip-cache"
os.makedirs(cache_dir, exist_ok=True)

class InstallerApp:
    def __init__(self, root, license_text=""):
        self.root = root
        self.license_text_str = license_text
        self.root.title("Installation de TrackMyPrompt")
        self.root.geometry("600x400")
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)
        self.step = 0
        self.install_success = False
        self.build_interface()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def build_interface(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        if self.step == 0:
            self.label = tk.Label(self.frame, text="Bienvenue dans l’installeur de TrackMyPrompt", font=(font_family, 14))
            self.label.pack(pady=40)
            self.next_button("Continuer")

        elif self.step == 1:
            self.label = tk.Label(self.frame, text="Licence d’utilisation", font=(font_family, 14))
            self.label.pack(pady=10)

            license_box = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, height=15)
            license_box.insert(tk.END, self.license_text_str)
            license_box.config(state=tk.DISABLED)
            license_box.pack(padx=10, pady=10, fill="both", expand=True)

            self.next_button("J’accepte")

        elif self.step == 2:
            self.label = tk.Label(self.frame, text="Installation des dépendances", font=(font_family, 14))
            self.label.pack(pady=10)

            tk.Label(self.frame, text="Cela peut prendre quelques minutes...", font=(font_family, 10)).pack()

            self.output_box = scrolledtext.ScrolledText(self.frame, height=15)
            self.output_box.pack(fill="both", expand=True, padx=10, pady=10)
            self.output_box.config(state=tk.DISABLED)

            self.install_button = tk.Button(self.frame, text="Installer", command=self.start_installation)
            self.install_button.pack(pady=10)

        elif self.step == 3:
            self.label = tk.Label(self.frame, text="Installation terminée", font=(font_family, 14))
            self.label.pack(pady=40)

            tk.Label(self.frame, text="Merci d’avoir installé TrackMyPrompt !", font=(font_family, 12)).pack(pady=10)
            tk.Button(self.frame, text="Quitter", command=self.quit_success).pack(pady=20)

    def next_button(self, text):
        tk.Button(self.frame, text=text, command=self.next_step).pack(pady=20)

    def next_step(self):
        self.step += 1
        self.build_interface()

    def start_installation(self):
        self.install_button.config(state=tk.DISABLED)
        threading.Thread(target=self.run_installation, daemon=True).start()

    def append_output(self, text):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.insert(tk.END, text)
        self.output_box.yview(tk.END)
        self.output_box.config(state=tk.DISABLED)

    def run_commands(self, commands):
        for command in commands:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                self.append_output(line)

            retcode = process.wait()
            if retcode != 0:
                messagebox.showerror("Erreur", f"La commande a échoué :\n{' '.join(command)}")
                self.install_button.config(state=tk.NORMAL)
                return False
        return True

    def run_installation(self):
        commands = [
            ["/app/bin/pip3", "install", "--no-warn-script-location", "--cache-dir", "/tmp/pip_cache", "-r", "/app/bin/TrackMyPrompt-cpu-requirements.txt"],
            ["/app/bin/pip3", "install", "--no-warn-script-location", "--cache-dir", "/tmp/pip_cache", "-r", "/app/bin/TrackMyPrompt-requirements.txt"],
        ]

        success = self.run_commands(commands)
        if success:
            self.install_success = True
            self.next_step()
        else:
            self.install_success = False

    def on_closing(self):
        # Si on ferme la fenêtre avant fin de l'install => exit(1)
        # Si install réussie, exit(0)
        if self.install_success:
            sys.exit(0)
        else:
            sys.exit(1)

    def quit_success(self):
        self.root.destroy()
        sys.exit(0)


if __name__ == "__main__":
    with open("/app/bin/TrackMyPrompt-LICENSE", "r") as f:
        license_text = f.read()

    root = tk.Tk()

    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(family=font_family, size=10)  # ou "Roboto", "Segoe UI", etc.
    root.option_add("*Font", default_font)
    
    app = InstallerApp(root, license_text)
    root.mainloop()
