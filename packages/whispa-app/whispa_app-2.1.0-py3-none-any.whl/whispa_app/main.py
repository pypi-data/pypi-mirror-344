# src/whispa_app/main.py

import sys
import os
import threading
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
import psutil
import torch

from whispa_app.device import select_device
from whispa_app.transcription import transcribe_file
from whispa_app.translation import translate
from whispa_app.utils import simplify_text
from whispa_app.ui.panels import build_panels

# Available model sizes and languages
MODELS    = ["tiny", "base", "small", "medium", "large"]
LANGUAGES = ["Spanish", "French", "German", "Chinese", "Japanese"]

def resource_path(rel: str) -> str:
    """
    Resolve a path to a resource, working both in development and when bundled by PyInstaller.
    """
    if getattr(sys, "_MEIPASS", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, rel)

class ToolTip:
    """
    Simple tooltip that appears on hover for any widget.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwin = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _=None):
        if self.tipwin:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwin = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10)
        ).pack(ipadx=1)

    def hide(self, _=None):
        if self.tipwin:
            self.tipwin.destroy()
            self.tipwin = None

# Set up root-level logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logging.getLogger("transformers").setLevel(logging.WARNING)
logging.getLogger("torch").setLevel(logging.WARNING)

class WhispaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ----------------------------
        # Window configuration
        # ----------------------------
        self.title("Whispa App")
        self.minsize(800, 600)

        # ----------------------------
        # Advanced settings variables
        # ----------------------------
        self.adv_vram           = tk.IntVar(value=6)
        self.adv_tbeam          = tk.IntVar(value=5)
        self.adv_vad            = tk.BooleanVar(value=True)
        self.adv_num_beams      = tk.IntVar(value=8)
        self.adv_length_penalty = tk.DoubleVar(value=0.8)
        self.adv_temperature    = tk.DoubleVar(value=0.3)

        # ----------------------------
        # Load application icon
        # ----------------------------
        for ico in ("assets/icon.ico", "assets/icon.png"):
            path = resource_path(ico)
            if not os.path.isfile(path):
                continue
            try:
                if ico.endswith(".ico"):
                    self.iconbitmap(path)
                else:
                    # Keep a reference so it's not garbage-collected
                    self._icon_img = tk.PhotoImage(file=path)
                    self.iconphoto(True, self._icon_img)
                break
            except Exception:
                continue

        # ----------------------------
        # Build the menu bar
        # ----------------------------
        self._create_menubar()

        # ----------------------------
        # Main content container
        # ----------------------------
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)

        # ----------------------------
        # Row 0: File picker + Model selection
        # ----------------------------
        row0 = ctk.CTkFrame(container)
        row0.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10,5))
        row0.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(row0, text="Select audio file:", font=("Arial",14))\
            .grid(row=0, column=0, padx=5)
        self.file_entry = ctk.CTkEntry(row0, font=("Arial",14))
        self.file_entry.grid(row=0, column=1, sticky="ew", padx=(0,5))
        browse_btn = ctk.CTkButton(row0, text="Browse", font=("Arial",14), command=self._on_browse)
        browse_btn.grid(row=0, column=2, padx=5)
        ToolTip(browse_btn, "Browse for an audio file")

        ctk.CTkLabel(row0, text="Model:", font=("Arial",14))\
            .grid(row=0, column=3, padx=(20,5))
        self.model_menu = ctk.CTkOptionMenu(
            row0, values=MODELS,
            variable=ctk.StringVar(value=MODELS[2]),
            font=("Arial",14)
        )
        self.model_menu.grid(row=0, column=4, padx=5)

        # ----------------------------
        # Row 1: Transcribe button (centered)
        # ----------------------------
        row1 = ctk.CTkFrame(container)
        row1.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,10))
        self.transcribe_btn = ctk.CTkButton(
            row1, text="▶ Transcribe", font=("Arial",16),
            command=self._on_transcribe
        )
        self.transcribe_btn.pack()
        ToolTip(self.transcribe_btn, "Run transcription")

        # ----------------------------
        # Row 2: Transcription & Translation panels
        # ----------------------------
        panel = ctk.CTkFrame(container)
        panel.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=(0,10))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=1)
        self.transcription_box, self.translation_box = build_panels(
            panel,
            save_transcribe=self._save_transcription,
            save_translate=self._save_translation
        )

        # ----------------------------
        # Row 3: Language dropdown + Translate button (centered)
        # ----------------------------
        row3 = ctk.CTkFrame(container)
        row3.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0,10))
        inner3 = ctk.CTkFrame(row3)
        inner3.pack()
        ctk.CTkLabel(inner3, text="Language:", font=("Arial",14))\
            .pack(side="left", padx=5)
        self.lang_menu = ctk.CTkOptionMenu(
            inner3, values=LANGUAGES,
            variable=ctk.StringVar(value=LANGUAGES[0]),
            font=("Arial",14)
        )
        self.lang_menu.pack(side="left", padx=5)
        self.translate_btn = ctk.CTkButton(
            inner3, text="▶ Translate", font=("Arial",16),
            command=self._on_translate
        )
        self.translate_btn.pack(side="left", padx=(20,0))
        ToolTip(self.translate_btn, "Translate the transcription")

        # ----------------------------
        # Row 4: Advanced Settings (hidden by default)
        # ----------------------------
        self.adv_frame = ctk.CTkFrame(container)
        self.adv_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=(0,10))
        def _add(label, var, tip, width=60):
            ctk.CTkLabel(self.adv_frame, text=label, font=("Arial",14))\
                .pack(side="left", padx=(5,2))
            ent = ctk.CTkEntry(self.adv_frame, textvariable=var, font=("Arial",14), width=width)
            ent.pack(side="left", padx=(0,5))
            ToolTip(ent, tip)
        _add("VRAM",   self.adv_vram,           "Min GPU VRAM (GB)",         50)
        _add("Beam",   self.adv_tbeam,          "Transcribe beam size",      50)
        cb = ctk.CTkCheckBox(self.adv_frame, text="VAD", variable=self.adv_vad)
        cb.pack(side="left", padx=(10,5))
        ToolTip(cb, "Enable voice-activity detection")
        _add("T-beams",self.adv_num_beams,      "Translation beam size",     50)
        _add("LenPen", self.adv_length_penalty, "Length penalty",            50)
        _add("Temp",   self.adv_temperature,    "Sampling temperature",      50)
        self.adv_frame.grid_remove()

        # ----------------------------
        # Row 5: Progress bars and labels
        # ----------------------------
        row5 = ctk.CTkFrame(container)
        row5.grid(row=5, column=0, columnspan=2, sticky="ew", padx=20, pady=(0,10))
        self.transcribe_progress = ctk.CTkProgressBar(row5)
        self.transcribe_progress.pack(fill="x", pady=(5,2))
        self.transcribe_label = ctk.CTkLabel(row5, text="Ready to transcribe", font=("Arial",14))
        self.transcribe_label.pack(pady=(0,5))
        self.translate_progress = ctk.CTkProgressBar(row5)
        self.translate_progress.pack(fill="x", pady=(5,2))
        self.translate_label = ctk.CTkLabel(row5, text="Ready to translate", font=("Arial",14))
        self.translate_label.pack(pady=(0,5))

        # ----------------------------
        # Footer: System stats
        # ----------------------------
        footer = ctk.CTkFrame(self)
        footer.pack(fill="x", side="bottom", pady=(0,5))
        self.stats_lbl = ctk.CTkLabel(footer, text="System Stats: N/A", font=("Arial",14))
        self.stats_lbl.pack()

        # Start periodic system stats updates
        self._update_stats()

    def _create_menubar(self):
        """
        Create the File / Advanced / Help menus with slightly larger font.
        """
        menubar = tk.Menu(self)
        font = ("Arial", 16)

        file_menu = tk.Menu(menubar, tearoff=0, font=font)
        file_menu.add_command(label="Save Transcript", command=lambda: self._save_transcription(self.transcription_box.get("1.0","end")))
        file_menu.add_command(label="Save Translation", command=lambda: self._save_translation(self.translation_box.get("1.0","end")))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        adv_menu = tk.Menu(menubar, tearoff=0, font=font)
        adv_menu.add_command(label="Toggle Settings", command=self.toggle_advanced)
        menubar.add_cascade(label="Advanced", menu=adv_menu)

        help_menu = tk.Menu(menubar, tearoff=0, font=font)
        help_menu.add_command(label="View Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _on_browse(self):
        """Handle the Browse button click."""
        path = filedialog.askopenfilename(filetypes=[("Audio","*.wav *.mp3")])
        if path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, path)

    def _on_transcribe(self):
        """Start transcription in a background thread."""
        audio = self.file_entry.get().strip()
        if not audio:
            return messagebox.showerror("Error", "Select a file first.")
        self.transcribe_btn.configure(state="disabled")
        self.transcription_box.delete("1.0","end")
        self.translation_box.delete("1.0","end")
        self.transcribe_progress.set(0)
        self.transcribe_label.configure(text="Transcribing…")

        args = (
            audio,
            self.model_menu.get(),
            self.adv_vram.get(),
            lambda f,_: (
                self.transcribe_progress.set(f),
                self.transcribe_label.configure(text=f"Transcribing: {f*100:.1f}%")
            ),
            self.adv_tbeam.get(),
            self.adv_vad.get()
        )
        threading.Thread(target=self._run_transcribe, args=(args,), daemon=True).start()

    def _run_transcribe(self, args):
        """Worker thread for transcription."""
        try:
            text = transcribe_file(*args)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        else:
            self.after(0, lambda: self.transcription_box.insert("1.0", text))
        finally:
            self.after(0, lambda: self.transcribe_btn.configure(state="normal"))

    def _on_translate(self):
        """Start translation in a background thread."""
        src = self.transcription_box.get("1.0","end").strip()
        if not src:
            return messagebox.showerror("Error","Nothing to translate.")
        self.translate_btn.configure(state="disabled")
        self.translate_progress.set(0)
        self.translate_label.configure(text="Translating…")

        args = (
            src,
            self.lang_menu.get(),
            lambda i,t: (
                self.translate_progress.set(i/t),
                self.translate_label.configure(text=f"Translating: {i/t*100:.1f}%")
            ),
            self.adv_num_beams.get(),
            self.adv_length_penalty.get(),
            self.adv_temperature.get()
        )
        threading.Thread(target=self._run_translate, args=(args,), daemon=True).start()

    def _run_translate(self, args):
        """Worker thread for translation."""
        try:
            out = translate(
                args[0], args[1],
                progress_callback=args[2],
                num_beams=args[3],
                length_penalty=args[4],
                temperature=args[5]
            )
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        else:
            self.after(0, lambda: self.translation_box.insert("1.0", out))
        finally:
            self.after(0, lambda: self.translate_btn.configure(state="normal"))

    def _update_stats(self):
        """Periodically update CPU/RAM/GPU usage in the footer."""
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            parts = [f"CPU: {cpu:.1f}%", f"RAM: {ram:.1f}%"]
            if torch.cuda.is_available():
                used = torch.cuda.memory_reserved(0)
                total = torch.cuda.get_device_properties(0).total_memory
                parts.append(f"GPU: {used/total*100:.1f}%")
            self.stats_lbl.configure(text="System Stats:   " + "   ".join(parts))
        except:
            self.stats_lbl.configure(text="System Stats: Error")
        self.after(5000, self._update_stats)

    def toggle_advanced(self):
        """Show or hide the advanced settings row."""
        if self.adv_frame.winfo_ismapped():
            self.adv_frame.grid_remove()
        else:
            self.adv_frame.grid()

    def _save_transcription(self, txt):
        """Save transcription text to a file."""
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(simplify_text(txt))
            messagebox.showinfo("Saved", f"Transcript saved to:\n{path}")

    def _save_translation(self, txt):
        """Save translation text to a file."""
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(simplify_text(txt))
            messagebox.showinfo("Saved", f"Translation saved to:\n{path}")

    def show_help(self):
        """Display the help dialog."""
        messagebox.showinfo(
            "Help",
            "1) Browse file. 2) ▶ Transcribe.\n"
            "3) Select language & ▶ Translate.\n"
            "4) Save via File menu.\n\n"
            "Use Advanced ▶ Toggle Settings to tweak VRAM, beams, VAD, etc."
        )

    def show_about(self):
        """Display the about dialog."""
        messagebox.showinfo("About", "Whispa App\nVersion 2.1.0\n© 2025")

def launch_app():
    app = WhispaApp()
    app.mainloop()

if __name__ == "__main__":
    launch_app()
