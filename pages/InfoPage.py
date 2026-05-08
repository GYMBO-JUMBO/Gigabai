import customtkinter as ctk

class InfoPage(ctk.CTkFrame):
    def __init__(self, parent, username, theme="dark"):
        bg = "#0a1628" if theme == "dark" else "#f0f4f8"
        super().__init__(parent, fg_color=bg)
        self.theme = theme
        self.build_ui()

    def build_ui(self):
        dark = self.theme == "dark"
        bg        = "#0a1628" if dark else "#f0f4f8"
        card_bg   = "#0f2044" if dark else "#ffffff"
        border    = "#1e4080" if dark else "#c0d4f0"
        title_col = "#4da6ff" if dark else "#1565c0"
        text_col  = "#d0e8ff" if dark else "#1a2e4a"
        sub_col   = "#6b8cba" if dark else "#5a7a9a"
        acc_col   = "#a0c4ff" if dark else "#1565c0"

        self.configure(fg_color=bg)

        scroll = ctk.CTkScrollableFrame(self, fg_color=bg)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(scroll, text="ℹ️  About FinTrack",
                     font=("Arial", 22, "bold"), text_color=title_col).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(scroll, text="Everything you need to know",
                     font=("Arial", 13), text_color=sub_col).pack(anchor="w", pady=(0, 20))

        # About card
        card = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=18,
                            border_width=1, border_color=border)
        card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(card, text="💙 What is FinTrack?",
                     font=("Arial", 16, "bold"), text_color=title_col).pack(
            anchor="w", padx=30, pady=(24, 10))

        about_text = (
            "FinTrack is a personal finance management application designed to help "
            "you take full control of your financial life. With FinTrack you can easily "
            "track your income and expenses, monitor your account balance in real time, "
            "and get a clear picture of your spending habits.\n\n"
            "Our goal is to make financial tracking simple, beautiful, and accessible "
            "for everyone — no complicated spreadsheets, no confusion. Just clean, "
            "intuitive tools that help you make smarter financial decisions every day."
        )
        ctk.CTkLabel(card, text=about_text, font=("Arial", 13),
                     text_color=text_col, wraplength=700, justify="left").pack(
            anchor="w", padx=30, pady=(0, 24))

        # Features card
        feat_card = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=18,
                                 border_width=1, border_color=border)
        feat_card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(feat_card, text="✨ Key Features",
                     font=("Arial", 16, "bold"), text_color=title_col).pack(
            anchor="w", padx=30, pady=(24, 12))

        features = [
            ("💰", "Balance Tracking",    "See your total balance updated in real time."),
            ("📈", "Income & Expenses",   "Monitor monthly income and spending clearly."),
            ("🔒", "Secure Accounts",     "Your data is stored locally and stays private."),
            ("🎨", "Custom Themes",       "Switch between dark and light mode anytime."),
            ("👤", "Personal Profile",    "Store your personal and banking information."),
        ]

        for icon, title, desc in features:
            row = ctk.CTkFrame(feat_card, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=(0, 14))
            ctk.CTkLabel(row, text=icon, font=("Arial", 26), width=40).pack(side="left", padx=(0, 14))
            col = ctk.CTkFrame(row, fg_color="transparent")
            col.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(col, text=title, font=("Arial", 13, "bold"),
                         text_color=acc_col, anchor="w").pack(anchor="w")
            ctk.CTkLabel(col, text=desc, font=("Arial", 12),
                         text_color=text_col, anchor="w").pack(anchor="w")

        ctk.CTkFrame(feat_card, fg_color="transparent", height=10).pack()

        # Authors card
        auth_card = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=18,
                                 border_width=1, border_color=border)
        auth_card.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(auth_card, text="👨‍💻 Developers",
                     font=("Arial", 16, "bold"), text_color=title_col).pack(
            anchor="w", padx=30, pady=(24, 14))

        ctk.CTkLabel(auth_card,
                     text="This application was created as a university project by two students:",
                     font=("Arial", 13), text_color=text_col).pack(anchor="w", padx=30)

        for name, role in [
            ("Korostylev Dmitriy",  "Backend & Database"),
            ("Mansur Murodyan",     "UI & Frontend"),
        ]:
            dev = ctk.CTkFrame(auth_card, fg_color="#0a2044" if dark else "#e0ecff",
                               corner_radius=12)
            dev.pack(fill="x", padx=30, pady=(10, 0))
            ctk.CTkLabel(dev, text=f"🎓  {name}",
                         font=("Arial", 14, "bold"), text_color=acc_col).pack(
                anchor="w", padx=20, pady=(12, 2))
            ctk.CTkLabel(dev, text=role,
                         font=("Arial", 12), text_color=sub_col).pack(
                anchor="w", padx=20, pady=(0, 12))

        ctk.CTkLabel(auth_card,
                     text="Group: SE-2513  |  University Project  |  2026",
                     font=("Arial", 12), text_color=sub_col).pack(pady=(16, 24))