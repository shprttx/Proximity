import os
import sys
import ctypes
import math
import random
import threading
import subprocess
import webbrowser
import winsound
import urllib.request
import json
import customtkinter as ctk
from PIL import Image
import pystray

#version & urls 

CURRENT_VERSION = "26.06.26"
UPDATE_URL      = "https://raw.githubusercontent.com/shprttx/Proximity/main/update.json"

#design tokens 

COLOR_MAIN      = "#00f2ff"
COLOR_SECONDARY = "#00c8d4"
COLOR_HOVER     = "#0b1c2c"
COLOR_BG        = "#050508"
COLOR_FRAME     = "#0c0d14"
COLOR_BORDER    = "#1b142c"
COLOR_ACCENT    = "#ff0844"
FONT_NAME       = "Segoe UI"

PULSE_COLORS = ["#00f2ff", "#1ae5ff", "#33d8ff", "#4dcaff", "#66bdff", "#4dcaff", "#33d8ff", "#1ae5ff"]

#system

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

TOOLS_DIR        = resource_path("Tools")
CREATE_NO_WINDOW = 0x08000000
ICON_PATH        = os.path.join(TOOLS_DIR, "Proximity.ico")

#helpers

def color_fade(c1, c2, steps):
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    return [
        f"#{int(r1+(r2-r1)*i/(steps-1)):02x}"
        f"{int(g1+(g2-g1)*i/(steps-1)):02x}"
        f"{int(b1+(b2-b1)*i/(steps-1)):02x}"
        for i in range(steps)
    ]

def play_ui_sound(sound_type):
    sound_map = {
        "click":   "click.wav",
        "switch":  "toggle.wav",
        "startup": "welcome.wav",
        "master":  "master.wav",
        "warning": "warning.wav",
    }
    path = resource_path(os.path.join("sounds", sound_map.get(sound_type, "")))
    if os.path.exists(path):
        threading.Thread(target=winsound.PlaySound, args=(path, winsound.SND_FILENAME), daemon=True).start()

#locales

LOCALES = {
    "EN": {
        "lang_btn":        "RU",
        "header":          "PROXIMITY",
        "sw_happ":         "Happ",
        "sw_tg":           "TG Proxy",
        "sw_zprtx":        "YouTube + Discord ZPRTX",
        "sw_warp":         "Cloudflare WARP",
        "btn_installer":   "SETUP WIZARD",
        "btn_pdf":         "Happ + Cloudflare WARP Manual",
        "btn_about":       "GITHUB",
        "installer_title": "SETUP WIZARD",
        "installer_label": "Select what you want to install",
        "installer_happ":  "INSTALL HAPP",
        "installer_warp":  "INSTALL CLOUDFLARE WARP",
        "installer_close": "Close Setup Wizard",
        "info_happ":       "Happ VPN is an advanced routing tool.\n\nDevelopers: Flyfrog LLC\n\nPlease read the instructions\n\nbefore installing!",
        "info_tg":         "Telegram Proxy creates a secure WebSocket tunnel.\n\nDeveloper: Flowseal",
        "info_zprtx":      "ZPRTX is a DPI bypass engine.\n\nDeveloper: shprot\n\nIt modifies packets at the driver level to unblock websites.",
        "info_warp":       "Cloudflare WARP is a utility that combines VPN features with a secure DNS resolver.\n\nIt speeds up website loading and provides access to AI models [Gemini, Claude, GPT, etc.].\n\nDevelopers: Cloudflare, Inc.",
        "warn_title":      "⚠️ WARNING",
        "warn_msg_bold":   "Are you sure you want to close the application?",
        "warn_msg_norm":   "Active toggles will be disabled after restart.\nRe-enabling toggles for an already active service\nmay cause system bugs.",
        "btn_yes":         "Yes",
        "btn_no":          "No",
        "tray_show":       "Open",
        "tray_exit":       "Exit",
        "upd_title":       "UPDATE AVAILABLE",
        "upd_msg":         "A new version of the application is available.\nPlease update to ensure stable performance.\nThe changelog is available on GitHub.",
        "upd_warn":        "NOTE: The website is temporarily unavailable,\nplease use instant download instead.",
        "btn_upd_site":    "Instant Download",
        "btn_upd_gh":      "Changelog",
    },
    "RU": {
        "lang_btn":        "EN",
        "header":          "PROXIMITY",
        "sw_happ":         "Happ",
        "sw_tg":           "TG Прокси",
        "sw_zprtx":        "Ютуб + Дискорд ZPRTX",
        "sw_warp":         "Cloudflare WARP",
        "btn_installer":   "МАСТЕР УСТАНОВКИ",
        "btn_pdf":         "Инструкция Happ + Cloudflare WARP",
        "btn_about":       "GITHUB",
        "installer_title": "МАСТЕР УСТАНОВКИ",
        "installer_label": "Выберите что хотите установить",
        "installer_happ":  "УСТАНОВИТЬ HAPP",
        "installer_warp":  "УСТАНОВИТЬ CLOUDFLARE WARP",
        "installer_close": "Закрыть Мастер установки",
        "info_happ":       "Happ vpn - это продвинутый инструмент маршрутизации.\n\nРазработчики - Flyfrog LLC\n\nПеред тем как установить\n\nпрочтите инструкцию!\n\nТРЕБУЕТСЯ УСТАНОВКА В Мастер установки!",
        "info_tg":         "Telegram Proxy создает защищенный WebSocket туннель\n\nРазработчик - Flowseal",
        "info_zprtx":      "ZPRTX - движок обхода DPI.\n\nРазработчик - shprot\n\nМодифицирует пакеты на уровне драйвера для разблокировки сайтов.",
        "info_warp":       "Cloudflare WARP - утилита объединяющий функции VPN и безопасного DNS-резолвера.\n\nУскоряет загрузку сайтов, дотуп к нейросетям [Gemini, Claude, GPT и др]\n\nРазработчики- Cloudflare, Inc.\n\nТРЕБУЕТСЯ УСТАНОВКА В Мастер установки!",
        "warn_title":      "⚠️ ВНИМАНИЕ",
        "warn_msg_bold":   "Вы уверены, что хотите закрыть приложение?",
        "warn_msg_norm":   "Включенные ползунки будут отключены после перезапуска,\nПовторное включение ползунков уже активного сервиса\nможет привести к возможным багам в системе.",
        "btn_yes":         "Да",
        "btn_no":          " Нет",
        "tray_show":       "Открыть",
        "tray_exit":       "Выход",
        "upd_title":       "ДОСТУПНО ОБНОВЛЕНИЕ",
        "upd_msg":         "Вышло новое обновление приложения.\nПожалуйста, обновитесь для стабильной работы.\nСписок изменений доступен на GitHub.",
        "upd_warn":        "ВНИМАНИЕ: Сайт временно приостановил свою работу,\nвоспользуйтесь мгновенным скачиванием.",
        "btn_upd_site":    "Мгновенное скачивание",
        "btn_upd_gh":      "Список изменений",
    },
}

#bubble

class BubbleBackground(ctk.CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG, highlightthickness=0, **kwargs)
        self.bubbles   = []
        self.animating = False
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.width  = event.width
        self.height = event.height
        if not self.bubbles:
            for _ in range(30):
                self._spawn(init=True)

    def _spawn(self, init=False):
        size  = random.randint(12, 30)
        x     = random.randint(10, max(100, getattr(self, "width",  300) - 10))
        y     = random.randint(10, getattr(self, "height", 500)) if init else getattr(self, "height", 500) + random.randint(10, 60)
        r     = size // 2
        color = random.choice([COLOR_MAIN, COLOR_SECONDARY, "#00c8d4"])

        glow_id = self.create_oval(x-r-2, y-r-2, x+r+2, y+r+2, outline=color, width=1)
        core_id = self.create_oval(x-r,   y-r,   x+r,   y+r,   fill="#0c0d14", outline="")

        self.bubbles.append({
            "glow_id":      glow_id,
            "core_id":      core_id,
            "x": x, "y": y, "r": r,
            "speed":        random.uniform(0.3, 1.0),
            "color":        color,
            "swing_offset": random.uniform(0, 10),
        })

    def start_animation(self):
        if not self.animating:
            self.animating = True
            self._loop()

    def stop_animation(self):
        self.animating = False

    def _loop(self):
        if not self.animating:
            return
        for b in self.bubbles[:]:
            b["y"] -= b["speed"]
            b["x"] += math.sin(b["y"] / 40.0 + b["swing_offset"]) * 0.25
            r = b["r"]
            self.coords(b["glow_id"], b["x"]-r-2, b["y"]-r-2, b["x"]+r+2, b["y"]+r+2)
            self.coords(b["core_id"], b["x"]-r,   b["y"]-r,   b["x"]+r,   b["y"]+r)
            if b["y"] < -r * 2:
                self.delete(b["glow_id"])
                self.delete(b["core_id"])
                self.bubbles.remove(b)
                self._spawn(init=False)
        self.after(16, self._loop)

#update notification

class UpdateNotificationWindow(ctk.CTkToplevel):
    def __init__(self, parent, lang, update_data):
        super().__init__(parent)
        self.title(LOCALES[lang]["upd_title"])

        WIN_W, WIN_H = 380, 300
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.attributes("-alpha", 0.0)

        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width()  - WIN_W) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - WIN_H) // 2
        self.geometry(f"+{x}+{y}")

        if os.path.exists(ICON_PATH):
            self.after(200, lambda: self.iconbitmap(ICON_PATH))

        release_url = update_data.get("release_url", "https://github.com/shprttx/Proximity/releases")

        self._canvas = ctk.CTkCanvas(self, bg=COLOR_BG, highlightthickness=0, width=WIN_W, height=WIN_H)
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self._content = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=16,
                                     border_color=COLOR_MAIN, border_width=2)

        ctk.CTkLabel(self._content, text=LOCALES[lang]["upd_title"],
                     font=(FONT_NAME, 18, "bold"), text_color=COLOR_MAIN
                     ).pack(pady=(18, 4))

        ctk.CTkLabel(self._content, text=LOCALES[lang]["upd_msg"],
                     font=(FONT_NAME, 13, "bold"), justify="center", text_color="#e0e0e0"
                     ).pack(pady=(0, 4))

        ctk.CTkLabel(self._content, text=LOCALES[lang]["upd_warn"],
                     font=(FONT_NAME, 11, "bold"), justify="center", text_color="#ffffff"
                     ).pack(pady=(0, 12))

        btn_site = ctk.CTkButton(
            self._content, text=LOCALES[lang]["btn_upd_site"],
            fg_color="transparent", border_width=2, border_color=COLOR_MAIN,
            hover_color="#0b2e35", corner_radius=10, text_color=COLOR_MAIN,
            font=(FONT_NAME, 12, "bold"), height=34,
            command=lambda: [play_ui_sound("click"), webbrowser.open("https://github.com/shprttx/Proximity/releases/download/26.06.26/Proximity.exe")]
        )
        btn_site.bind("<Enter>", lambda e: btn_site.configure(text_color="#ffffff"))
        btn_site.bind("<Leave>", lambda e: btn_site.configure(text_color=COLOR_MAIN))
        btn_site.pack(pady=3, fill="x", padx=30)

        btn_gh = ctk.CTkButton(
            self._content, text=LOCALES[lang]["btn_upd_gh"],
            fg_color="#12121e", border_width=1, border_color=COLOR_BORDER,
            hover_color=COLOR_SECONDARY, corner_radius=10, text_color="#ffffff",
            font=(FONT_NAME, 12, "bold"), height=34,
            command=lambda: [play_ui_sound("click"), webbrowser.open("https://github.com/shprttx/Proximity/releases")]
        )
        btn_gh.pack(pady=3, fill="x", padx=30)

        self._pulse_colors = PULSE_COLORS
        self._pulse_step   = 0
        self._pulsing      = False
        self.after(80, self._fade_in)

    #animation chain

    def _fade_in(self, alpha=0.0):
        alpha = min(alpha + 0.07, 1.0)
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(14, lambda: self._fade_in(alpha))
        else:
            self._anim_line()

    def _anim_line(self):
        cx, cy = 190, 150
        line   = self._canvas.create_line(cx, cy, cx, cy, fill=COLOR_MAIN, width=2)
        self._line_id = line
        def grow(w=0):
            if not self._alive(): return
            if w < 130:
                self._canvas.coords(line, cx-w, cy, cx+w, cy)
                self.after(8, lambda: grow(w+7))
            else:
                self._canvas.coords(line, cx-130, cy, cx+130, cy)
                self._fade_title()
        grow()

    def _fade_title(self):
        self._pulsing = True
        self._pulse_loop()
        cx, cy = 190, 150
        colors = color_fade(COLOR_BG, COLOR_MAIN, 28)
        glows  = color_fade(COLOR_BG, "#004455", 28)
        def step(i=0):
            if not self._alive(): return
            if i < len(colors):
                self._canvas.delete("upd_title")
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    self._canvas.create_text(cx+dx, cy-24+dy, text="UPDATE", fill=glows[i],
                                             font=(FONT_NAME, 24, "bold"), tags="upd_title")
                self._canvas.create_text(cx, cy-24, text="UPDATE", fill=colors[i],
                                         font=(FONT_NAME, 24, "bold"), tags="upd_title")
                self.after(14, lambda: step(i+1))
            else:
                self._fade_subtitle()
        step()

    def _fade_subtitle(self):
        cx, cy = 190, 150
        colors = color_fade(COLOR_BG, "#ffffff", 25)
        def step(i=0):
            if not self._alive(): return
            if i < len(colors):
                self._canvas.delete("upd_sub")
                self._canvas.create_text(cx, cy+24, text="AVAILABLE", fill=colors[i],
                                         font=(FONT_NAME, 14, "bold"), tags="upd_sub")
                self.after(14, lambda: step(i+1))
            else:
                self.after(1200, self._fade_out_and_show_content)
        step()

    def _pulse_loop(self):
        if not self._pulsing or not self._alive(): return
        cx, cy = 190, 150
        self._pulse_step = (self._pulse_step + 1) % len(self._pulse_colors)
        color = self._pulse_colors[self._pulse_step]
        glow  = color_fade(color, COLOR_BG, 5)[1]
        try:
            self._canvas.delete("upd_title")
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                self._canvas.create_text(cx+dx, cy-24+dy, text="UPDATE", fill=glow,
                                         font=(FONT_NAME, 24, "bold"), tags="upd_title")
            self._canvas.create_text(cx, cy-24, text="UPDATE", fill=color,
                                     font=(FONT_NAME, 24, "bold"), tags="upd_title")
        except Exception:
            pass
        self.after(140, self._pulse_loop)

    def _fade_out_and_show_content(self):
        self._pulsing = False
        cx, cy  = 190, 150
        color   = self._pulse_colors[self._pulse_step]
        c_title = color_fade(color,     COLOR_BG, 22)
        c_sub   = color_fade("#ffffff", COLOR_BG, 22)
        c_line  = color_fade(COLOR_MAIN,COLOR_BG, 22)
        def step(i=0):
            if not self._alive(): return
            if i < 22:
                glow = color_fade(color, COLOR_BG, 5)[1]
                self._canvas.delete("upd_title")
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    self._canvas.create_text(cx+dx, cy-24+dy, text="UPDATE", fill=glow,
                                             font=(FONT_NAME, 24, "bold"), tags="upd_title")
                self._canvas.create_text(cx, cy-24, text="UPDATE", fill=c_title[i],
                                         font=(FONT_NAME, 24, "bold"), tags="upd_title")
                self._canvas.delete("upd_sub")
                self._canvas.create_text(cx, cy+24, text="AVAILABLE", fill=c_sub[i],
                                         font=(FONT_NAME, 14, "bold"), tags="upd_sub")
                self._canvas.itemconfig(self._line_id, fill=c_line[i])
                self.after(14, lambda: step(i+1))
            else:
                self._canvas.place_forget()
                self._content.place(x=0, y=0, relwidth=1, relheight=1)
        step()

    def _alive(self):
        try:
            return self.winfo_exists()
        except Exception:
            return False

#custom warning

class CustomWarningWindow(ctk.CTkToplevel):
    def __init__(self, parent, lang, callback_yes, callback_no):
        super().__init__(parent)
        self.title(LOCALES[lang]["warn_title"])
        self.geometry("420x240")
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width()  - 420) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 240) // 2
        self.geometry(f"+{x}+{y}")

        if os.path.exists(ICON_PATH):
            self.after(200, lambda: self.iconbitmap(ICON_PATH))

        frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=16,
                             border_color=COLOR_MAIN, border_width=2)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(frame, text=LOCALES[lang]["warn_msg_bold"],
                     font=(FONT_NAME, 14, "bold"), text_color=COLOR_MAIN
                     ).pack(pady=(15, 6))

        ctk.CTkLabel(frame, text=LOCALES[lang]["warn_msg_norm"],
                     font=(FONT_NAME, 11), justify="center", text_color="#cccccc"
                     ).pack(pady=(0, 15))

        btn_yes = ctk.CTkButton(
            frame, text=LOCALES[lang]["btn_yes"],
            fg_color="transparent", border_width=2, border_color=COLOR_MAIN,
            hover_color="#0b2e35", corner_radius=10, text_color=COLOR_MAIN,
            font=(FONT_NAME, 11, "bold"), height=32,
            command=callback_yes
        )
        btn_yes.bind("<Enter>", lambda e: btn_yes.configure(text_color="#ffffff"))
        btn_yes.bind("<Leave>", lambda e: btn_yes.configure(text_color=COLOR_MAIN))
        btn_yes.pack(pady=4, fill="x", padx=30)

        btn_no = ctk.CTkButton(
            frame, text=LOCALES[lang]["btn_no"],
            fg_color="#12121e", border_width=1, border_color=COLOR_BORDER,
            hover_color=COLOR_SECONDARY, corner_radius=10, text_color="#ffffff",
            font=(FONT_NAME, 11), height=32,
            command=callback_no
        )
        btn_no.pack(pady=4, fill="x", padx=30)

#main

class ProximityApp(ctk.CTk):

    #init

    def __init__(self):
        super().__init__()
        self.current_lang = "RU"
        self.title("Proximity")
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)

        self.pulse_step = 0

        if os.path.exists(ICON_PATH):
            self.after(200, lambda: self.iconbitmap(ICON_PATH))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Unmap>", self._on_minimize)

        # toggle
        self.var_happ  = ctk.StringVar(value="off")
        self.var_tg    = ctk.StringVar(value="off")
        self.var_zprtx = ctk.StringVar(value="off")
        self.var_warp  = ctk.StringVar(value="off")

        self.open_buttons   = {}
        self.switch_widgets = {}
        self.tray_icon      = None
        self.update_data    = None

        self._check_for_updates()

        self.attributes("-alpha", 0.0)
        self.withdraw()
        self._show_splash()

    # pdate check

    def _check_for_updates(self):
        def fetch():
            try:
                req = urllib.request.Request(UPDATE_URL, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=4) as r:
                    data = json.loads(r.read().decode("utf-8"))
                    if data.get("version") and data["version"] != CURRENT_VERSION:
                        self.update_data = data
            except Exception:
                pass
        threading.Thread(target=fetch, daemon=True).start()

    #splash

    def _show_splash(self):
        W, H = 480, 300
        splash = ctk.CTkToplevel(self)
        splash.geometry(f"{W}x{H}")
        splash.overrideredirect(True)
        splash.configure(fg_color=COLOR_BG)

        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        splash.geometry(f"+{(sw-W)//2}+{(sh-H)//2}")

        if os.path.exists(ICON_PATH):
            splash.after(200, lambda: splash.iconbitmap(ICON_PATH))

        canvas = ctk.CTkCanvas(splash, bg=COLOR_BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.splash_canvas = canvas

        play_ui_sound("startup")

        cx, cy = W // 2, H // 2
        try:
            user = os.getlogin().title()
        except Exception:
            user = os.environ.get("USERNAME", "USER").title()
        welcome_text = f"WELCOME, {user.upper()}"

        line_id           = canvas.create_line(cx, cy, cx, cy, fill=COLOR_MAIN, width=2)
        pulse_step        = [0]
        current_state     = ["none"]

        def pulse_tick():
            try:
                if not splash.winfo_exists(): return
            except Exception:
                return
            if current_state[0] == "prox":
                pulse_step[0] = (pulse_step[0] + 1) % len(PULSE_COLORS)
                color = PULSE_COLORS[pulse_step[0]]
                glow  = color_fade(color, COLOR_BG, 5)[1]
                try:
                    canvas.delete("text_prox")
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        canvas.create_text(cx+dx, cy-30+dy, text="PROXIMITY", fill=glow,
                                           font=(FONT_NAME, 26, "bold"), tags="text_prox")
                    canvas.create_text(cx, cy-30, text="PROXIMITY", fill=color,
                                       font=(FONT_NAME, 26, "bold"), tags="text_prox")
                except Exception:
                    pass
            splash.after(140, pulse_tick)

        def grow_line(w=0):
            try:
                if not splash.winfo_exists(): return
            except Exception:
                return
            if w < 150:
                canvas.coords(line_id, cx-w, cy, cx+w, cy)
                splash.after(10, lambda: grow_line(w+8))
            else:
                fade_in_prox()

        def fade_in_prox():
            colors = color_fade(COLOR_BG, COLOR_MAIN, 30)
            glows  = color_fade(COLOR_BG, "#004455", 30)
            def step(i=0):
                try:
                    if not splash.winfo_exists(): return
                except Exception:
                    return
                if i < len(colors):
                    canvas.delete("text_prox")
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        canvas.create_text(cx+dx, cy-30+dy, text="PROXIMITY", fill=glows[i],
                                           font=(FONT_NAME, 26, "bold"), tags="text_prox")
                    canvas.create_text(cx, cy-30, text="PROXIMITY", fill=colors[i],
                                       font=(FONT_NAME, 26, "bold"), tags="text_prox")
                    splash.after(16, lambda: step(i+1))
                else:
                    current_state[0] = "prox"
                    fade_in_welc()
            step()

        def fade_in_welc():
            colors = color_fade(COLOR_BG, "#ffffff", 30)
            def step(i=0):
                try:
                    if not splash.winfo_exists(): return
                except Exception:
                    return
                if i < len(colors):
                    canvas.delete("text_welc")
                    canvas.create_text(cx, cy+30, text=welcome_text, fill=colors[i],
                                       font=(FONT_NAME, 14, "bold"), tags="text_welc")
                    splash.after(16, lambda: step(i+1))
                else:
                    splash.after(1500, fade_out_all)
            step()

        def fade_out_all():
            current_state[0] = "none"
            cur_color  = PULSE_COLORS[pulse_step[0]]
            c_prox = color_fade(cur_color,  COLOR_BG, 25)
            c_glow = color_fade(color_fade(cur_color, COLOR_BG, 5)[1], COLOR_BG, 25)
            c_welc = color_fade("#ffffff",  COLOR_BG, 25)
            c_line = color_fade(COLOR_MAIN, COLOR_BG, 25)
            def step(i=0):
                try:
                    if not splash.winfo_exists(): return
                except Exception:
                    return
                if i < 25:
                    canvas.delete("text_prox", "text_welc")
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        canvas.create_text(cx+dx, cy-30+dy, text="PROXIMITY", fill=c_glow[i],
                                           font=(FONT_NAME, 26, "bold"), tags="text_prox")
                    canvas.create_text(cx, cy-30, text="PROXIMITY", fill=c_prox[i],
                                       font=(FONT_NAME, 26, "bold"), tags="text_prox")
                    canvas.create_text(cx, cy+30, text=welcome_text, fill=c_welc[i],
                                       font=(FONT_NAME, 14, "bold"), tags="text_welc")
                    canvas.itemconfig(line_id, fill=c_line[i])
                    splash.after(16, lambda: step(i+1))
                else:
                    finish()
            step()

        def finish():
            try:
                splash.destroy()
            except Exception:
                pass
            self.update_idletasks()
            w, h = 460, 650
            sw2, sh2 = self.winfo_screenwidth(), self.winfo_screenheight()
            self.geometry(f"{w}x{h}+{(sw2-w)//2}+{(sh2-h)//2}")
            self._build_main_ui()
            self.deiconify()
            self._fade_in()

        pulse_tick()
        splash.after(200, grow_line)

    def _fade_in(self, alpha=0.0):
        alpha += 0.06
        self.attributes("-alpha", min(alpha, 1.0))
        if alpha < 1.0:
            self.after(16, lambda: self._fade_in(alpha))
        else:
            if self.update_data:
                self.after(200, lambda: UpdateNotificationWindow(self, self.current_lang, self.update_data))

    #ui

    def _build_main_ui(self):
        self.bg_canvas = BubbleBackground(self)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.start_animation()

        self.main_container = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=20,
                                           border_width=1, border_color=COLOR_BORDER)
        self.main_container.place(relx=0.05, rely=0.04, relwidth=0.90, relheight=0.92)
        self.main_container.lift()

        self._populate_main_screen()

    def _populate_main_screen(self):
        """Fill main_container with the home screen widgets."""
        for w in self.main_container.winfo_children():
            w.destroy()

        self.btn_lang = ctk.CTkButton(
            self.main_container, text=LOCALES[self.current_lang]["lang_btn"],
            width=34, height=24, fg_color="#12121e", border_color=COLOR_BORDER,
            border_width=1, hover_color=COLOR_SECONDARY, corner_radius=8,
            text_color=COLOR_MAIN, font=(FONT_NAME, 10, "bold"),
            command=self.toggle_language
        )
        self.btn_lang.place(relx=0.96, rely=0.03, anchor="ne")

        self.header = ctk.CTkLabel(self.main_container,
                                   text=LOCALES[self.current_lang]["header"],
                                   font=(FONT_NAME, 34, "bold"), text_color=COLOR_MAIN)
        self.header.pack(pady=(40, 15))

        self.subheader = ctk.CTkLabel(self.main_container, text="A G G R E G A T O R",
                                      font=(FONT_NAME, 11, "bold"), text_color="#555566")
        self.subheader.pack(pady=(0, 4))

        self._animate_header()

        scroll_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        scroll_frame.pack(pady=10, padx=20, fill="both")

        self.sw_happ_widget  = self._create_switch(scroll_frame, LOCALES[self.current_lang]["sw_happ"],  self.toggle_happ,  self.var_happ,  "info_happ",  "happ")
        self.sw_tg_widget    = self._create_switch(scroll_frame, LOCALES[self.current_lang]["sw_tg"],    self.toggle_tg,    self.var_tg,    "info_tg",    "tg")
        self.sw_zprtx_widget = self._create_switch(scroll_frame, LOCALES[self.current_lang]["sw_zprtx"], self.toggle_zprtx, self.var_zprtx, "info_zprtx", "zprtx")
        self.sw_warp_widget  = self._create_switch(scroll_frame, LOCALES[self.current_lang]["sw_warp"],  self.toggle_warp,  self.var_warp,  "info_warp",  "warp")

        
        self._sync_open_buttons()

        self.btn_installer = self._create_button(self.main_container, LOCALES[self.current_lang]["btn_installer"], self.open_installer_window, is_accent=True, sound=None)
        self.btn_inst      = self._create_button(self.main_container, LOCALES[self.current_lang]["btn_pdf"],       self.open_instructions)
        self.btn_about     = self._create_button(self.main_container, LOCALES[self.current_lang]["btn_about"],     self.open_about)

        ctk.CTkLabel(self.main_container, text="by shprot",
                     font=(FONT_NAME, 11, "italic"), text_color="#444455"
                     ).pack(side="bottom", pady=12)

    def _sync_open_buttons(self):
        """Light up ↗ buttons for every toggle that is currently ON."""
        mapping = {
            "happ":  self.var_happ,
            "tg":    self.var_tg,
            "zprtx": self.var_zprtx,
            "warp":  self.var_warp,
        }
        for key, var in mapping.items():
            btn = self.open_buttons.get(key)
            if btn is None:
                continue
            if var.get() == "on":
                btn.configure(state="normal", fg_color=COLOR_MAIN,
                              border_color=COLOR_MAIN, text_color="#000000")
            else:
                btn.configure(state="disabled", fg_color="transparent",
                              border_color="#222230", text_color="#555566")

    def _animate_header(self):
        try:
            self.header.configure(text_color=PULSE_COLORS[self.pulse_step])
            self.pulse_step = (self.pulse_step + 1) % len(PULSE_COLORS)
            self.after(140, self._animate_header)
        except Exception:
            pass

    #widge

    def _create_switch(self, parent, text, command, var, info_key, id_key):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(pady=12, fill="x")

        sw = ctk.CTkSwitch(
            row, text=text, variable=var, onvalue="on", offvalue="off",
            command=lambda: [play_ui_sound("switch"), command(var)],
            progress_color=COLOR_MAIN, font=(FONT_NAME, 14, "bold"),
            text_color="#ffffff", button_color="#ffffff", button_hover_color=COLOR_MAIN,
        )
        sw.pack(side="left")
        self.switch_widgets[id_key] = sw

        btn_info = ctk.CTkButton(
            row, text="?", width=28, height=28, corner_radius=14,
            fg_color="#12121e", border_color=COLOR_BORDER, border_width=1,
            hover_color=COLOR_MAIN, text_color="#888899", font=(FONT_NAME, 12, "bold"),
            command=lambda k=info_key: self.show_info_screen(k)
        )
        btn_info.pack(side="right", padx=(5, 0))
        btn_info.bind("<Enter>", lambda e: btn_info.configure(fg_color=COLOR_MAIN, text_color="#000000"))
        btn_info.bind("<Leave>", lambda e: btn_info.configure(fg_color="#12121e",  text_color="#888899"))

        btn_open = ctk.CTkButton(
            row, text="↗", width=28, height=28, corner_radius=14,
            state="disabled", fg_color="transparent", border_width=1,
            border_color="#222230", text_color="#555566",
            hover_color=COLOR_MAIN, font=(FONT_NAME, 14, "bold"),
            command=lambda k=id_key: self._open_app_window(k)
        )
        btn_open.pack(side="right")
        self.open_buttons[id_key] = btn_open

        return sw

    def _create_button(self, master, text, command, is_accent=False, sound="click"):
        def _cmd():
            if sound:
                play_ui_sound(sound)
            command()

        if is_accent:
            btn = ctk.CTkButton(
                master, text=text, command=_cmd,
                fg_color="transparent", border_width=2, border_color=COLOR_MAIN,
                hover_color="#0b2e35", corner_radius=14, text_color=COLOR_MAIN,
                font=(FONT_NAME, 13, "bold"), height=46,
            )
            btn.bind("<Enter>", lambda e: btn.configure(text_color="#ffffff"))
            btn.bind("<Leave>", lambda e: btn.configure(text_color=COLOR_MAIN))
        else:
            btn = ctk.CTkButton(
                master, text=text, command=_cmd,
                fg_color="#12121e", border_width=1, border_color=COLOR_BORDER,
                hover_color=COLOR_SECONDARY, corner_radius=14, text_color="#ffffff",
                font=(FONT_NAME, 13, "bold"), height=46,
            )
            btn.bind("<Enter>", lambda e: btn.configure(border_color=COLOR_MAIN))
            btn.bind("<Leave>", lambda e: btn.configure(border_color=COLOR_BORDER))

        btn.pack(pady=8, fill="x", padx=30)
        return btn

    #launch

    def _launch_happ(self):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        candidates = [
            os.path.join(desktop, "Happ.lnk"),
            os.path.join(desktop, "Happ VPN.lnk"),
            os.path.join(os.environ.get("ProgramFiles",      "C:\\Program Files"),        "Happ", "Happ.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),  "Happ", "Happ.exe"),
            os.path.join(os.environ.get("LocalAppData", ""), "Programs", "Happ", "Happ.exe"),
            os.path.join(os.environ.get("LocalAppData", ""), "Happ", "Happ.exe"),
            os.path.join(os.environ.get("AppData",      ""), "Happ", "Happ.exe"),
        ]
        target = next((p for p in candidates if os.path.exists(p)), None)
        if target:
            target_dir = os.path.dirname(target) if os.path.isfile(target) else TOOLS_DIR
            try:
                subprocess.Popen(f'start "" /d "{target_dir}" "{target}"', shell=True)
                return True
            except Exception:
                return False
        return False

    def _launch_warp(self):
        target = os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"),
                              "Cloudflare", "Cloudflare WARP", "Cloudflare WARP.exe")
        if os.path.exists(target):
            try:
                subprocess.Popen(f'start "" /d "{os.path.dirname(target)}" "{target}"', shell=True)
                return True
            except Exception:
                return False
        return False

    def _open_app_window(self, id_key):
        play_ui_sound("click")
        if id_key == "happ":
            self._launch_happ()
        elif id_key == "warp":
            self._launch_warp()
        elif id_key == "tg":
            webbrowser.open("https://github.com/Flowseal/tg-ws-proxy")
        elif id_key == "zprtx":
            webbrowser.open("https://github.com/shprttx")

    #tra

    def _on_minimize(self, event):
        if event.widget == self and str(self.state()) == "iconic":
            self.withdraw()
            threading.Thread(target=self._create_tray, daemon=True).start()

    def _create_tray(self):
        if self.tray_icon is not None:
            return
        image = (Image.open(ICON_PATH).convert("RGBA")
                 if os.path.exists(ICON_PATH)
                 else Image.new("RGB", (64, 64), color=COLOR_MAIN))
        menu = pystray.Menu(
            pystray.MenuItem(LOCALES[self.current_lang]["tray_show"], self._tray_show, default=True),
            pystray.MenuItem(LOCALES[self.current_lang]["tray_exit"], self._tray_exit),
        )
        self.tray_icon = pystray.Icon("Proximity", image, "Proximity", menu)
        self.tray_icon.run()

    def _tray_show(self, icon, item):
        self.tray_icon.stop()
        self.tray_icon = None
        self.after(0, self._restore_window)

    def _tray_exit(self, icon, item):
        self.tray_icon.stop()
        self.tray_icon = None
        self.after(0, self.on_closing)

    def _restore_window(self):
        self.deiconify()
        self.state("normal")

    #language

    def toggle_language(self):
        self.current_lang = "RU" if self.current_lang == "EN" else "EN"
        l = LOCALES[self.current_lang]
        safe = lambda fn: (lambda: None)() if True else None

        def try_cfg(widget, **kw):
            try: widget.configure(**kw)
            except Exception: pass

        try_cfg(self.btn_lang,                    text=l["lang_btn"])
        try_cfg(self.header,                       text=l["header"])
        try_cfg(self.switch_widgets.get("happ"),   text=l["sw_happ"])
        try_cfg(self.switch_widgets.get("tg"),     text=l["sw_tg"])
        try_cfg(self.switch_widgets.get("zprtx"),  text=l["sw_zprtx"])
        try_cfg(self.switch_widgets.get("warp"),   text=l["sw_warp"])
        try_cfg(self.btn_installer,                text=l["btn_installer"])
        try_cfg(self.btn_inst,                     text=l["btn_pdf"])
        try_cfg(self.btn_about,                    text=l["btn_about"])

    #close / warning

    def on_closing(self):
        if "on" in (self.var_happ.get(), self.var_tg.get(),
                    self.var_zprtx.get(), self.var_warp.get()):
            play_ui_sound("warning")
            CustomWarningWindow(self, self.current_lang,
                                callback_yes=self._force_close,
                                callback_no=self._dismiss_warning)
        else:
            self._force_close()

    def _dismiss_warning(self):
        """Close the warning dialog without touching toggle/arrow state."""
        for w in self.winfo_children():
            if isinstance(w, ctk.CTkToplevel):
                w.grab_release()
                w.destroy()
       
        self._sync_open_buttons()

    def _force_close(self):
        if self.var_happ.get()  == "on": self.toggle_happ (ctk.StringVar(value="off"))
        if self.var_tg.get()    == "on": self.toggle_tg   (ctk.StringVar(value="off"))
        if self.var_zprtx.get() == "on": self.toggle_zprtx(ctk.StringVar(value="off"))
        if self.var_warp.get()  == "on": self.toggle_warp (ctk.StringVar(value="off"))
        self.bg_canvas.stop_animation()
        self.quit()

    #screens

    def show_main_screen(self):
        self._populate_main_screen()

    def show_installer_screen(self):
        lang = self.current_lang
        for w in self.main_container.winfo_children():
            w.destroy()

        # header
        hdr = ctk.CTkFrame(self.main_container, fg_color="#161618", corner_radius=0, height=48)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=LOCALES[lang]["installer_title"],
                     font=(FONT_NAME, 13, "bold"), text_color="#e8e8e8", anchor="w"
                     ).place(x=16, rely=0.5, anchor="w")
        ctk.CTkLabel(hdr, text="PROXIMITY",
                     font=(FONT_NAME, 10), text_color="#444455", anchor="e"
                     ).place(relx=1.0, x=-16, rely=0.5, anchor="e")

        # separator
        sep = ctk.CTkCanvas(self.main_container, height=1, bg=COLOR_FRAME, highlightthickness=0)
        sep.pack(fill="x")
        sep.create_line(0, 0, 460, 0, fill=COLOR_MAIN, width=1)

        # body
        body = ctk.CTkFrame(self.main_container, fg_color="transparent", corner_radius=0)
        body.pack(fill="both", expand=True, padx=20, pady=16)
        ctk.CTkLabel(body, text=LOCALES[lang]["installer_label"],
                     font=(FONT_NAME, 11), text_color="#888899", anchor="w"
                     ).pack(anchor="w", pady=(0, 12))

        def make_row(parent, label, callback):
            row = ctk.CTkFrame(parent, fg_color="#16161a", corner_radius=4,
                               border_width=1, border_color="#2a2a35", height=40)
            row.pack(fill="x", pady=4)
            row.pack_propagate(False)

            inner = ctk.CTkFrame(row, fg_color="transparent", corner_radius=0)
            inner.place(relx=0, rely=0, relwidth=1, relheight=1)

            lbl   = ctk.CTkLabel(inner, text=label, font=(FONT_NAME, 12),
                                  text_color="#c8c8d0", anchor="w")
            lbl.place(x=14, rely=0.5, anchor="w")

            arrow = ctk.CTkLabel(inner, text="›", font=(FONT_NAME, 16), text_color="#444455")
            arrow.place(relx=1.0, x=-14, rely=0.5, anchor="e")

            def on_enter(e):
                row.configure(fg_color="#1e1e28", border_color=COLOR_MAIN)
                lbl.configure(text_color="#ffffff")
                arrow.configure(text_color=COLOR_MAIN)
            def on_leave(e):
                row.configure(fg_color="#16161a", border_color="#2a2a35")
                lbl.configure(text_color="#c8c8d0")
                arrow.configure(text_color="#444455")
            def on_click(e):
                play_ui_sound("click")
                callback()

            for widget in (row, inner, lbl, arrow):
                widget.bind("<Enter>",    on_enter)
                widget.bind("<Leave>",    on_leave)
                widget.bind("<Button-1>", on_click)

        make_row(body, LOCALES[lang]["installer_happ"], self._install_happ)
        make_row(body, LOCALES[lang]["installer_warp"], self._install_warp)

        # footer
        footer = ctk.CTkFrame(self.main_container, fg_color="#161618", corner_radius=0, height=44)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        btn_close = ctk.CTkButton(
            footer, text=LOCALES[lang]["installer_close"],
            width=130, height=26, corner_radius=3,
            fg_color="#252530", border_width=1, border_color="#333344",
            hover_color="#2e2e3d", text_color="#999aaa", font=(FONT_NAME, 11),
            command=self.show_main_screen
        )
        btn_close.place(relx=1.0, x=-16, rely=0.5, anchor="e")

    def show_info_screen(self, info_key):
        lang = self.current_lang
        text = LOCALES[lang][info_key]

        for w in self.main_container.winfo_children():
            w.destroy()

        # top accent
        top_line = ctk.CTkCanvas(self.main_container, height=2, bg=COLOR_FRAME, highlightthickness=0)
        top_line.pack(fill="x")
        top_line.create_line(0, 1, 460, 1, fill=COLOR_MAIN, width=2)

        ctk.CTkLabel(self.main_container, text="// INFO",
                     font=(FONT_NAME, 11, "bold"), text_color=COLOR_MAIN, anchor="w"
                     ).pack(anchor="w", padx=24, pady=(14, 0))

        text_frame = ctk.CTkFrame(self.main_container, fg_color="#0c0d14",
                                  corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        text_frame.pack(fill="both", expand=True, padx=20, pady=(8, 0))

        text_label = ctk.CTkLabel(text_frame, text="", font=(FONT_NAME, 12),
                                  text_color="#e0e0e8", justify="left",
                                  anchor="nw", wraplength=360)
        text_label.pack(fill="both", expand=True, padx=16, pady=14)

        # typewriter
        chars     = list(text)
        displayed = [""]
        def type_char(i=0):
            if i < len(chars):
                displayed[0] += chars[i]
                text_label.configure(text=displayed[0])
                delay = 8 if chars[i] not in ("\n", " ") else 4
                self.main_container.after(delay, lambda: type_char(i+1))
        self.main_container.after(120, lambda: type_char(0))

        # back button
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer.pack(fill="x", side="bottom", pady=16, padx=20)

        back_text = "← Back" if lang == "EN" else "← Назад"
        btn_back  = ctk.CTkButton(
            footer, text=back_text,
            fg_color="transparent", border_width=2, border_color=COLOR_MAIN,
            hover_color="#0b2e35", corner_radius=10, text_color=COLOR_MAIN,
            font=(FONT_NAME, 12, "bold"), height=38,
            command=self.show_main_screen
        )
        btn_back.bind("<Enter>", lambda e: btn_back.configure(text_color="#ffffff"))
        btn_back.bind("<Leave>", lambda e: btn_back.configure(text_color=COLOR_MAIN))
        btn_back.pack(fill="x")

    #installe

    def open_installer_window(self):
        play_ui_sound("master")
        self.show_installer_screen()

    def _install_happ(self):
        path = os.path.join(TOOLS_DIR, "Happinstallation", "setup-Happ.x64.exe")
        if os.path.exists(path): os.startfile(path)

    def _install_warp(self):
        path = os.path.join(TOOLS_DIR, "warpinstall", "CloudflareWARP.msi")
        if os.path.exists(path): os.startfile(path)

    def open_instructions(self):
        path = os.path.join(TOOLS_DIR, "INST.pdf")
        if os.path.exists(path): os.startfile(path)

    def open_about(self):
        webbrowser.open("https://github.com/shprttx/Proximity")

    #toggle handlers

    def toggle_happ(self, var):
        if var.get() == "on":
            self.open_buttons["happ"].configure(state="normal", fg_color=COLOR_MAIN,
                                                border_color=COLOR_MAIN, text_color="#000000")
            if not self._launch_happ():
                var.set("off")
                self.switch_widgets["happ"].deselect()
                self.open_buttons["happ"].configure(state="disabled", fg_color="transparent",
                                                    border_color="#222230", text_color="#555566")
        else:
            self.open_buttons["happ"].configure(state="disabled", fg_color="transparent",
                                                border_color="#222230", text_color="#555566")
            subprocess.run("taskkill /IM Happ.exe /F", shell=True, creationflags=CREATE_NO_WINDOW)

    def toggle_tg(self, var):
        t_path = os.path.join(TOOLS_DIR, "TG", "TgWsProxy_windows.exe")
        if var.get() == "on":
            self.open_buttons["tg"].configure(state="normal", fg_color=COLOR_MAIN,
                                              border_color=COLOR_MAIN, text_color="#000000")
            if os.path.exists(t_path):
                subprocess.Popen(t_path, creationflags=CREATE_NO_WINDOW)
            else:
                var.set("off")
                self.switch_widgets["tg"].deselect()
                self.open_buttons["tg"].configure(state="disabled", fg_color="transparent",
                                                  border_color="#222230", text_color="#555566")
        else:
            self.open_buttons["tg"].configure(state="disabled", fg_color="transparent",
                                              border_color="#222230", text_color="#555566")
            subprocess.run("taskkill /IM TgWsProxy_windows.exe /F",
                           shell=True, creationflags=CREATE_NO_WINDOW)

    def toggle_zprtx(self, var):
        z_dir    = os.path.abspath(os.path.join(TOOLS_DIR, "Zprtx"))
        main_bat = "MAIN.bat"
        full_bat = os.path.join(z_dir, main_bat)

        if var.get() == "on":
            self.open_buttons["zprtx"].configure(state="normal", fg_color=COLOR_MAIN,
                                                 border_color=COLOR_MAIN, text_color="#000000")
            if os.path.exists(full_bat):
                try:
                    subprocess.Popen(f'start "" /d "{z_dir}" "{main_bat}"', shell=True)
                except Exception:
                    var.set("off")
                    self.switch_widgets["zprtx"].deselect()
                    self.open_buttons["zprtx"].configure(state="disabled", fg_color="transparent",
                                                        border_color="#222230", text_color="#555566")
            else:
                var.set("off")
                self.switch_widgets["zprtx"].deselect()
                self.open_buttons["zprtx"].configure(state="disabled", fg_color="transparent",
                                                     border_color="#222230", text_color="#555566")
        else:
            self.open_buttons["zprtx"].configure(state="disabled", fg_color="transparent",
                                                 border_color="#222230", text_color="#555566")
            
            if self.var_warp.get() == "on":
                self.var_warp.set("off")
                self.switch_widgets["warp"].deselect()
                self.open_buttons["warp"].configure(state="disabled", fg_color="transparent",
                                                    border_color="#222230", text_color="#555566")
                subprocess.run('taskkill /IM "Cloudflare WARP.exe" /F',
                               shell=True, creationflags=CREATE_NO_WINDOW)
            try:
                subprocess.run("taskkill /IM winws.exe /F", shell=True, creationflags=CREATE_NO_WINDOW)
                subprocess.run("taskkill /IM cmd.exe /F",   shell=True, creationflags=CREATE_NO_WINDOW)
            except Exception:
                pass

    def toggle_warp(self, var):
        if var.get() == "on":
            if self.var_zprtx.get() == "off":
                self.switch_widgets["zprtx"].select()
                self.var_zprtx.set("on")
                self.toggle_zprtx(self.var_zprtx)
            self.open_buttons["warp"].configure(state="normal", fg_color=COLOR_MAIN,
                                                border_color=COLOR_MAIN, text_color="#000000")
            if not self._launch_warp():
                var.set("off")
                self.switch_widgets["warp"].deselect()
                self.open_buttons["warp"].configure(state="disabled", fg_color="transparent",
                                                    border_color="#222230", text_color="#555566")
        else:
            self.open_buttons["warp"].configure(state="disabled", fg_color="transparent",
                                                border_color="#222230", text_color="#555566")
            subprocess.run('taskkill /IM "Cloudflare WARP.exe" /F',
                           shell=True, creationflags=CREATE_NO_WINDOW)

#

if __name__ == "__main__":
    app = ProximityApp()
    app.mainloop()
