import customtkinter as ctk
from database import get_user, add_income

INCOME_SOURCES = ["Salary", "Freelance", "Investment", "Business", "Gift", "Other"]

# Green shades for income entries
INC_COLOR = "#4dff88"
INC_COLOR_L = "#0a8a40"


class BankPage(ctk.CTkFrame):
    def __init__(self, parent, username, theme="dark"):
        dark = theme == "dark"
        bg = "#0a1628" if dark else "#eef2f8"
        super().__init__(parent, fg_color=bg)
        self.username = username
        self.theme = theme
        self.dark = dark
        self.build_ui()

    # ─────────────────────────────────── UI BUILD ────────────────────────────
    def build_ui(self):
        d = self.dark
        bg      = "#0a1628" if d else "#eef2f8"
        card_bg = "#0f2044" if d else "#ffffff"
        border  = "#1e4080" if d else "#c8d8f0"
        t_col   = "#4da6ff" if d else "#1565c0"
        lbl_col = "#a0c4ff" if d else "#1565c0"
        txt_col = "white"   if d else "#1a1a2e"
        sub_col = "#6b8cba" if d else "#4a6a8a"
        ent_bg  = "#0a1e3d" if d else "#e4eeff"
        ent_brd = "#1e4080" if d else "#90b4e0"

        self.configure(fg_color=bg)

        scroll = ctk.CTkScrollableFrame(self, fg_color=bg)
        scroll.pack(fill="both", expand=True, padx=24, pady=16)

        # ── Page title ────────────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="🏦  Bank & Balance",
                     font=("Arial", 22, "bold"), text_color=t_col).pack(
            anchor="w", pady=(0, 2))
        ctk.CTkLabel(scroll, text="Track your income and monitor your balance",
                     font=("Arial", 13), text_color=sub_col).pack(
            anchor="w", pady=(0, 18))

        user = get_user(self.username) or {}
        balance  = user.get("balance",  0.0)
        income   = user.get("income",   0.0)
        expenses = user.get("expenses", 0.0)

        # ── Balance hero card ─────────────────────────────────────────────────
        hero = ctk.CTkFrame(scroll,
                            fg_color="#0f2f6e" if d else "#dceeff",
                            corner_radius=18, border_width=1,
                            border_color="#1e4080" if d else "#b0cef0",
                            height=130)
        hero.pack(fill="x", pady=(0, 14))
        hero.pack_propagate(False)

        ctk.CTkLabel(hero, text="Current Balance",
                     font=("Arial", 14), text_color=sub_col).place(x=28, y=20)
        bal_col = (INC_COLOR if d else INC_COLOR_L) if balance >= 0 \
            else ("#ff6b6b" if d else "#c02020")
        self.balance_lbl = ctk.CTkLabel(
            hero, text=f"${balance:,.2f}",
            font=("Arial", 38, "bold"), text_color=bal_col)
        self.balance_lbl.place(x=28, y=48)
        ctk.CTkLabel(hero, text="💰", font=("Arial", 40)).place(relx=0.86, y=36)

        # ── Income / Expenses mini-cards ──────────────────────────────────────
        row = ctk.CTkFrame(scroll, fg_color="transparent")
        row.pack(fill="x", pady=(0, 14))

        inc_c = ctk.CTkFrame(row, fg_color="#0a2e1a" if d else "#d4f4e2",
                             corner_radius=14, border_width=1,
                             border_color="#1a5c30" if d else "#6dba90",
                             height=90)
        inc_c.pack(side="left", fill="both", expand=True, padx=(0, 8))
        inc_c.pack_propagate(False)
        ctk.CTkLabel(inc_c, text="Total Income",
                     font=("Arial", 12),
                     text_color="#4daa70" if d else "#1a6a40").place(x=16, y=14)
        self.income_lbl = ctk.CTkLabel(inc_c,
                                       text=f"${income:,.2f}",
                                       font=("Arial", 22, "bold"),
                                       text_color=INC_COLOR if d else INC_COLOR_L)
        self.income_lbl.place(x=16, y=40)
        ctk.CTkLabel(inc_c, text="📥", font=("Arial", 26)).place(relx=0.8, y=26)

        exp_c = ctk.CTkFrame(row, fg_color="#2e0a0a" if d else "#fde8e8",
                             corner_radius=14, border_width=1,
                             border_color="#7a2020" if d else "#e08080",
                             height=90)
        exp_c.pack(side="left", fill="both", expand=True, padx=(8, 0))
        exp_c.pack_propagate(False)
        ctk.CTkLabel(exp_c, text="Total Expenses",
                     font=("Arial", 12),
                     text_color="#d47070" if d else "#a02020").place(x=16, y=14)
        ctk.CTkLabel(exp_c, text=f"${expenses:,.2f}",
                     font=("Arial", 22, "bold"),
                     text_color="#ff6b6b").place(x=16, y=40)
        ctk.CTkLabel(exp_c, text="📤", font=("Arial", 26)).place(relx=0.8, y=26)

        # ── Bank info card (from profile) ─────────────────────────────────────
        bank_name    = user.get("bank_name", "")
        account_num  = user.get("account_number", "")
        if bank_name or account_num:
            bcard = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=16,
                                 border_width=1, border_color=border)
            bcard.pack(fill="x", pady=(0, 14))

            ctk.CTkLabel(bcard, text="🏦  Bank Details",
                         font=("Arial", 14, "bold"), text_color=t_col).pack(
                anchor="w", padx=20, pady=(14, 6))

            for label, value in [("Bank", bank_name or "—"),
                                  ("Account", self._mask(account_num) if account_num else "—")]:
                r = ctk.CTkFrame(bcard, fg_color="transparent")
                r.pack(fill="x", padx=20, pady=3)
                ctk.CTkLabel(r, text=label,
                             font=("Arial", 12, "bold"), text_color=lbl_col,
                             width=80, anchor="w").pack(side="left")
                ctk.CTkLabel(r, text=value,
                             font=("Courier", 13), text_color=txt_col).pack(side="left")

            ctk.CTkFrame(bcard, fg_color="transparent", height=10).pack()

        # ── Add Income section ────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="➕  Add Income",
                     font=("Arial", 15, "bold"), text_color=t_col).pack(
            anchor="w", pady=(4, 6))

        form = ctk.CTkFrame(scroll, fg_color=card_bg, corner_radius=16,
                            border_width=1, border_color=border)
        form.pack(fill="x", pady=(0, 14))

        fi = ctk.CTkFrame(form, fg_color="transparent")
        fi.pack(fill="x", padx=20, pady=16)

        # Amount + Source side-by-side
        top_row = ctk.CTkFrame(fi, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 8))

        left_f = ctk.CTkFrame(top_row, fg_color="transparent")
        left_f.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkLabel(left_f, text="Amount ($)",
                     font=("Arial", 12, "bold"), text_color=lbl_col).pack(anchor="w")
        self.inc_amount = ctk.CTkEntry(
            left_f, placeholder_text="0.00",
            height=38, corner_radius=8,
            fg_color=ent_bg, border_color=ent_brd,
            text_color=txt_col, font=("Arial", 14))
        self.inc_amount.pack(fill="x", pady=(4, 0))

        right_f = ctk.CTkFrame(top_row, fg_color="transparent")
        right_f.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(right_f, text="Source",
                     font=("Arial", 12, "bold"), text_color=lbl_col).pack(anchor="w")
        self.src_var = ctk.StringVar(value="Salary")
        ctk.CTkOptionMenu(
            right_f, values=INCOME_SOURCES, variable=self.src_var,
            height=38, corner_radius=8,
            fg_color=ent_bg, button_color="#1565c0",
            button_hover_color="#1976d2",
            dropdown_fg_color="#0d1f3c" if d else "#f0f6ff",
            text_color=txt_col, font=("Arial", 12)
        ).pack(fill="x", pady=(4, 0))

        ctk.CTkLabel(fi, text="Note (optional)",
                     font=("Arial", 12, "bold"), text_color=lbl_col).pack(anchor="w")
        self.inc_note = ctk.CTkEntry(
            fi, placeholder_text="e.g. June salary, client payment…",
            height=34, corner_radius=8,
            fg_color=ent_bg, border_color=ent_brd,
            text_color=txt_col, font=("Arial", 12))
        self.inc_note.pack(fill="x", pady=(4, 8))

        self.inc_msg = ctk.CTkLabel(fi, text="", font=("Arial", 11))
        self.inc_msg.pack(anchor="w")

        ctk.CTkButton(fi, text="💰  Add Income",
                      height=40, corner_radius=8,
                      fg_color="#1565c0", hover_color="#1976d2",
                      font=("Arial", 13, "bold"),
                      command=self._add_income).pack(fill="x", pady=(4, 0))

        # ── Income history ────────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="📋  Income History",
                     font=("Arial", 15, "bold"), text_color=t_col).pack(
            anchor="w", pady=(12, 6))

        self.inc_list = ctk.CTkScrollableFrame(
            scroll, fg_color=card_bg,
            corner_radius=14, border_width=1, border_color=border,
            height=220)
        self.inc_list.pack(fill="x", pady=(0, 16))

        self._refresh_income_list()

    # ─────────────────────────────────── HELPERS ─────────────────────────────
    @staticmethod
    def _mask(number):
        s = str(number)
        if len(s) <= 4:
            return s
        return "•" * (len(s) - 4) + s[-4:]

    def _add_income(self):
        amount_str = self.inc_amount.get().strip()
        source     = self.src_var.get()
        note       = self.inc_note.get().strip()

        if not amount_str:
            self.inc_msg.configure(text="⚠ Enter an amount", text_color="#ff5555")
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.inc_msg.configure(text="⚠ Invalid amount", text_color="#ff5555")
            return

        if add_income(self.username, amount, source, note):
            self.inc_msg.configure(
                text=f"✅  +${amount:.2f} recorded!", text_color="#4dff88")
            self.inc_amount.delete(0, "end")
            self.inc_note.delete(0, "end")
            self.after(2500, lambda: self.inc_msg.configure(text=""))
            self._refresh_display()
            self._refresh_income_list()

    def _refresh_display(self):
        d = self.dark
        user    = get_user(self.username) or {}
        balance = user.get("balance", 0.0)
        income  = user.get("income",  0.0)
        bal_col = (INC_COLOR if d else INC_COLOR_L) if balance >= 0 \
            else ("#ff6b6b" if d else "#c02020")
        self.balance_lbl.configure(text=f"${balance:,.2f}", text_color=bal_col)
        self.income_lbl.configure(text=f"${income:,.2f}")

    def _refresh_income_list(self):
        for w in self.inc_list.winfo_children():
            w.destroy()

        d       = self.dark
        txt_col = "white"   if d else "#1a1a2e"
        sub_col = "#6b8cba" if d else "#4a6a8a"

        user    = get_user(self.username) or {}
        history = list(reversed(user.get("income_history", [])))

        if not history:
            ctk.CTkLabel(self.inc_list, text="No income recorded yet 🌱",
                         font=("Arial", 12), text_color=sub_col).pack(pady=16)
            return

        for t in history[:30]:
            row = ctk.CTkFrame(self.inc_list,
                               fg_color="#0a1e3d" if d else "#eef4ff",
                               corner_radius=8)
            row.pack(fill="x", pady=2, padx=4)

            bar = ctk.CTkFrame(row,
                               fg_color=INC_COLOR if d else INC_COLOR_L,
                               width=4, corner_radius=2)
            bar.pack(side="left", fill="y")
            bar.pack_propagate(False)

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=8, pady=5)

            lbl = t.get("source", "Income")
            if t.get("note"):
                lbl += f"  •  {t['note']}"
            ctk.CTkLabel(info, text=lbl,
                         font=("Arial", 11, "bold"),
                         text_color=txt_col, anchor="w").pack(anchor="w")
            ctk.CTkLabel(info, text=t.get("date", ""),
                         font=("Arial", 10),
                         text_color=sub_col, anchor="w").pack(anchor="w")

            ctk.CTkLabel(row,
                         text=f"+${t['amount']:,.2f}",
                         font=("Arial", 12, "bold"),
                         text_color=INC_COLOR if d else INC_COLOR_L
                         ).pack(side="right", padx=10)