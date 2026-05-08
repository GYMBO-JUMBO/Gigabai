import customtkinter as ctk
from database import get_user, update_user

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, username, theme="dark"):
        bg = "#0a1628" if theme == "dark" else "#f0f4f8"
        super().__init__(parent, fg_color=bg)
        self.username = username
        self.theme = theme
        self.build_ui()

    def build_ui(self):
        dark = self.theme == "dark"
        bg        = "#0a1628"   if dark else "#f0f4f8"
        card_bg   = "#0f2044"   if dark else "#ffffff"
        border    = "#1e4080"   if dark else "#c0d4f0"
        title_col = "#4da6ff"   if dark else "#1565c0"
        label_col = "#a0c4ff"   if dark else "#1565c0"
        text_col  = "white"     if dark else "#1a1a2e"
        sub_col   = "#6b8cba"   if dark else "#5a7a9a"
        entry_bg  = "#0a1e3d"   if dark else "#e8f0fe"
        entry_brd = "#1e4080"   if dark else "#90b4e0"
        btn_fg    = "#1565c0"
        btn_hov   = "#1976d2"

        self.configure(fg_color=bg)

        # Scroll
        scroll = ctk.CTkScrollableFrame(self, fg_color=bg)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)

        # Header
        ctk.CTkLabel(scroll, text="👤  My Profile",
                     font=("Arial", 22, "bold"), text_color=title_col).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(scroll, text="Your personal information",
                     font=("Arial", 13), text_color=sub_col).pack(anchor="w", pady=(0, 20))

        # Card
        card = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=18,
                            border_width=1, border_color=border)
        card.pack(fill="x", pady=(0, 20))

        user = get_user(self.username) or {}

        fields = [
            ("First Name",   "first_name",  "e.g. Dmitriy"),
            ("Last Name",    "last_name",   "e.g. Korostylev"),
            ("Workplace",    "workplace",   "e.g. ABC Company"),
            ("Bank Name",    "bank_name",   "e.g. Kaspi Bank"),
        ]

        self.entries = {}
        for i, (label, key, placeholder) in enumerate(fields):
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=(18 if i == 0 else 10, 0))
            ctk.CTkLabel(row, text=label, font=("Arial", 13, "bold"),
                         text_color=label_col, width=130, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(
                row, placeholder_text=placeholder,
                height=40, corner_radius=10,
                fg_color=entry_bg, border_color=entry_brd,
                text_color=text_col, font=("Arial", 13)
            )
            entry.pack(side="left", fill="x", expand=True)
            val = user.get(key, "")
            if val:
                entry.insert(0, val)
            self.entries[key] = entry

        # Username (read-only)
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=30, pady=(10, 20))
        ctk.CTkLabel(row, text="Username", font=("Arial", 13, "bold"),
                     text_color=label_col, width=130, anchor="w").pack(side="left")
        u_entry = ctk.CTkEntry(
            row, height=40, corner_radius=10,
            fg_color=entry_bg, border_color=entry_brd,
            text_color="#6b8cba", font=("Arial", 13),
            state="disabled"
        )
        u_entry.pack(side="left", fill="x", expand=True)
        u_entry.configure(state="normal")
        u_entry.insert(0, self.username)
        u_entry.configure(state="disabled")

        # Message
        self.msg = ctk.CTkLabel(scroll, text="", font=("Arial", 12))
        self.msg.pack(anchor="w", pady=(0, 6))

        # Save button
        ctk.CTkButton(
            scroll, text="💾  Save Profile", height=44, corner_radius=10,
            fg_color=btn_fg, hover_color=btn_hov,
            font=("Arial", 14, "bold"), command=self.save_profile
        ).pack(fill="x")

    def save_profile(self):
        data = {key: entry.get().strip() for key, entry in self.entries.items()}
        update_user(self.username, data)
        self.msg.configure(text="✅ Profile saved successfully!", text_color="#4dff88")
        self.after(2500, lambda: self.msg.configure(text=""))