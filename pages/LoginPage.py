import customtkinter as ctk
from database import login_user

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, switch_to_register, switch_to_home, theme="dark"):
        bg = "#0a1628" if theme == "dark" else "#f0f4f8"
        super().__init__(parent, fg_color=bg)
        self.switch_to_register = switch_to_register
        self.switch_to_home = switch_to_home
        self.build_ui()

    def build_ui(self):
        # Center card
        card = ctk.CTkFrame(self, fg_color="#0f2044", corner_radius=20,
                            border_width=1, border_color="#1e4080")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.38, relheight=0.72)

        # Logo / Title
        ctk.CTkLabel(card, text="💙", font=("Arial", 48)).pack(pady=(40, 5))
        ctk.CTkLabel(card, text="Welcome Back",
                     font=("Arial", 26, "bold"), text_color="#4da6ff").pack()
        ctk.CTkLabel(card, text="Sign in to your account",
                     font=("Arial", 13), text_color="#6b8cba").pack(pady=(2, 25))

        # Username
        ctk.CTkLabel(card, text="Username", font=("Arial", 13, "bold"),
                     text_color="#a0c4ff", anchor="w").pack(padx=40, fill="x")
        self.username_entry = ctk.CTkEntry(
            card, placeholder_text="Enter username",
            height=42, corner_radius=10,
            fg_color="#0a1e3d", border_color="#1e4080",
            text_color="white", font=("Arial", 13)
        )
        self.username_entry.pack(padx=40, fill="x", pady=(4, 14))

        # Password
        ctk.CTkLabel(card, text="Password", font=("Arial", 13, "bold"),
                     text_color="#a0c4ff", anchor="w").pack(padx=40, fill="x")
        self.password_entry = ctk.CTkEntry(
            card, placeholder_text="Enter password",
            show="•", height=42, corner_radius=10,
            fg_color="#0a1e3d", border_color="#1e4080",
            text_color="white", font=("Arial", 13)
        )
        self.password_entry.pack(padx=40, fill="x", pady=(4, 6))

        # Error label
        self.error_label = ctk.CTkLabel(card, text="", text_color="#ff5555",
                                        font=("Arial", 12))
        self.error_label.pack()

        # Login button
        ctk.CTkButton(
            card, text="Sign In", height=44, corner_radius=10,
            fg_color="#1565c0", hover_color="#1976d2",
            font=("Arial", 14, "bold"), command=self.handle_login
        ).pack(padx=40, fill="x", pady=(10, 14))

        # Divider
        ctk.CTkLabel(card, text="─────────  or  ─────────",
                     text_color="#2a4a7a", font=("Arial", 11)).pack()

        # Register link
        reg_frame = ctk.CTkFrame(card, fg_color="transparent")
        reg_frame.pack(pady=(10, 30))
        ctk.CTkLabel(reg_frame, text="Don't have an account?",
                     text_color="#6b8cba", font=("Arial", 12)).pack(side="left")
        ctk.CTkButton(
            reg_frame, text=" Sign Up", fg_color="transparent",
            hover_color="#0f2044", text_color="#4da6ff",
            font=("Arial", 12, "bold"), width=70, height=28,
            command=self.switch_to_register
        ).pack(side="left")

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            self.error_label.configure(text="⚠ Please fill in all fields")
            return
        success, result = login_user(username, password)
        if success:
            self.error_label.configure(text="")
            self.switch_to_home(username)
        else:
            self.error_label.configure(text=f"⚠ {result}")