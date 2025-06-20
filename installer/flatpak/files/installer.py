import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import tkinter.font as tkfont
import threading
import subprocess
import sys
import os
from installer_translate import LANGUAGES, TRANSLATIONS

font_family = "courier"
cache_dir = "/tmp/TrackMyPrompt-pip-cache"
os.makedirs(cache_dir, exist_ok=True)

version_available = {
    "CUDA 11.8": "gpu-requirements/cuda118-requirements.txt",
    "CUDA 12.6": "gpu-requirements/cuda126-requirements.txt",
    "CUDA 12.8": "gpu-requirements/cuda128-requirements.txt",
    "ROCm": "gpu-requirements/rocm-requirements.txt",
    "CPU": "gpu-requirements/cpu-requirements.txt"
}

class InstallerApp:
    def __init__(self, root, license_text=""):
        self.root = root
        self.license_text_str = license_text
        self.current_language = "English"
        self.root.title(self.get_text("title"))
        self.root.geometry("600x400")
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)
        self.step = 0
        self.install_success = False
        self.build_interface()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_text(self, key):
        """Get translated text for current language"""
        return TRANSLATIONS[LANGUAGES[self.current_language]].get(key, key)

    def on_language_change(self, event=None):
        """Called when language changes in dropdown"""
        self.current_language = self.language_var.get()
        self.root.title(self.get_text("title"))
        self.build_interface()  # Rebuild interface with new language

    def build_interface(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        if self.step == 0:  # Language selection + Welcome
            # Welcome section
            self.label = tk.Label(self.frame, text=self.get_text("welcome"), font=(font_family, 14))
            self.label.pack(pady=20)

            # Language selection section
            lang_frame = tk.Frame(self.frame)
            lang_frame.pack(pady=20)

            tk.Label(lang_frame, text=self.get_text("choose_language"), font=(font_family, 12)).pack(pady=10)

            self.language_var = tk.StringVar()
            self.language_var.set(self.current_language)
            
            self.language_dropdown = ttk.Combobox(
                lang_frame, 
                textvariable=self.language_var,
                values=list(LANGUAGES.keys()),
                state="readonly",
                width=15,
                font=(font_family, 11)
            )
            self.language_dropdown.pack(pady=10)
            self.language_dropdown.bind('<<ComboboxSelected>>', self.on_language_change)

            tk.Button(lang_frame, text=self.get_text("continue"), command=self.next_step, font=(font_family, 10)).pack(pady=20)

        elif self.step == 1:
            self.label = tk.Label(self.frame, text=self.get_text("license"), font=(font_family, 14))
            self.label.pack(pady=10)

            license_box = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, height=15)
            license_box.insert(tk.END, self.license_text_str)
            license_box.config(state=tk.DISABLED)
            license_box.pack(padx=10, pady=10, fill="both", expand=True)

            self.next_button(self.get_text("accept"))

        elif self.step == 2:
            self.label = tk.Label(self.frame, text=self.get_text("installation"), font=(font_family, 14))
            self.label.pack(pady=10)

            # Version selection section
            self.version_frame = tk.Frame(self.frame)
            self.version_frame.pack(pady=20)

            tk.Label(self.version_frame, text=self.get_text("choose_version"), font=(font_family, 12)).pack(pady=10)

            self.version_var = tk.StringVar()
            self.version_var.set("CPU")  # Default selection

            version_options = list(version_available.keys())
            self.version_dropdown = ttk.Combobox(
                self.version_frame,
                textvariable=self.version_var,
                values=version_options,
                state="readonly",
                width=15,
                font=(font_family, 11)
            )
            self.version_dropdown.pack(pady=10)
            
            

            self.install_button = tk.Button(self.frame, text=self.get_text("install"), command=self.start_installation)
            self.install_button.pack(pady=10)

        elif self.step == 3:
            self.label = tk.Label(self.frame, text=self.get_text("completed"), font=(font_family, 14))
            self.label.pack(pady=40)

            tk.Label(self.frame, text=self.get_text("thanks"), font=(font_family, 12)).pack(pady=10)
            tk.Button(self.frame, text=self.get_text("quit"), command=self.quit_success).pack(pady=20)

    def next_button(self, text):
        tk.Button(self.frame, text=text, command=self.next_step).pack(pady=20)

    def next_step(self):
        self.step += 1
        self.build_interface()

    def start_installation(self):
        self.install_button.config(state=tk.DISABLED)
        self.version_frame.destroy()  # Remove version selection UI
        self.show_output_box()  # Show output box
        threading.Thread(target=self.run_installation, daemon=True).start()

    def show_output_box(self):
        tk.Label(self.frame, text=self.get_text("wait_message"), font=(font_family, 10)).pack()

        self.output_box = scrolledtext.ScrolledText(self.frame, height=12)
        self.output_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.output_box.config(state=tk.DISABLED)
        self.install_button.pack_forget()
        self.install_button.pack(pady=10)

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
                messagebox.showerror(self.get_text("error"), self.get_text("command_failed").format(' '.join(command)))
                self.install_button.config(state=tk.NORMAL)
                return False
        return True

    def run_installation(self):
        commands = [
            ["/app/bin/pip3", "install", "--no-warn-script-location", "--cache-dir", "/tmp/pip_cache", "-r", "/app/bin/" + version_available[self.version_var.get()]],
            ["/app/bin/pip3", "install", "--no-warn-script-location", "--cache-dir", "/tmp/pip_cache", "-r", "/app/bin/TrackMyPrompt-requirements.txt"],
        ]

        success = self.run_commands(commands)
        if success:
            self.install_success = True
            self.next_step()
        else:
            self.install_success = False

    def on_closing(self):
        # If window is closed before installation finishes => exit(1)
        # If installation succeeded, exit(0)
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
    default_font.configure(family=font_family, size=10)
    root.option_add("*Font", default_font)
    
    app = InstallerApp(root, license_text)
    root.mainloop()