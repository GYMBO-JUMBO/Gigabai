import customtkinter as ctk
from database import get_user
from datetime import datetime


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, username, switch_to_login, on_theme_change, theme="dark"):
        dark = theme == "dark"
        bg = "#0a1628" if dark else "#eef2f8"
        super().__init__(parent, fg_color=bg)
        self.username = username
        self.switch_to_login = switch_to_login
        self.on_theme_change = on_theme_change
        self.theme = theme
        self.current_page = None
        self.content_frame = None
        self.build_ui()

    # ─────────────────────────────────── MAIN SHELL ──────────────────────────
    def build_ui(self):
        d = self.theme == "dark"
        sidebar_bg = "#0d1f3c" if d else "#d8eaff"
        main_bg    = "#0a1628" if d else "#eef2f8"
        top_bg     = "#0d1f3c" if d else "#d8eaff"
        logo_col   = "#4da6ff" if d else "#1565c0"
        nav_col    = "#a0c4ff" if d else "#1565c0"
        sub_col    = "#3a6090" if d else "#4a6a9a"

        # ── Sidebar ───────────────────────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, fg_color=sidebar_bg, width=210, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="💙  FinTrack",
                     font=("Arial", 21, "bold"), text_color=logo_col).pack(pady=(30, 2))
        ctk.CTkLabel(self.sidebar, text="Finance Manager",
                     font=("Arial", 11), text_color=sub_col).pack(pady=(0, 28))

        nav_items = [
            ("🏠  Dashboard",  "dashboard"),
            ("👤  Profile",    "profile"),
            ("📊  Statistics", "chart"),
            ("🏦  Bank",       "bank"),
            ("⚙️  Settings",   "settings"),
            ("ℹ️  Info",       "info"),
        ]

        self.nav_buttons = {}
        for label, key in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                height=44, corner_radius=10,
                fg_color="transparent",
                hover_color="#1a3560" if d else "#b0d0f0",
                text_color=nav_col, font=("Arial", 14),
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(padx=14, fill="x", pady=3)
            self.nav_buttons[key] = btn

        ctk.CTkFrame(self.sidebar,
                     fg_color="#1a3560" if d else "#90bce0",
                     height=1).pack(fill="x", padx=14, pady=18)

        ctk.CTkButton(
            self.sidebar, text="🚪  Log Out", anchor="w",
            height=40, corner_radius=10,
            fg_color="transparent", hover_color="#3d1a1a" if d else "#fde8e8",
            text_color="#ff6b6b", font=("Arial", 13),
            command=self.switch_to_login
        ).pack(padx=14, fill="x")

        # ── Right area ────────────────────────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=main_bg)
        right.pack(side="left", fill="both", expand=True)

        # Top bar
        topbar = ctk.CTkFrame(right, fg_color=top_bg, height=60, corner_radius=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.page_title = ctk.CTkLabel(
            topbar, text="Dashboard",
            font=("Arial", 17, "bold"), text_color=logo_col)
        self.page_title.pack(side="left", padx=24, pady=16)

        ctk.CTkLabel(topbar, text=f"👤  {self.username}",
                     font=("Arial", 13), text_color=sub_col).pack(side="right", padx=24)

        # Content area
        self.content_frame = ctk.CTkFrame(right, fg_color=main_bg)
        self.content_frame.pack(fill="both", expand=True)

        self.show_page("dashboard")

    # ─────────────────────────────────── PAGE ROUTER ─────────────────────────
    def show_page(self, key):
        d = self.theme == "dark"
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color="#1a3d6e" if d else "#90bce0")
            else:
                btn.configure(fg_color="transparent")

        for w in self.content_frame.winfo_children():
            w.destroy()

        titles = {
            "dashboard": "Dashboard",
            "profile":   "My Profile",
            "chart":     "Statistics",
            "bank":      "Bank & Balance",
            "settings":  "Settings",
            "info":      "About FinTrack",
        }
        self.page_title.configure(text=titles.get(key, key.title()))

        if key == "dashboard":
            self._build_dashboard(self.content_frame)
        elif key == "profile":
            from pages.ProfilePage import ProfilePage
            ProfilePage(self.content_frame, self.username, self.theme
                        ).pack(fill="both", expand=True)
        elif key == "chart":
            from pages.ChartPage import ChartPage
            ChartPage(self.content_frame, self.username, self.theme
                      ).pack(fill="both", expand=True)
        elif key == "bank":
            from pages.BankPage import BankPage
            BankPage(self.content_frame, self.username, self.theme
                     ).pack(fill="both", expand=True)
        elif key == "settings":
            from pages.SettingsPage import SettingsPage
            SettingsPage(self.content_frame, self.username,
                         on_theme_change=self.on_theme_change,
                         theme=self.theme).pack(fill="both", expand=True)
        elif key == "info":
            from pages.InfoPage import InfoPage
            InfoPage(self.content_frame, self.username, self.theme
                     ).pack(fill="both", expand=True)

    # ─────────────────────────────────── DASHBOARD ───────────────────────────
    def _build_dashboard(self, parent):
        d = self.theme == "dark"
        bg       = "#0a1628" if d else "#eef2f8"
        card1_bg = "#0f2f6e" if d else "#dceeff"
        border   = "#1e4080" if d else "#c8d8f0"
        sub_col  = "#6b9fd4" if d else "#4a7aaa"
        txt_col  = "white"   if d else "#0d3d7a"

        user     = get_user(self.username) or {}
        balance  = user.get("balance",  0.0)
        income   = user.get("income",   0.0)
        expenses = user.get("expenses", 0.0)
        savings  = max(income - expenses, 0.0)

        scroll = ctk.CTkScrollableFrame(parent, fg_color=bg)
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        # ── Balance hero ──────────────────────────────────────────────────────
        bal = ctk.CTkFrame(scroll, fg_color=card1_bg, corner_radius=18,
                           border_width=1, border_color=border, height=140)
        bal.pack(fill="x", pady=(0, 16))
        bal.pack_propagate(False)

        ctk.CTkLabel(bal, text="Total Balance",
                     font=("Arial", 14), text_color=sub_col).place(x=28, y=22)
        bal_color = ("white" if d else "#0d3d7a") if balance >= 0 else "#ff6b6b"
        ctk.CTkLabel(bal, text=f"${balance:,.2f}",
                     font=("Arial", 42, "bold"),
                     text_color=bal_color).place(x=28, y=50)
        ctk.CTkLabel(bal, text="💳", font=("Arial", 44)).place(relx=0.88, y=38)

        # ── Income / Expenses row ─────────────────────────────────────────────
        row = ctk.CTkFrame(scroll, fg_color="transparent")
        row.pack(fill="x", pady=(0, 16))

        def mini_card(parent, fg, bdr, lbl_c, lbl_t, val_c, val_t, icon, side, pad):
            c = ctk.CTkFrame(parent, fg_color=fg, corner_radius=16,
                             border_width=1, border_color=bdr, height=110)
            c.pack(side=side, fill="both", expand=True, padx=pad)
            c.pack_propagate(False)
            ctk.CTkLabel(c, text=lbl_t, font=("Arial", 13),
                         text_color=lbl_c).place(x=20, y=18)
            ctk.CTkLabel(c, text=val_t, font=("Arial", 26, "bold"),
                         text_color=val_c).place(x=20, y=46)
            ctk.CTkLabel(c, text=icon, font=("Arial", 30)).place(relx=0.8, y=32)

        mini_card(row,
                  "#0a2e1a" if d else "#d4f4e2",
                  "#1a5c30" if d else "#6dba90",
                  "#4daa70" if d else "#1a6a40",
                  "Monthly Income",
                  "#4dff88" if d else "#0a8a40",
                  f"+ ${income:,.2f}",
                  "📥", "left", (0, 10))

        mini_card(row,
                  "#2e0a0a" if d else "#fde8e8",
                  "#7a2020" if d else "#e08080",
                  "#d47070" if d else "#a02020",
                  "Monthly Expenses",
                  "#ff6b6b" if d else "#c02020",
                  f"- ${expenses:,.2f}",
                  "📤", "left", (10, 0))

        # ── Quick overview ────────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="Quick Overview",
                     font=("Arial", 16, "bold"),
                     text_color="#4da6ff" if d else "#1565c0").pack(
            anchor="w", pady=(4, 10))

        stats_row = ctk.CTkFrame(scroll, fg_color="transparent")
        stats_row.pack(fill="x")

        now = datetime.now().strftime("%B %Y")
        cats = user.get("categories", {})
        num_cats = len(cats)
        total_txns = sum(len(v) for v in cats.values())
        inc_hist = user.get("income_history", [])

        stats = [
            ("📊", "Net Savings",  f"${savings:,.2f}",
             "#1a3d5c" if d else "#d0eaff", "#5bc0eb"),
            ("📅", "This Month",   now,
             "#1a1a3d" if d else "#e8e0ff", "#a78bfa"),
            ("🧾", "Transactions", f"{total_txns} logged",
             "#1a2e1a" if d else "#d4f4e2", "#4daa70"),
            ("💰", "Income Entries", f"{len(inc_hist)} recorded",
             "#2e1a0a" if d else "#fff3e0", "#ff9f43"),
        ]
        for icon, title, val, bg2, col in stats:
            c = ctk.CTkFrame(stats_row, fg_color=bg2, corner_radius=14,
                             border_width=1, border_color=col, height=88)
            c.pack(side="left", fill="both", expand=True, padx=4)
            c.pack_propagate(False)
            ctk.CTkLabel(c, text=f"{icon}  {title}",
                         font=("Arial", 11), text_color=col).place(x=14, y=12)
            ctk.CTkLabel(c, text=val,
                         font=("Arial", 17, "bold"),
                         text_color="white" if d else "#1a1a2e").place(x=14, y=40)

        # ── Recent expenses ───────────────────────────────────────────────────
        if cats:
            ctk.CTkLabel(scroll, text="Recent Expenses",
                         font=("Arial", 16, "bold"),
                         text_color="#4da6ff" if d else "#1565c0").pack(
                anchor="w", pady=(18, 8))

            recent_card = ctk.CTkFrame(scroll,
                                       fg_color="#0f2044" if d else "#ffffff",
                                       corner_radius=16, border_width=1,
                                       border_color=border)
            recent_card.pack(fill="x")

            all_txns = []
            for cat, txns in cats.items():
                for t in txns:
                    all_txns.append((cat, t))
            all_txns.sort(key=lambda x: x[1].get("date", ""), reverse=True)

            COLORS = [
                "#4da6ff", "#ff6b6b", "#4dff88", "#ffd700", "#ff9f43",
                "#a78bfa", "#34d399", "#f472b6", "#60a5fa", "#fb923c",
            ]
            cat_keys = list(cats.keys())
            for cat, t in all_txns[:5]:
                ci    = cat_keys.index(cat) if cat in cat_keys else 0
                color = COLORS[ci % len(COLORS)]
                rr    = ctk.CTkFrame(recent_card, fg_color="transparent")
                rr.pack(fill="x", padx=16, pady=4)

                dot = ctk.CTkFrame(rr, fg_color=color,
                                   width=8, height=8, corner_radius=4)
                dot.pack(side="left", padx=(0, 10))
                dot.pack_propagate(False)

                ctk.CTkLabel(rr, text=cat, font=("Arial", 12, "bold"),
                             text_color="white" if d else "#1a1a2e").pack(side="left")
                if t.get("note"):
                    ctk.CTkLabel(rr, text=f"  {t['note']}",
                                 font=("Arial", 12),
                                 text_color=sub_col).pack(side="left")
                ctk.CTkLabel(rr, text=f"-${t['amount']:,.2f}",
                             font=("Arial", 12, "bold"),
                             text_color="#ff6b6b").pack(side="right")

            ctk.CTkFrame(recent_card, fg_color="transparent", height=8).pack()