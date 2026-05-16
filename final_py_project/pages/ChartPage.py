import customtkinter as ctk
import tkinter as tk
from database import get_user, add_category_expense, delete_transaction

SLICE_COLORS = [
    "#4da6ff", "#ff6b6b", "#4dff88", "#ffd700", "#ff9f43",
    "#a78bfa", "#34d399", "#f472b6", "#60a5fa", "#fb923c",
    "#e879f9", "#2dd4bf",
]

DEFAULT_CATEGORIES = ["Food", "Transport", "Entertainment", "Health", "Shopping", "Bills", "Other"]


class ChartPage(ctk.CTkFrame):
    def __init__(self, parent, username, theme="dark"):
        dark = theme == "dark"
        bg = "#0a1628" if dark else "#eef2f8"
        super().__init__(parent, fg_color=bg)
        self.username = username
        self.theme = theme
        self.dark = dark
        self.card_bg = "#0f2044" if dark else "#ffffff"   # ← Добавила сюда
        self.build_ui()

    def build_ui(self):
        d = self.dark
        bg = "#0a1628" if d else "#eef2f8"
        border = "#1e4080" if d else "#c8d8f0"
        t_col = "#4da6ff" if d else "#1565c0"

        self.configure(fg_color=bg)

        main_wrap = ctk.CTkFrame(self, fg_color=bg)
        main_wrap.pack(fill="both", expand=True, padx=18, pady=14)

        main_wrap.grid_columnconfigure(0, weight=3)
        main_wrap.grid_columnconfigure(1, weight=1)
        main_wrap.grid_rowconfigure(0, weight=1)

        # Левая панель
        left = ctk.CTkFrame(main_wrap, fg_color=self.card_bg, corner_radius=18,
                            border_width=1, border_color=border)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Правая панель
        right = ctk.CTkScrollableFrame(main_wrap, fg_color=bg, width=340)
        right.grid(row=0, column=1, sticky="nsew")

        # ── Левая часть (график) ─────────────────────
        ctk.CTkLabel(left, text="📊  Expenses by Category",
                     font=("Arial", 16, "bold"), text_color=t_col).pack(pady=(18, 8))

        self.canvas = tk.Canvas(left, width=360, height=280,
                                bg=self.card_bg, highlightthickness=0)
        self.canvas.pack(pady=8, padx=20)

        self.legend_frame = ctk.CTkFrame(left, fg_color="transparent")
        self.legend_frame.pack(fill="x", padx=22, pady=8)

        sumrow = ctk.CTkFrame(left, fg_color="#0a2044" if d else "#e0ecff",
                              corner_radius=12)
        sumrow.pack(fill="x", padx=18, pady=(4, 18))

        user = get_user(self.username) or {}
        total_exp = user.get("expenses", 0.0)
        self.total_lbl = ctk.CTkLabel(
            sumrow, text=f"📤  Total Expenses: ${total_exp:,.2f}",
            font=("Arial", 13, "bold"), text_color="#ff6b6b" if d else "#b02020"
        )
        self.total_lbl.pack(pady=10)

        self._draw_chart()

        # ── Правая часть ─────────────────────
        self._build_add_form(right)
        self._build_history(right)

    def _category_data(self):
        user = get_user(self.username) or {}
        cats = user.get("categories", {})
        data = {}
        for cat, txns in cats.items():
            total = sum(t.get("amount", 0) for t in txns)
            if total > 0:
                data[cat] = total
        return data

    def _draw_chart(self):
        self.canvas.delete("all")
        for w in self.legend_frame.winfo_children():
            w.destroy()

        d = self.dark
        data = self._category_data()

        if not data:
            self.canvas.create_text(180, 140,
                text="No expenses yet 🌱\nAdd one below! 👇",
                fill="#4da6ff" if d else "#1565c0",
                font=("Arial", 13), justify="center")
            return

        total = sum(data.values())
        cx, cy, r = 180, 140, 110
        start = 90.0

        items = list(data.items())
        for i, (cat, amount) in enumerate(items):
            color = SLICE_COLORS[i % len(SLICE_COLORS)]
            extent = -360.0 * amount / total
            if extent <= -360:
                extent = -359.999

            self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start, extent=extent,
                fill=color, outline=self.card_bg, width=2
            )
            start += extent

        # Donut hole
        ir = 58
        self.canvas.create_oval(cx - ir, cy - ir, cx + ir, cy + ir,
                                fill=self.card_bg, outline="")

        self.canvas.create_text(cx, cy - 10, text="Total",
                                fill="#6b8cba" if d else "#4a6a8a", font=("Arial", 9))
        self.canvas.create_text(cx, cy + 12, text=f"${total:,.0f}",
                                fill="white" if d else "#1a1a2e", font=("Arial", 15, "bold"))

        # Legend
        col_left = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
        col_right = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
        col_left.pack(side="left", fill="x", expand=True, padx=(0, 10))
        col_right.pack(side="left", fill="x", expand=True)

        txt_col = "white" if d else "#1a1a2e"
        for i, (cat, amount) in enumerate(items):
            color = SLICE_COLORS[i % len(SLICE_COLORS)]
            pct = amount / total * 100
            col = col_left if i % 2 == 0 else col_right

            row = ctk.CTkFrame(col, fg_color="transparent")
            row.pack(fill="x", pady=2)

            dot = ctk.CTkFrame(row, fg_color=color, width=10, height=10, corner_radius=5)
            dot.pack(side="left", padx=(0, 6))
            dot.pack_propagate(False)

            ctk.CTkLabel(row, text=cat, font=("Arial", 10, "bold"), text_color=txt_col).pack(side="left")
            ctk.CTkLabel(row, text=f" {pct:.1f}%", font=("Arial", 10),
                         text_color="#6b8cba" if d else "#4a6a8a").pack(side="left")

    def _build_add_form(self, parent):
        d = self.dark
        card_bg = self.card_bg
        ent_bg = "#0a1e3d" if d else "#e4eeff"
        ent_brd = "#1e4080" if d else "#90b4e0"
        lbl_col = "#a0c4ff" if d else "#1565c0"
        txt_col = "white" if d else "#1a1a2e"
        sub_col = "#6b8cba" if d else "#4a6a8a"

        ctk.CTkLabel(parent, text="➕  Add Expense",
                     font=("Arial", 15, "bold"), text_color=lbl_col).pack(anchor="w", pady=(0, 8))

        card = ctk.CTkFrame(parent, fg_color=card_bg, corner_radius=16,
                            border_width=1, border_color=ent_brd)
        card.pack(fill="x", pady=(0, 16))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=14)

        # Category
        ctk.CTkLabel(inner, text="Category", font=("Arial", 12, "bold"), text_color=lbl_col).pack(anchor="w")
        user = get_user(self.username) or {}
        existing = list(user.get("categories", {}).keys())
        all_cats = list(dict.fromkeys(DEFAULT_CATEGORIES + existing))

        self.cat_var = ctk.StringVar(value=all_cats[0])
        self.cat_menu = ctk.CTkOptionMenu(inner, values=all_cats, variable=self.cat_var,
                                          height=36, fg_color=ent_bg, text_color=txt_col)
        self.cat_menu.pack(fill="x", pady=(4, 8))

        ctk.CTkLabel(inner, text="Or create new category", font=("Arial", 11), text_color=sub_col).pack(anchor="w")
        self.custom_entry = ctk.CTkEntry(inner, placeholder_text="e.g. Gym, Coffee...", 
                                         height=34, fg_color=ent_bg, border_color=ent_brd, text_color=txt_col)
        self.custom_entry.pack(fill="x", pady=(4, 8))

        ctk.CTkLabel(inner, text="Amount ($)", font=("Arial", 12, "bold"), text_color=lbl_col).pack(anchor="w")
        self.amount_entry = ctk.CTkEntry(inner, placeholder_text="0.00", height=36,
                                         fg_color=ent_bg, border_color=ent_brd, text_color=txt_col)
        self.amount_entry.pack(fill="x", pady=(4, 8))

        ctk.CTkLabel(inner, text="Note (optional)", font=("Arial", 12, "bold"), text_color=lbl_col).pack(anchor="w")
        self.note_entry = ctk.CTkEntry(inner, placeholder_text="lunch, taxi...", height=34,
                                       fg_color=ent_bg, border_color=ent_brd, text_color=txt_col)
        self.note_entry.pack(fill="x", pady=(4, 8))

        self.add_msg = ctk.CTkLabel(inner, text="", font=("Arial", 11))
        self.add_msg.pack(anchor="w")

        ctk.CTkButton(inner, text="➕  Add Expense", height=40,
                      fg_color="#1565c0", hover_color="#1976d2",
                      font=("Arial", 13, "bold"), command=self._add_expense).pack(fill="x", pady=(8, 0))

    def _build_history(self, parent):
        d = self.dark
        card_bg = self.card_bg
        t_col = "#4da6ff" if d else "#1565c0"
        ent_bg = "#0a1e3d" if d else "#e4eeff"

        hdr = ctk.CTkFrame(parent, fg_color="transparent")
        hdr.pack(fill="x", pady=(10, 6))
        ctk.CTkLabel(hdr, text="📋  Expense History",
                     font=("Arial", 15, "bold"), text_color=t_col).pack(side="left")
        ctk.CTkButton(hdr, text="🔄", width=32, height=28,
                      command=self._refresh_history).pack(side="right")

        user = get_user(self.username) or {}
        existing = list(user.get("categories", {}).keys())
        all_cats = list(dict.fromkeys(DEFAULT_CATEGORIES + existing))

        self.filter_var = ctk.StringVar(value="All")
        ctk.CTkOptionMenu(parent, values=["All"] + all_cats, variable=self.filter_var,
                          command=lambda _: self._refresh_history()).pack(fill="x", pady=(0, 8))

        self.hist_list = ctk.CTkScrollableFrame(parent, fg_color=card_bg,
                                                corner_radius=14, border_width=1,
                                                border_color="#1e4080" if d else "#c8d8f0", height=260)
        self.hist_list.pack(fill="x", pady=(0, 10))

        self._refresh_history()

    # ──────────────────────────────── ACTIONS ────────────────────────────────
    def _add_expense(self):
        custom = self.custom_entry.get().strip()
        category = custom if custom else self.cat_var.get()
        amount_str = self.amount_entry.get().strip()
        note = self.note_entry.get().strip()

        if not amount_str:
            self.add_msg.configure(text="⚠ Enter an amount", text_color="#ff5555")
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.add_msg.configure(text="⚠ Invalid amount", text_color="#ff5555")
            return

        if add_category_expense(self.username, category, amount, note):
            self.add_msg.configure(text=f"✅ ${amount:.2f} → {category}", text_color="#4dff88")
            self.amount_entry.delete(0, "end")
            self.note_entry.delete(0, "end")
            self.custom_entry.delete(0, "end")

            self.after(1800, lambda: self.add_msg.configure(text=""))
            self._draw_chart()
            self._refresh_history()
            self._refresh_dropdowns()

            user = get_user(self.username) or {}
            self.total_lbl.configure(text=f"📤  Total Expenses: ${user.get('expenses', 0.0):,.2f}")

    def _refresh_dropdowns(self):
        user = get_user(self.username) or {}
        existing = list(user.get("categories", {}).keys())
        all_cats = list(dict.fromkeys(DEFAULT_CATEGORIES + existing))
        self.cat_menu.configure(values=all_cats)

    def _refresh_history(self):
        for w in self.hist_list.winfo_children():
            w.destroy()

        d = self.dark
        txt_col = "white" if d else "#1a1a2e"
        sub_col = "#6b8cba" if d else "#4a6a8a"

        user = get_user(self.username) or {}
        cats = user.get("categories", {})
        fcat = self.filter_var.get()

        all_txns = []
        for cat, txns in cats.items():
            if fcat != "All" and cat != fcat:
                continue
            for t in txns:
                all_txns.append((cat, t))

        all_txns.sort(key=lambda x: x[1].get("date", ""), reverse=True)

        if not all_txns:
            ctk.CTkLabel(self.hist_list, text="No transactions yet 🌱",
                         font=("Arial", 12), text_color=sub_col).pack(pady=40)
            return

        cat_keys = list(cats.keys())
        for cat, t in all_txns[:40]:
            cat_idx = cat_keys.index(cat) if cat in cat_keys else 0
            color = SLICE_COLORS[cat_idx % len(SLICE_COLORS)]

            row = ctk.CTkFrame(self.hist_list, fg_color="#0a1e3d" if d else "#eef4ff",
                               corner_radius=8)
            row.pack(fill="x", pady=2, padx=4)

            bar = ctk.CTkFrame(row, fg_color=color, width=4, corner_radius=2)
            bar.pack(side="left", fill="y")
            bar.pack_propagate(False)

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=8, pady=5)

            lbl = cat + (f" • {t['note']}" if t.get("note") else "")
            ctk.CTkLabel(info, text=lbl, font=("Arial", 11, "bold"),
                         text_color=txt_col, anchor="w").pack(anchor="w")
            ctk.CTkLabel(info, text=t.get("date", ""), font=("Arial", 10),
                         text_color=sub_col, anchor="w").pack(anchor="w")

            right_side = ctk.CTkFrame(row, fg_color="transparent")
            right_side.pack(side="right", padx=6)

            ctk.CTkLabel(right_side, text=f"-${t['amount']:,.2f}",
                         font=("Arial", 12, "bold"), text_color="#ff6b6b").pack(side="top")

            def make_delete(c=cat, dt=t.get("date", "")):
                def _del():
                    delete_transaction(self.username, c, dt)
                    self._draw_chart()
                    self._refresh_history()
                    u = get_user(self.username) or {}
                    self.total_lbl.configure(text=f"📤  Total Expenses: ${u.get('expenses', 0.0):,.2f}")
                return _del

            ctk.CTkButton(right_side, text="🗑", width=28, height=20,
                          fg_color="#3d1a1a" if d else "#fde8e8",
                          hover_color="#7a2020" if d else "#f4b0b0",
                          text_color="#ff6b6b", command=make_delete()).pack(side="top", pady=(2, 0))