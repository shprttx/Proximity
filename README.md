<div align="center">
<pre>
 ───═▶   ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗███╗   ███╗██╗████████╗██╗   ██╗   ◀═───
 ───═▶   ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝██║████╗ ████║██║╚══██╔══╝╚██╗ ██╔╝   ◀═───
 ───═▶   ██████╔╝██████╔╝██║   ██║ ╚███╔╝ ██║██╔████╔██║██║   ██║    ╚████╔╝    ◀═───
 ───═▶   ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗ ██║██║╚██╔╝██║██║   ██║     ╚██╔╝     ◀═───
 ───═▶   ██║     ██║  ██║╚██████╔╝██╔╝ ██╗██║██║ ╚═╝ ██║██║   ██║      ██║      ◀═───
 ───═▶   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝   ╚═╝      ╚═╝      ◀═───
</pre>

### Объединяет разные инструменты обхода блокировок под одним капотом — без ручной настройки конфигов


[![Platform](https://img.shields.io/badge/Platform-Windows-00f2ff?style=for-the-badge&logo=windows11&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.x-00c8d4?style=for-the-badge&logo=python&logoColor=white)](#)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1ae5ff?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-ff0844?style=for-the-badge)](https://github.com/shprttx/Proximity/blob/main/LICENSE)

[![Version](https://img.shields.io/github/v/release/shprttx/Proximity?style=flat-square&color=00f2ff&label=version)](https://github.com/shprttx/Proximity/releases)
[![Downloads](https://img.shields.io/github/downloads/shprttx/Proximity/total?style=flat-square&color=00c8d4)](https://github.com/shprttx/Proximity/releases)
[![Stars](https://img.shields.io/github/stars/shprttx/Proximity?style=flat-square&color=ff0844)](https://github.com/shprttx/Proximity/stargazers)

</div>




## 🚀 Что это

**Proximity** - desktop-приложение для Windows, которое собирает популярные инструменты обхода блокировок в едином интерфейсе с тумблерами. Не нужно вручную гонять `.bat` файлы и разбираться - включил тумблер, получил обход.

Все утилиты внутри от оригинальных авторов, ссылки на них указаны в разделе [Состав](#-состав).

<br>

## 🖥 Главный экран и трей

<div align="center">
<table>
<tr>
<td width="50%"><img src="MAIN.png" alt=""100%"></td>
<td width="50%"><img src="TRAY.png" alt="" width="100%"></td>
</tr>
</table>
</div>

<br>

## ⚙️ Как это работает
 
### 🎚️ Ползунки
 
Главные переключатели режимов обхода. Напротив каждого ползунка есть дополнительная кнопка:
 
- **Happ VPN + ZAPRTX** = открывает окно, если оно свёрнуто в системный трей.
- **Остальные** = мгновенно переводят на официальные страницы разработчиков софта.
> ⚠️ Если по какой-то причине ползунок Happ отказывается работать - создайте свой ярлык на рабочем столе.
 
<br>

### 🎮 Дискорд + Ютуб
 
Включение тумблера запускает выбор, после которого вы перейдёте в CMD-консоль нужного вам движка.
 
> 💡 Обход продолжит работать в системе до тех пор, пока вы вручную не переведёте ползунок в положение «ВЫКЛ».
 
<br>

### 🧩 Выбор ZPRTX или ZAPRET
 
При включении Дискорд + Ютуб появится окно выбора движка обхода **ZPRTX** или **ZAPRET**. Выберите нужный, и он запустится в CMD-консоли.
 
<div align="center">
<table>
<tr>
<td width="50%"><img src="CH.png" alt="" width="100%"></td>
</tr>
</table>
</div>
<br>

### ⏻ Выключатель всего
 
Одним нажатием останавливает все активные модули (Happ, TG Proxy, WARP, Дискорд + Ютуб) по очереди.
 
Сопровождается красной ударной волной, расходящейся по фону приложения.
 
<br>

### 🧙 Мастер установщик
 
Открывает окно для выборочной установки необходимых компонентов (Пока что Happ VPN или Cloudflare WARP).
 
<br>

### 📘 Кнопка инструкции
 
Подробный гайд по настройке Happ и Cloudflare WARP. Содержит 2 бесплатные ссылки на готовые сервера.
 
> 🔥 Вы можете использовать абсолютно любые свои личные или купленные конфигурационные ссылки.
 
<br>

### 🌐 RU / EN
 
Мгновенно переключает язык всего интерфейса приложения (Русский / Английский).
 
<br>

## 🧙 Мастер установки

Отдельное окно для выборочной установки компонентов - Happ VPN и/или Cloudflare WARP

<div align="center">
<table>
<tr>
<td width="50%"><img src="WIZZ.png" alt="" width="90%"></td>
</tr>
</table>
</div>

<br>

## 🛠️ Настройки

Отдельный экран для тонкой настройки поведения приложения: автозапуск с Windows, старт свёрнутым в трей, предупреждение при закрытии активных сервисов и автозапуск нужных утилит при каждом старте Proximity.

<div align="center">
<table>
<tr>
<td width="50%"><img src="SETT.png" alt="" width="90%"></td>
</tr>
</table>
</div>

<br>

## 🔐 Состав

| Инструмент | Назначение | Автор |
| :--- | :--- | :--- |
| 🌐 **Happ VPN** | Продвинутый инструмент маршрутизации и конфигураций для управления трафиком. Инструкция и установщик вшиты. | [**Happ**](https://github.com/Happ-proxy) |
| ✈️ **TG Proxy** | Локальный MTProto-прокси для Telegram Desktop — ускоряет работу Telegram через WebSocket-соединения. Данные передаются в зашифрованном виде, сторонние сервера не нужны. | [**Flowseal**](https://github.com/Flowseal) |
| 🧡 **Cloudflare WARP** | Объединяет функции VPN и безопасного DNS-резолвера. Ускоряет загрузку сайтов и открывает доступ к зарубежным ИИ-моделям (Gemini, Claude, ChatGPT). | [**Cloudflare, Inc.**](https://one.one.one.one) |
| 👾 **ZPRTX** | Сборка, объединившая версию от **Lux1de** и версию от **Flowseal**. | [**Shprot**](https://github.com/shprttx) |
| 👾 **ZAPRET-DISCORD-YOUTUBE** | Оригинал от **Flowseal**. | [**Flowseal**](https://github.com/Flowseal) |

<br>

## ⚖️ Лицензия

Проект распространяется на условиях лицензии [MIT](https://github.com/shprttx/Proximity/blob/main/LICENSE).

<div align="center">
<sub>Made with 🖤 by <a href="https://github.com/shprttx">Shprot</a></sub>
</div>


