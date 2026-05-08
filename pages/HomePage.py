import customtkinter as ctk
from database import get_user

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, username, switch_to_login, on_theme_change, theme="dark"):
        bg = "#0a1628" if theme == "dark" else "#f0f4f8"
        super().__init__(parent, fg_color=bg)
        self.username = username
        self.switch_to_login = switch_to_login
        self.on_theme_change = on_theme_change
        self.theme = theme
        self.current_page = None
        self.content_frame = None
        self.build_ui()

    def build_ui(self):
        dark = self.theme == "dark"
        sidebar_bg = "#0d1f3c" if dark else "#dceeff"
        main_bg    = "#0a1628" if dark else "#f0f4f8"
        top_bg     = "#0d1f3c" if dark else "#dceeff"
        logo_col   = "#4da6ff" if dark else "#1565c0"
        nav_col    = "#a0c4ff" if dark else "#1565c0"
        sub_col    = "#3a6090" if dark else "#5a8ab0"

        # ── Sidebar ────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, fg_color=sidebar_bg, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="💙 FinTrack",
                     font=("Arial", 20, "bold"), text_color=logo_col).pack(pady=(30, 4))
        ctk.CTkLabel(self.sidebar, text="Finance Manager",
                     font=("Arial", 11), text_color=sub_col).pack(pady=(0, 30))

        nav_items = [
            ("🏠  Dashboard", "dashboard"),
            ("👤  Profile",   "profile"),
            ("📈  Chart",     "chart"),
            ("🏦  Bank",      "bank"),
            ("⚙️  Settings",  "settings"),
            ("ℹ️  Info",      "info"),
        ]

        self.nav_buttons = {}
        for label, key in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                height=44, corner_radius=10,
                fg_color="transparent", hover_color="#1a3560" if dark else "#b0d0f0",
                text_color=nav_col, font=("Arial", 14),
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(padx=14, fill="x", pady=3)
            self.nav_buttons[key] = btn

        ctk.CTkFrame(self.sidebar,
                     fg_color="#1a3560" if dark else "#90bce0", height=1).pack(
            fill="x", padx=14, pady=20)

        ctk.CTkButton(
            self.sidebar, text="🚪  Log Out", anchor="w",
            height=40, corner_radius=10,
            fg_color="transparent", hover_color="#3d1a1a",
            text_color="#ff6b6b", font=("Arial", 13),
            command=self.switch_to_login
        ).pack(padx=14, fill="x")

        # ── Main area ──────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=main_bg)
        right.pack(side="left", fill="both", expand=True)

        # Topbar
        topbar = ctk.CTkFrame(right, fg_color=top_bg, height=60, corner_radius=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        self.page_title = ctk.CTkLabel(
            topbar, text="Dashboard",
            font=("Arial", 17, "bold"), text_color=logo_col)
        self.page_title.pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(topbar, text=f"👤 {self.username}",
                     font=("Arial", 13), text_color=sub_col).pack(side="right", padx=24)

        # Content frame
        self.content_frame = ctk.CTkFrame(right, fg_color=main_bg)
        self.content_frame.pack(fill="both", expand=True)

        self.show_page("dashboard")

    def show_page(self, key):
        # Highlight nav
        for k, btn in self.nav_buttons.items():
            dark = self.theme == "dark"
            btn.configure(fg_color="#1a3d6e" if k == key and dark
                          else "#90bce0" if k == key
                          else "transparent")

        # Clear content
        for w in self.content_frame.winfo_children():
            w.destroy()

        titles = {
            "dashboard": "Dashboard",
            "profile":   "My Profile",
            "chart":     "Chart",
            "bank":      "Bank",
            "settings":  "Settings",
            "info":      "Info",
        }
        self.page_title.configure(text=titles.get(key, key.title()))

        if key == "dashboard":
            self._build_dashboard(self.content_frame)
        elif key == "profile":
            from pages.ProfilePage import ProfilePage
            ProfilePage(self.content_frame, self.username, self.theme).pack(fill="both", expand=True)
        elif key == "settings":
            from pages.SettingsPage import SettingsPage
            SettingsPage(self.content_frame, self.username,
                         on_theme_change=self.on_theme_change,
                         theme=self.theme).pack(fill="both", expand=True)
        elif key == "info":
            from pages.InfoPage import InfoPage
            InfoPage(self.content_frame, self.username, self.theme).pack(fill="both", expand=True)
        elif key in ("chart", "bank"):
            self._build_placeholder(self.content_frame, key)

    def _build_dashboard(self, parent):
        dark = self.theme == "dark"
        bg       = "#0a1628" if dark else "#f0f4f8"
        card1_bg = "#0f2f6e" if dark else "#dceeff"
        border   = "#1e4080" if dark else "#c0d4f0"
        sub_col  = "#6b9fd4" if dark else "#4a7aaa"

        user = get_user(self.username) or {}
        balance  = user.get("balance", 0.0)
        income   = user.get("income", 0.0)
        expenses = user.get("expenses", 0.0)

        scroll = ctk.CTkScrollableFrame(parent, fg_color=bg)
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        # Balance
        bal = ctk.CTkFrame(scroll, fg_color=card1_bg, corner_radius=18,
                           border_width=1, border_color=border, height=140)
        bal.pack(fill="x", pady=(0, 18))
        bal.pack_propagate(False)
        ctk.CTkLabel(bal, text="Total Balance",
                     font=("Arial", 14), text_color=sub_col).place(x=28, y=24)
        ctk.CTkLabel(bal, text=f"${balance:,.2f}",
                     font=("Arial", 42, "bold"),
                     text_color="white" if dark else "#0d3d7a").place(x=28, y=52)
        ctk.CTkLabel(bal, text="💳", font=("Arial", 44)).place(relx=0.88, y=38)

        # Income / Expenses
        row = ctk.CTkFrame(scroll, fg_color="transparent")
        row.pack(fill="x", pady=(0, 18))

        inc = ctk.CTkFrame(row, fg_color="#0a2e1a" if dark else "#d4f4e2",
                           corner_radius=16,
                           border_width=1, border_color="#1a5c30" if dark else "#6dba90",
                           height=110)
        inc.pack(side="left", fill="both", expand=True, padx=(0, 10))
        inc.pack_propagate(False)
        ctk.CTkLabel(inc, text="Monthly Income",
                     font=("Arial", 13),
                     text_color="#4daa70" if dark else "#1a6a40").place(x=20, y=18)
        ctk.CTkLabel(inc, text=f"+ ${income:,.2f}",
                     font=("Arial", 26, "bold"),
                     text_color="#4dff88" if dark else "#0a8a40").place(x=20, y=46)
        ctk.CTkLabel(inc, text="📥", font=("Arial", 30)).place(relx=0.8, y=32)

        exp = ctk.CTkFrame(row, fg_color="#2e0a0a" if dark else "#fde8e8",
                           corner_radius=16,
                           border_width=1, border_color="#7a2020" if dark else "#e08080",
                           height=110)
        exp.pack(side="left", fill="both", expand=True, padx=(10, 0))
        exp.pack_propagate(False)
        ctk.CTkLabel(exp, text="Monthly Expenses",
                     font=("Arial", 13),
                     text_color="#d47070" if dark else "#a02020").place(x=20, y=18)
        ctk.CTkLabel(exp, text=f"- ${expenses:,.2f}",
                     font=("Arial", 26, "bold"),
                     text_color="#ff6b6b" if dark else "#c0202020").place(x=20, y=46)
        ctk.CTkLabel(exp, text="📤", font=("Arial", 30)).place(relx=0.8, y=32)

        # Quick stats
        ctk.CTkLabel(scroll, text="Quick Overview",
                     font=("Arial", 16, "bold"),
                     text_color="#4da6ff" if dark else "#1565c0").pack(anchor="w", pady=(6, 10))

        stats_row = ctk.CTkFrame(scroll, fg_color="transparent")
        stats_row.pack(fill="x")
        stats = [
            ("📊", "Net Savings", f"${max(income - expenses, 0):,.2f}", "#1a3d5c" if dark else "#d0eaff", "#5bc0eb"),
            ("📅", "This Month",  "May 2026",   "#1a1a3d" if dark else "#e8e0ff", "#a78bfa"),
            ("🔔", "Alerts",      "No alerts",  "#1a2e1a" if dark else "#d4f4e2", "#4daa70"),
        ]
        for icon, title, val, bg2, col in stats:
            c = ctk.CTkFrame(stats_row, fg_color=bg2, corner_radius=14,
                             border_width=1, border_color=col, height=90)
            c.pack(side="left", fill="both", expand=True, padx=5)
            c.pack_propagate(False)
            ctk.CTkLabel(c, text=f"{icon} {title}",
                         font=("Arial", 12), text_color=col).place(x=16, y=14)
            ctk.CTkLabel(c, text=val, font=("Arial", 18, "bold"),
                         text_color="white" if dark else "#1a1a2e").place(x=16, y=42)

    def _build_placeholder(self, parent, key):
        dark = self.theme == "dark"
        bg = "#0a1628" if dark else "#f0f4f8"
        ctk.CTkLabel(parent,
                     text=f"🚧  {key.title()} — Coming Soon",
                     font=("Arial", 22, "bold"),
                     text_color="#4da6ff" if dark else "#1565c0").pack(expand=True)