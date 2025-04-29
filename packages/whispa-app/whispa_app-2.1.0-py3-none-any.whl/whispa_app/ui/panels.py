# src/whispa_app/ui/panels.py

import customtkinter as ctk

def build_panels(parent, save_transcribe, save_translate):
    """
    Build two side‑by‑side text panels with padding between them.
    Returns (transcription_box, translation_box).
    """
    # Transcription panel
    tframe = ctk.CTkFrame(parent)
    tframe.grid(row=0, column=0, sticky="nsew", padx=(0,5), pady=10)
    tbox = ctk.CTkTextbox(tframe)
    tbox.pack(fill="both", expand=True, padx=5, pady=5)
    ctk.CTkButton(
        tframe,
        text="Save",
        command=lambda: save_transcribe(tbox.get("1.0","end"))
    ).pack(pady=(0,5))

    # Translation panel
    dframe = ctk.CTkFrame(parent)
    dframe.grid(row=0, column=1, sticky="nsew", padx=(5,0), pady=10)
    dbox = ctk.CTkTextbox(dframe)
    dbox.pack(fill="both", expand=True, padx=5, pady=5)
    ctk.CTkButton(
        dframe,
        text="Save",
        command=lambda: save_translate(dbox.get("1.0","end"))
    ).pack(pady=(0,5))

    # Make the two columns resize equally
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)

    return tbox, dbox
