import customtkinter as ctk
from database import get_user, update_user

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, username, on_theme_change, theme="dark"):
        bg = "#0a1628" if theme == "dark" else "#f0f4f8"
        super().__init__(parent, fg_color=bg)
        self.username = username
        self.theme = theme
        self.on_theme_change = on_theme_change
        self.account_visible = False
        self.build_ui()

    def build_ui(self):
        dark = self.theme == "dark"
        bg        = "#0a1628" if dark else "#f0f4f8"
        card_bg   = "#0f2044" if dark else "#ffffff"
        border    = "#1e4080" if dark else "#c0d4f0"
        title_col = "#4da6ff" if dark else "#1565c0"
        label_col = "#a0c4ff" if dark else "#1565c0"
        text_col  = "white"   if dark else "#1a1a2e"
        sub_col   = "#6b8cba" if dark else "#5a7a9a"
        entry_bg  = "#0a1e3d" if dark else "#e8f0fe"
        entry_brd = "#1e4080" if dark else "#90b4e0"
        btn_fg    = "#1565c0"
        btn_hov   = "#1976d2"

        self.configure(fg_color=bg)

        scroll = ctk.CTkScrollableFrame(self, fg_color=bg)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(scroll, text="⚙️  Settings",
                     font=("Arial", 22, "bold"), text_color=title_col).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(scroll, text="Manage your account and preferences",
                     font=("Arial", 13), text_color=sub_col).pack(anchor="w", pady=(0, 20))

        user = get_user(self.username) or {}

        # ── Theme card ──────────────────────────────────────────
        self._section(scroll, card_bg, border, label_col, sub_col, "🎨  Appearance")

        theme_card = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=18,
                                  border_width=1, border_color=border)
        theme_card.pack(fill="x", pady=(0, 18))

        theme_inner = ctk.CTkFrame(theme_card, fg_color="transparent")
        theme_inner.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(theme_inner, text="Color Theme",
                     font=("Arial", 13, "bold"), text_color=label_col).pack(side="left")

        self.theme_var = ctk.StringVar(value=self.theme)

        btn_frame = ctk.CTkFrame(theme_inner, fg_color="transparent")
        btn_frame.pack(side="right")

        dark_btn = ctk.CTkButton(
            btn_frame, text="🌙 Dark", width=100, height=36, corner_radius=10,
            fg_color="#1565c0" if dark else "#c8daf5",
            hover_color="#1976d2", text_color="white" if dark else "#1565c0",
            font=("Arial", 13, "bold"),
            command=lambda: self.apply_theme("dark")
        )
        dark_btn.pack(side="left", padx=(0, 8))

        light_btn = ctk.CTkButton(
            btn_frame, text="☀️ Light", width=100, height=36, corner_radius=10,
            fg_color="#1565c0" if not dark else "#0a2e5c",
            hover_color="#1976d2", text_color="white",
            font=("Arial", 13, "bold"),
            command=lambda: self.apply_theme("light")
        )
        light_btn.pack(side="left")

        # ── Change password card ────────────────────────────────
        self._section(scroll, card_bg, border, label_col, sub_col, "🔒  Security")

        pwd_card = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=18,
                                border_width=1, border_color=border)
        pwd_card.pack(fill="x", pady=(0, 18))

        for label, attr, placeholder in [
            ("New Username",       "new_username_entry", "Enter new username"),
            ("Current Password",   "cur_pwd_entry",      "Enter current password"),
            ("New Password",       "new_pwd_entry",      "Enter new password"),
            ("Confirm Password",   "conf_pwd_entry",     "Confirm new password"),
        ]:
            row = ctk.CTkFrame(pwd_card, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=(14, 0))
            ctk.CTkLabel(row, text=label, font=("Arial", 13, "bold"),
                         text_color=label_col, width=160, anchor="w").pack(side="left")
            show = "•" if "Password" in label else None
            e = ctk.CTkEntry(
                row, placeholder_text=placeholder,
                height=40, corner_radius=10, show=show or "",
                fg_color=entry_bg, border_color=entry_brd,
                text_color=text_col, font=("Arial", 13)
            )
            e.pack(side="left", fill="x", expand=True)
            setattr(self, attr, e)

        self.pwd_msg = ctk.CTkLabel(pwd_card, text="", font=("Arial", 12))
        self.pwd_msg.pack(anchor="w", padx=30, pady=(8, 0))

        ctk.CTkButton(
            pwd_card, text="🔄  Update Credentials", height=42, corner_radius=10,
            fg_color=btn_fg, hover_color=btn_hov,
            font=("Arial", 13, "bold"), command=self.update_credentials
        ).pack(padx=30, fill="x", pady=(10, 20))

        # ── Account number card ─────────────────────────────────
        self._section(scroll, card_bg, border, label_col, sub_col, "🏦  Bank Account")

        acc_card = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=18,
                                border_width=1, border_color=border)
        acc_card.pack(fill="x", pady=(0, 18))

        acc_inner = ctk.CTkFrame(acc_card, fg_color="transparent")
        acc_inner.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(acc_inner, text="Account Number",
                     font=("Arial", 13, "bold"), text_color=label_col).pack(anchor="w")

        acc_num = user.get("account_number", "")
        self.acc_display_var = ctk.StringVar(value=self._mask(acc_num))

        display_row = ctk.CTkFrame(acc_card, fg_color="transparent")
        display_row.pack(fill="x", padx=30, pady=(0, 10))

        self.acc_label = ctk.CTkLabel(
            display_row,
            text=self._mask(acc_num) if acc_num else "No account number set",
            font=("Courier", 18, "bold"), text_color=text_col
        )
        self.acc_label.pack(side="left")

        self.toggle_btn = ctk.CTkButton(
            display_row, text="👁 Show", width=80, height=32, corner_radius=8,
            fg_color="#0a2e5c", hover_color="#0d3d7a",
            text_color="#4da6ff", font=("Arial", 12, "bold"),
            command=self.toggle_account
        )
        self.toggle_btn.pack(side="left", padx=(16, 0))

        self._acc_number_raw = acc_num

        # Change account number
        new_acc_row = ctk.CTkFrame(acc_card, fg_color="transparent")
        new_acc_row.pack(fill="x", padx=30, pady=(0, 8))
        ctk.CTkLabel(new_acc_row, text="New Account Number",
                     font=("Arial", 13, "bold"), text_color=label_col,
                     width=200, anchor="w").pack(side="left")
        self.new_acc_entry = ctk.CTkEntry(
            new_acc_row, placeholder_text="Enter new account number",
            height=40, corner_radius=10,
            fg_color=entry_bg, border_color=entry_brd,
            text_color=text_col, font=("Arial", 13)
        )
        self.new_acc_entry.pack(side="left", fill="x", expand=True)

        self.acc_msg = ctk.CTkLabel(acc_card, text="", font=("Arial", 12))
        self.acc_msg.pack(anchor="w", padx=30)

        ctk.CTkButton(
            acc_card, text="💾  Save Account Number", height=42, corner_radius=10,
            fg_color=btn_fg, hover_color=btn_hov,
            font=("Arial", 13, "bold"), command=self.save_account
        ).pack(padx=30, fill="x", pady=(8, 20))

    def _section(self, parent, card_bg, border, label_col, sub_col, title):
        ctk.CTkLabel(parent, text=title,
                     font=("Arial", 15, "bold"), text_color=label_col).pack(
            anchor="w", pady=(10, 6))

    def _mask(self, number):
        if not number:
            return ""
        number = str(number)
        if len(number) <= 4:
            return number
        return "*" * (len(number) - 4) + number[-4:]

    def toggle_account(self):
        self.account_visible = not self.account_visible
        if self.account_visible:
            self.acc_label.configure(
                text=self._acc_number_raw if self._acc_number_raw else "Not set")
            self.toggle_btn.configure(text="🙈 Hide")
        else:
            self.acc_label.configure(
                text=self._mask(self._acc_number_raw) if self._acc_number_raw else "Not set")
            self.toggle_btn.configure(text="👁 Show")

    def save_account(self):
        new_num = self.new_acc_entry.get().strip()
        if not new_num:
            self.acc_msg.configure(text="⚠ Please enter an account number", text_color="#ff5555")
            return
        if not new_num.isdigit():
            self.acc_msg.configure(text="⚠ Only digits allowed", text_color="#ff5555")
            return
        update_user(self.username, {"account_number": new_num})
        self._acc_number_raw = new_num
        self.account_visible = False
        self.acc_label.configure(text=self._mask(new_num))
        self.toggle_btn.configure(text="👁 Show")
        self.new_acc_entry.delete(0, "end")
        self.acc_msg.configure(text="✅ Account number saved!", text_color="#4dff88")
        self.after(2500, lambda: self.acc_msg.configure(text=""))

    def update_credentials(self):
        from database import load_users, save_users
        new_username = self.new_username_entry.get().strip()
        cur_pwd      = self.cur_pwd_entry.get().strip()
        new_pwd      = self.new_pwd_entry.get().strip()
        conf_pwd     = self.conf_pwd_entry.get().strip()

        users = load_users()
        user  = users.get(self.username, {})

        if cur_pwd and cur_pwd != user.get("password", ""):
            self.pwd_msg.configure(text="⚠ Current password is incorrect", text_color="#ff5555")
            return

        if new_pwd:
            if len(new_pwd) < 4:
                self.pwd_msg.configure(text="⚠ Password must be at least 4 characters", text_color="#ff5555")
                return
            if new_pwd != conf_pwd:
                self.pwd_msg.configure(text="⚠ Passwords do not match", text_color="#ff5555")
                return
            users[self.username]["password"] = new_pwd
            save_users(users)

        if new_username and new_username != self.username:
            if new_username in users:
                self.pwd_msg.configure(text="⚠ Username already taken", text_color="#ff5555")
                return
            users[new_username] = users.pop(self.username)
            save_users(users)
            self.username = new_username

        self.pwd_msg.configure(text="✅ Credentials updated!", text_color="#4dff88")
        for e in [self.new_username_entry, self.cur_pwd_entry,
                  self.new_pwd_entry, self.conf_pwd_entry]:
            e.delete(0, "end")
        self.after(2500, lambda: self.pwd_msg.configure(text=""))

    def apply_theme(self, theme):
        self.on_theme_change(theme)