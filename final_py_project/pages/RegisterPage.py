import customtkinter as ctk
from database import register_user

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, switch_to_login, theme="dark"):
        bg = "#0a1628" if theme == "dark" else "#f0f4f8"
        super().__init__(parent, fg_color=bg)
        self.switch_to_login = switch_to_login
        self.build_ui()

    def build_ui(self):
        card = ctk.CTkFrame(self, fg_color="#0f2044", corner_radius=20,
                            border_width=1, border_color="#1e4080")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.38, relheight=0.78)

        ctk.CTkLabel(card, text="✨", font=("Arial", 44)).pack(pady=(35, 4))
        ctk.CTkLabel(card, text="Create Account",
                     font=("Arial", 26, "bold"), text_color="#4da6ff").pack()
        ctk.CTkLabel(card, text="Join us today — it's free!",
                     font=("Arial", 13), text_color="#6b8cba").pack(pady=(2, 22))

        # Username
        ctk.CTkLabel(card, text="Username", font=("Arial", 13, "bold"),
                     text_color="#a0c4ff", anchor="w").pack(padx=40, fill="x")
        self.username_entry = ctk.CTkEntry(
            card, placeholder_text="Choose a username",
            height=42, corner_radius=10,
            fg_color="#0a1e3d", border_color="#1e4080",
            text_color="white", font=("Arial", 13)
        )
        self.username_entry.pack(padx=40, fill="x", pady=(4, 12))

        # Password
        ctk.CTkLabel(card, text="Password", font=("Arial", 13, "bold"),
                     text_color="#a0c4ff", anchor="w").pack(padx=40, fill="x")
        self.password_entry = ctk.CTkEntry(
            card, placeholder_text="Create a password",
            show="•", height=42, corner_radius=10,
            fg_color="#0a1e3d", border_color="#1e4080",
            text_color="white", font=("Arial", 13)
        )
        self.password_entry.pack(padx=40, fill="x", pady=(4, 12))

        # Confirm password
        ctk.CTkLabel(card, text="Confirm Password", font=("Arial", 13, "bold"),
                     text_color="#a0c4ff", anchor="w").pack(padx=40, fill="x")
        self.confirm_entry = ctk.CTkEntry(
            card, placeholder_text="Repeat your password",
            show="•", height=42, corner_radius=10,
            fg_color="#0a1e3d", border_color="#1e4080",
            text_color="white", font=("Arial", 13)
        )
        self.confirm_entry.pack(padx=40, fill="x", pady=(4, 6))

        # Error / success
        self.msg_label = ctk.CTkLabel(card, text="", font=("Arial", 12),
                                      text_color="#ff5555")
        self.msg_label.pack(pady=2)

        # Register button
        ctk.CTkButton(
            card, text="Create Account", height=44, corner_radius=10,
            fg_color="#1565c0", hover_color="#1976d2",
            font=("Arial", 14, "bold"), command=self.handle_register
        ).pack(padx=40, fill="x", pady=(8, 12))

        ctk.CTkLabel(card, text="─────────  or  ─────────",
                     text_color="#2a4a7a", font=("Arial", 11)).pack()

        back_frame = ctk.CTkFrame(card, fg_color="transparent")
        back_frame.pack(pady=(10, 28))
        ctk.CTkLabel(back_frame, text="Already have an account?",
                     text_color="#6b8cba", font=("Arial", 12)).pack(side="left")
        ctk.CTkButton(
            back_frame, text=" Sign In", fg_color="transparent",
            hover_color="#0f2044", text_color="#4da6ff",
            font=("Arial", 12, "bold"), width=70, height=28,
            command=self.switch_to_login
        ).pack(side="left")

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not username or not password or not confirm:
            self.msg_label.configure(text="⚠ Please fill in all fields", text_color="#ff5555")
            return
        if len(password) < 4:
            self.msg_label.configure(text="⚠ Password must be at least 4 characters", text_color="#ff5555")
            return
        if password != confirm:
            self.msg_label.configure(text="⚠ Passwords do not match", text_color="#ff5555")
            return

        success, msg = register_user(username, password)
        if success:
            self.msg_label.configure(text="✅ Account created! Redirecting...", text_color="#4dff88")
            self.after(1200, self.switch_to_login)
        else:
            self.msg_label.configure(text=f"⚠ {msg}", text_color="#ff5555")