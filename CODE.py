import os
import sys
import ctypes
import time
import threading
import subprocess
import webbrowser
import winsound
import customtkinter as ctk
from PIL import Image
import pystray


COLOR_MAIN = "#8b2bfa"      # фиолетовый
COLOR_HOVER = "#6e21c9"     # Темно-фиолетовый 
COLOR_BG = "#000000"        # Глубокий черный фон 
COLOR_FRAME = "#0c0514"     # Фон контейнера 
COLOR_BORDER = "#3a1663"    # Имитация свечения
FONT_NAME = "Segoe UI"
TEXT_COLOR = "#ffffff"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()


TOOLS_DIR = resource_path("Tools")
CREATE_NO_WINDOW = 0x08000000
ICON_PATH = os.path.join(TOOLS_DIR, "Proximity.ico")


class CTKTooltip:
    def __init__(self, widget, info_key, app_instance):
        self.widget = widget
        self.info_key = info_key
        self.app = app_instance
        self.tooltip_window = None
        self.id = None
        
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        self.unschedule()
        self.id = self.widget.after(300, self.show_tooltip)

    def leave(self, event=None):
        self.unschedule()
        self.hide_tooltip()

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show_tooltip(self):
        if self.tooltip_window:
            return
            
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        tw.configure(fg_color="#1a1a1a")

        text = LOCALES[self.app.current_lang][self.info_key]

        label = ctk.CTkLabel(tw, text=text, font=(FONT_NAME, 12), 
                             padx=14, pady=10, text_color="#ffffff", fg_color="#1a1a1a", corner_radius=10)
        label.pack()

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


LOCALES = {
    "EN": {
        "lang_btn": "RU",
        "splash_welcome": "Welcome {name}",
        "splash_loading": "Loading system resources...",
        "splash_check": "Checking Windows Registry...",
        "splash_search": "Searching for Happ service...",
        "splash_sync": "Synchronizing DPI drivers...",
        "splash_fin": "Preparing interface...",
        "header": "PROXIMITY",
        "sw_happ": "Happ VPN",
        "sw_tg": "TG Proxy",
        "sw_zprtx": "ZPRTX YouTube + Discord + Roblox",
        "btn_happ": "DOWNLOAD AND INSTALL HAPP",
        "btn_pdf": "Happ Configuration Guide",
        "btn_about": "WEBSITE",
        
        "info_happ": "Advanced routing and configuration tool for traffic management.\nBEFORE LAUNCHING OR INSTALLING\nPLEASE READ THE GUIDE !!!",
        "info_tg": "Local MTProto proxy for Telegram Desktop\nDeveloped by Flowseal",
        "info_zprtx": "A hybrid build merging configurations from Lux1de and visual style from Flowseal. The entire utility is streamlined into exactly 1 working strategy: general (ALT) for YouTube, Discord, and Roblox.\nDeveloped by Shprot",
        
        "warn_title": "⚠️ WARNING",
        "warn_msg_bold": "Are you sure you want to exit the application?",
        "warn_msg_norm": "Active toggles will be disabled after restarting.\nIt is highly recommended to turn off all toggles before exiting.",
        "btn_yes": "Yes",
        "btn_no": "No",
        "tray_show": "Open",
        "tray_exit": "Exit"
    },

    "RU": {
        "lang_btn": "EN",
        "splash_welcome": "Welcome {name}",
        "splash_loading": "Загрузка системных ресурсов...",
        "splash_check": "Проверка реестра Windows...",
        "splash_search": "Поиск службы Happ...",
        "splash_sync": "Синхронизация драйверов DPI...",
        "splash_fin": "Подготовка интерфейса...",
        "header": "PROXIMITY",
        "sw_happ": "Happ vpn",
        "sw_tg": "TG Прокси",
        "sw_zprtx": "ZPRTX Ютуб + Дискорд + Роблокс",
        "btn_happ": "СКАЧАТЬ И УСТАНОВИТЬ HAPP",
        "btn_pdf": "Инструкция по настройке HAPP",
        "btn_about": "САЙТ",
        
        "info_happ": "продвинутый инструмент маршрутизации и конфигураций для управления трафиком.\nПЕРЕД ТЕМ КАК ЗАПУСТИТЬ ИЛИ УСТАНОВИТЬ\nПРОЧТИТЕ ИНСТРУКЦИЮ !!!",
        "info_tg": "Локальный MTProto-прокси для Telegram Desktop\nРазработчик - Flowseal",
        "info_zprtx": "Сборка, объединившая в себе версию от Lux1de и версию от Flowseal. Вся утилита сведена к 1 стратегии general (ALT) для YouTube, Discord, Roblox.\nРазработчик - Shprot",
        
        "warn_title": "⚠️ ВНИМАНИЕ",
        "warn_msg_bold": "Вы уверены, что хотите закрыть приложение?",
        "warn_msg_norm": "Включенные ползунки будут отключены после перезапуска,\nРекомендую отключить все ползунки перед выходом.",
        "btn_yes": "Да",
        "btn_no": "Нет",
        "tray_show": "открыть",
        "tray_exit": "выход"
    }
}


def play_ui_sound(sound_type):
    sound_map = {
        'click': "click.wav",
        'switch': "toggle.wav",
        'startup': "welcome.wav"
    }
    s_path = resource_path(os.path.join("sounds", sound_map.get(sound_type, "")))
    if os.path.exists(s_path):
        threading.Thread(target=winsound.PlaySound, args=(s_path, winsound.SND_FILENAME), daemon=True).start()


class CustomWarningWindow(ctk.CTkToplevel):
    def __init__(self, parent, lang, callback_yes, callback_no):
        super().__init__(parent)
        self.title(LOCALES[lang]["warn_title"])
        self.geometry("480x280")
        self.configure(fg_color=COLOR_BG) 
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        if os.path.exists(ICON_PATH):
            self.after(200, lambda: self.iconbitmap(ICON_PATH))

        #
        self.inner_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=20, border_color=COLOR_BORDER, border_width=1)
        self.inner_frame.pack(fill="both", expand=True, padx=15, pady=15)

        lbl_bold = ctk.CTkLabel(self.inner_frame, text=LOCALES[lang]["warn_msg_bold"], font=(FONT_NAME, 16, "bold"), text_color="#ffcc00")
        lbl_bold.pack(pady=(20, 10))

        lbl_norm = ctk.CTkLabel(self.inner_frame, text=LOCALES[lang]["warn_msg_norm"], font=(FONT_NAME, 13), justify="center", text_color="#cccccc")
        lbl_norm.pack(pady=(0, 20))

        btn_yes = ctk.CTkButton(self.inner_frame, text=LOCALES[lang]["btn_yes"], fg_color=COLOR_MAIN, hover_color=COLOR_HOVER, corner_radius=12, font=(FONT_NAME, 12, "bold"), command=callback_yes)
        btn_yes.pack(pady=5, fill="x", padx=40)

        btn_no = ctk.CTkButton(self.inner_frame, text=LOCALES[lang]["btn_no"], fg_color="#333333", hover_color="#555555", corner_radius=12, text_color="#ffffff", font=(FONT_NAME, 12), command=callback_no)
        btn_no.pack(pady=5, fill="x", padx=40)


class ProximityApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.current_lang = "RU"
        self.title("Proximity")
        self.geometry("460x650") 
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)
        
        if os.path.exists(ICON_PATH):
            self.after(200, lambda: self.iconbitmap(ICON_PATH))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Unmap>", self.on_minimize)

        self.var_happ = ctk.StringVar(value="off")
        self.var_tg = ctk.StringVar(value="off")
        self.var_zprtx = ctk.StringVar(value="off")
        
        self.open_buttons = {} 

        self.tray_icon = None
        self.withdraw() 
        self.show_splash()

    def show_splash(self):
        splash = ctk.CTkToplevel(self)
        splash.geometry("400x250")
        splash.overrideredirect(True)
        splash.configure(fg_color=COLOR_BG)
        
        if os.path.exists(ICON_PATH):
            splash.after(200, lambda: splash.iconbitmap(ICON_PATH))
            
        screen_width = splash.winfo_screenwidth()
        screen_height = splash.winfo_screenheight()
        x = (screen_width // 2) - 200
        y = (screen_height // 2) - 125
        splash.geometry(f"400x250+{x}+{y}")

        # 
        splash_frame = ctk.CTkFrame(splash, fg_color=COLOR_FRAME, corner_radius=24, border_color=COLOR_BORDER, border_width=1)
        splash_frame.pack(fill="both", expand=True, padx=10, pady=10)

        user_name = os.getlogin().title()
        welcome_text = LOCALES[self.current_lang]["splash_welcome"].format(name=user_name)
        
        lbl_welcome = ctk.CTkLabel(splash_frame, text=welcome_text, font=(FONT_NAME, 26, "bold"), text_color="#ffffff")
        lbl_welcome.pack(pady=(50, 20))
        
        progress = ctk.CTkProgressBar(splash_frame, orientation="horizontal", width=280, progress_color=COLOR_MAIN, fg_color="#1a1a1a")
        progress.set(0)
        progress.pack(pady=10)
        
        status_label = ctk.CTkLabel(splash_frame, text=LOCALES[self.current_lang]["splash_loading"], font=(FONT_NAME, 12), text_color="#aaaaaa")
        status_label.pack()

        play_ui_sound('startup')

        def load():
            for i in range(1, 101):
                time.sleep(0.03)
                progress.set(i / 100)
                if i == 20: status_label.configure(text=LOCALES[self.current_lang]["splash_check"])
                if i == 45: status_label.configure(text=LOCALES[self.current_lang]["splash_search"])
                if i == 70: status_label.configure(text=LOCALES[self.current_lang]["splash_sync"])
                if i == 90: status_label.configure(text=LOCALES[self.current_lang]["splash_fin"])
            
            splash.destroy()
            self.deiconify()
            self.setup_main_ui()

        threading.Thread(target=load).start()

    def setup_main_ui(self):
        
        self.main_container = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=24, border_width=1, border_color=COLOR_BORDER)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.btn_lang = ctk.CTkButton(self.main_container, text=LOCALES[self.current_lang]["lang_btn"], width=40, height=30, 
                                      fg_color="#1a1a1a", hover_color="#2a2a2a", corner_radius=10, text_color="#ffffff", font=(FONT_NAME, 12, "bold"), 
                                      command=lambda: [play_ui_sound('click'), self.toggle_language()])
        self.btn_lang.place(relx=0.94, rely=0.03, anchor="ne")

        self.header = ctk.CTkLabel(self.main_container, text=LOCALES[self.current_lang]["header"], font=(FONT_NAME, 34, "bold"), text_color=COLOR_MAIN)
        self.header.pack(pady=(40, 15))

        self.scroll_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.scroll_frame.pack(pady=10, padx=20, fill="both")

        self.sw_happ_widget = self.create_switch(LOCALES[self.current_lang]["sw_happ"], self.toggle_happ, self.var_happ, "info_happ", "happ")
        self.sw_tg_widget = self.create_switch(LOCALES[self.current_lang]["sw_tg"], self.toggle_tg, self.var_tg, "info_tg", "tg")
        self.sw_zprtx_widget = self.create_switch(LOCALES[self.current_lang]["sw_zprtx"], self.toggle_zprtx, self.var_zprtx, "info_zprtx", "zprtx")

        self.btn_install_happ = self.create_button(LOCALES[self.current_lang]["btn_happ"], self.install_happ, is_accent=True)
        self.btn_inst = self.create_button(LOCALES[self.current_lang]["btn_pdf"], self.open_instructions)
        self.btn_about = self.create_button(LOCALES[self.current_lang]["btn_about"], self.open_about)

        self.footer = ctk.CTkLabel(self.main_container, text="by Shprot", font=(FONT_NAME, 11, "italic"), text_color="#555555")
        self.footer.pack(side="bottom", pady=15)

    def create_switch(self, text, command, var, info_key, id_key):
        row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row.pack(pady=12, fill="x")

        sw = ctk.CTkSwitch(
            row, text=text, command=lambda: [play_ui_sound('switch'), command(var)],
            variable=var, onvalue="on", offvalue="off",
            progress_color=COLOR_MAIN, font=(FONT_NAME, 14, "bold"), text_color="#ffffff",
            button_color="#ffffff", button_hover_color="#e0e0e0"
        )
        sw.pack(side="left")

        
        btn_info = ctk.CTkButton(
            row, text="?", width=28, height=28, corner_radius=14,
            fg_color="#1a1a1a", hover_color=COLOR_MAIN, text_color="#ffffff", font=(FONT_NAME, 12, "bold")
        )
        btn_info.pack(side="right", padx=(5, 0))
        CTKTooltip(btn_info, info_key, self) 
        
        
        btn_open = ctk.CTkButton(
            row, text="↗", width=28, height=28, corner_radius=14,
            state="disabled", fg_color="#111111", text_color="#555555", hover_color=COLOR_HOVER, font=(FONT_NAME, 14, "bold"),
            command=lambda: self.open_app_window(id_key)
        )
        btn_open.pack(side="right")
        self.open_buttons[id_key] = btn_open
        
        return sw

    def create_button(self, text, command, is_accent=False):
        f_color = COLOR_MAIN if is_accent else "#1a1a1a"
        h_color = COLOR_HOVER if is_accent else "#2a2a2a"
        
        btn = ctk.CTkButton(
            self.main_container, text=text, command=lambda: [play_ui_sound('click'), command()],
            fg_color=f_color, hover_color=h_color, corner_radius=14, text_color="#ffffff",
            font=(FONT_NAME, 13, "bold"), height=46
        )
        btn.pack(pady=8, padx=30, fill="x")
        return btn




    def open_app_window(self, id_key):
        play_ui_sound('click')
        if id_key == "happ":
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            search_paths = [
                os.path.join(desktop, "Happ.lnk", "Happ.exe"),
                os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Happ", "Happ.exe"),
                os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Happ", "Happ.exe"),
                os.path.join(os.environ.get("LocalAppData", ""), "Happ", "Happ.exe")
            ]
            target = next((p for p in search_paths if os.path.exists(p)), None)
            if target: os.startfile(target)
            
        elif id_key == "tg":
            webbrowser.open("https://github.com/Flowseal/tg-ws-proxy")
            
        elif id_key == "zprtx":
            webbrowser.open("https://github.com/shprttx")



    def on_minimize(self, event):
        if str(self.state()) == 'iconic':
            self.withdraw()
            threading.Thread(target=self.create_tray_icon, daemon=True).start()

    def create_tray_icon(self):
        if self.tray_icon is not None:
            return

        image = Image.open(ICON_PATH).convert("RGBA") if os.path.exists(ICON_PATH) else Image.new('RGB', (64, 64), color='purple')
        
        menu = pystray.Menu(
            pystray.MenuItem(LOCALES[self.current_lang]["tray_show"], self.show_from_tray, default=True),
            pystray.MenuItem(LOCALES[self.current_lang]["tray_exit"], self.exit_from_tray)
        )
        self.tray_icon = pystray.Icon("Proximity", image, "Proximity", menu)
        self.tray_icon.run()

    def show_from_tray(self, icon, item):
        self.tray_icon.stop()
        self.tray_icon = None
        self.after(0, self.restore_window)

    def restore_window(self):
        self.deiconify()
        self.state('normal')

    def exit_from_tray(self, icon, item):
        self.tray_icon.stop()
        self.tray_icon = None
        self.after(0, self.on_closing)



    def toggle_language(self):
        self.current_lang = "RU" if self.current_lang == "EN" else "EN"
        l = LOCALES[self.current_lang]
        
        self.btn_lang.configure(text=l["lang_btn"])
        self.header.configure(text=l["header"])
        self.sw_happ_widget.configure(text=l["sw_happ"])
        self.sw_tg_widget.configure(text=l["sw_tg"])
        self.sw_zprtx_widget.configure(text=l["sw_zprtx"])
        self.btn_install_happ.configure(text=l["btn_happ"])
        self.btn_inst.configure(text=l["btn_pdf"])
        self.btn_about.configure(text=l["btn_about"])


    def on_closing(self):
        if "on" in (self.var_happ.get(), self.var_tg.get(), self.var_zprtx.get()):
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            CustomWarningWindow(self, self.current_lang, self.force_close, self.close_dialog)
        else:
            self.force_close()

    def close_dialog(self):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                widget.destroy()

    def force_close(self):
        if self.var_happ.get() == "on": self.toggle_happ(ctk.StringVar(value="off"))
        if self.var_tg.get() == "on": self.toggle_tg(ctk.StringVar(value="off"))
        if self.var_zprtx.get() == "on": self.toggle_zprtx(ctk.StringVar(value="off"))
        self.quit()


    def install_happ(self):
        install_path = os.path.join(TOOLS_DIR, "Happinstallation", "setup-Happ.x64.exe")
        if os.path.exists(install_path): os.startfile(install_path)

    def open_instructions(self):
        pdf_path = os.path.join(TOOLS_DIR, "INST.pdf")
        if os.path.exists(pdf_path): os.startfile(pdf_path)

    def open_about(self):
        webbrowser.open("https://freeweb-376.pages.dev")

    def toggle_zprtx(self, var):
        z_dir = os.path.abspath(os.path.join(TOOLS_DIR, "Zprtx"))
        main_bat = "MAIN.bat"
        full_path = os.path.join(z_dir, main_bat)

        if var.get() == "on":
            
            self.open_buttons["zprtx"].configure(state="normal", fg_color=COLOR_MAIN, text_color="#ffffff")
            if os.path.exists(full_path):
                try:
                    subprocess.Popen(f'start "" /d "{z_dir}" "{main_bat}"', shell=True)
                except Exception:
                    var.set("off")
            else:
                var.set("off")
        else:
            
            self.open_buttons["zprtx"].configure(state="disabled", fg_color="#111111", text_color="#555555")
            try:
                subprocess.run("taskkill /IM winws.exe /F", shell=True, creationflags=CREATE_NO_WINDOW)
                subprocess.run("taskkill /IM cmd.exe /F", shell=True, creationflags=CREATE_NO_WINDOW)
            except: pass

    def toggle_happ(self, var):
        if var.get() == "on":
            self.open_buttons["happ"].configure(state="normal", fg_color=COLOR_MAIN, text_color="#ffffff")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            search_paths = [
                os.path.join(desktop, "Happ.lnk"),
                os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Happ", "Happ.exe"),
                os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Happ", "Happ.exe"),
                os.path.join(os.environ.get("LocalAppData", ""), "Happ", "Happ.exe")
            ]
            target = next((p for p in search_paths if os.path.exists(p)), None)
            if target: 
                os.startfile(target)
            else: 
                var.set("off")
        else:
            self.open_buttons["happ"].configure(state="disabled", fg_color="#111111", text_color="#555555")
            subprocess.run("taskkill /IM Happ.exe /F", shell=True, creationflags=CREATE_NO_WINDOW)

    def toggle_tg(self, var):
        t_path = os.path.join(TOOLS_DIR, "TG", "TgWsProxy_windows.exe")
        if var.get() == "on":
            self.open_buttons["tg"].configure(state="normal", fg_color=COLOR_MAIN, text_color="#ffffff")
            if os.path.exists(t_path): subprocess.Popen(t_path, creationflags=CREATE_NO_WINDOW)
            else: var.set("off")
        else:
            self.open_buttons["tg"].configure(state="disabled", fg_color="#111111", text_color="#555555")
            subprocess.run("taskkill /IM TgWsProxy_windows.exe /F", shell=True, creationflags=CREATE_NO_WINDOW)

if __name__ == "__main__":
    app = ProximityApp()
    app.mainloop()
