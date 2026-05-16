import customtkinter as ctk
from pages.LoginPage import LoginPage
from pages.RegisterPage import RegisterPage
from pages.HomePage import HomePage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FinTrack — Finance Manager")
        self.geometry("1100x700")
        self.minsize(960, 620)
        self.theme = "dark"
        self._apply_theme()
        self.current_frame = None
        self.show_login()

    def _apply_theme(self):
        # Always keep CTk in dark mode — we handle all colours manually.
        # Switching CTk to "light" overrides our custom hex colours and turns
        # transparent frames white, which is the root cause of the white-screen bug.
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#0a1628" if self.theme == "dark" else "#eef2f8")

    def clear(self):
        if self.current_frame:
            self.current_frame.destroy()

    def on_theme_change(self, theme, username=None):
        self.theme = theme
        self._apply_theme()
        if username:
            self.show_home(username)

    def show_login(self):
        self.clear()
        self.current_frame = LoginPage(
            self,
            switch_to_register=self.show_register,
            switch_to_home=self.show_home,
            theme=self.theme
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.clear()
        self.current_frame = RegisterPage(
            self,
            switch_to_login=self.show_login,
            theme=self.theme
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_home(self, username):
        self.clear()
        self.current_frame = HomePage(
            self,
            username=username,
            switch_to_login=self.show_login,
            on_theme_change=lambda t: self.on_theme_change(t, username),
            theme=self.theme
        )
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()