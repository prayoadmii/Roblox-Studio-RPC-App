import tkinter as tk
from flask import Flask, request, jsonify
import threading
import time
from pypresence import Presence
import ctypes
import sys, os
import pystray
from PIL import Image

discord_connected = False
RPC = None

DEFAULT_RPC = {
    "details": "On Startpage Or Did Not Close Server",
    "state": "Editing: nil",
    "large_image": None,
    "small_image": "https://tr.rbxcdn.com/30DAY-AvatarHeadshot-310966282D3529E36976BF6B07B1DC90-Png/100/100/AvatarHeadshot/Png/isCircular"
}

def init_discord_rpc():
    global RPC, discord_connected
    try:
        if RPC is None:
            RPC = Presence("1435950204535836702")
            RPC.connect()
            RPC.update(**DEFAULT_RPC)
        discord_connected = True
        DiscordStatus.config(text="Discord Was Connected!", fg="#00FF00")
    except Exception as e:
        RPC = None
        discord_connected = False
        DiscordStatus.config(text="Can't Connect To Discord Retrying...", fg="red")
        print("Discord RPC not connected yet:", e)

last_update = time.time()
app = Flask(__name__)

def disconnect_discord_rpc():
    global RPC, discord_connected
    if RPC is not None:
        try:
            RPC.close()
        except Exception as e:
            print("Error closing Discord RPC:", e)
        RPC = None
    discord_connected = False
    DiscordStatus.config(text="Server Paused! Open Roblox Studio To Resume", fg="red")

@app.route("/StudioRPC/Update", methods=["POST"])
def rpc_upload():
    global last_update, discord_connected
    data = request.json or {}

    # Reconnect if not connected
    if not discord_connected:
        init_discord_rpc()

    if discord_connected:
        try:
            RPC.update(
                details="Game: " + data.get("Details", "No Return"),
                state="Editing: " + data.get("State", "No Return"),
                large_image=data.get("LargeImage", None),
                small_image=data.get("SmallImage", None),
                large_text=data.get("BigImageToolHover", "Roblox Studio"),
                small_text=data.get("SmallImageHover", "No Return")
            )
        except Exception as e:
            discord_connected = False
            DiscordStatus.config(text="Can't Connect To Discord Retrying...", fg="red")
            print("Failed to update Discord RPC:", e)

    Top.config(text=f"Game: {data.get('Details', '')}")
    Disc.config(text=f"Editing: {data.get('State', '')}")
    last_update = time.time() 
    return jsonify({"status": "OK", "received": data})

def start_flask():
    ResaultIPLabel.config(text=f"Server Is Running On: http://127.0.0.1:1234")
    app.run(host="127.0.0.1", port=1234, debug=False)

def timeout_checker():
    global last_update, discord_connected
    while True:
        elapsed = time.time() - last_update
        if elapsed > 15:
            if discord_connected:
                disconnect_discord_rpc()
            Top.config(text="Please Start Your Roblox Studio!")
            Disc.config(text="Waiting For Data From Roblox Studio")
        elif elapsed > 5:
            if discord_connected:
                try:
                    RPC.update(**DEFAULT_RPC)
                except:
                    pass
            Top.config(text="Please Start Your Roblox Studio!")
            Disc.config(text="Waiting For Data From Roblox Studio")
        time.sleep(1)

def discord_reconnect_checker():
    while True:
        if not discord_connected:
            init_discord_rpc()
        time.sleep(0.25)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

window = tk.Tk()
window.title("Roblox Studio RPC Server")
window.geometry("400x150")
window.resizable(False, False)

icon_path = resource_path("Icon.ico")
window.iconbitmap(icon_path)

DWMWA_USE_IMMERSIVE_DARK_MODE = 20
hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
ctypes.windll.dwmapi.DwmSetWindowAttribute(
    hwnd,
    DWMWA_USE_IMMERSIVE_DARK_MODE,
    ctypes.byref(ctypes.c_int(1)),
    ctypes.sizeof(ctypes.c_int(1))
)

window.configure(bg="#111111")
Top = tk.Label(window, text="Please Start Your Roblox Studio!", font=("Arial", 12, "bold"),
               bg="#111111", fg="white")
Top.pack(pady=5)

Disc = tk.Label(window, text="Waiting For Data From Roblox Studio", font=("Arial", 12, "bold"),
                bg="#111111", fg="white")
Disc.pack(pady=5)

ResaultIPLabel = tk.Label(window, text="Loading Server...", font=("Arial", 12), bg="#111111", fg="#0070FF")
ResaultIPLabel.pack(pady=5)

DiscordStatus = tk.Label(window, text="Connecting To Discord...", font=("Arial", 12), bg="#111111", fg="#0070FF")
DiscordStatus.pack(pady=5)

def show_window(icon, item):
    window.after(0, window.deiconify)

def quit_app(icon, item):
    icon.stop()
    window.destroy()
    sys.exit()

icon_image = Image.open(icon_path)
menu = pystray.Menu(
    pystray.MenuItem("Show Window", show_window),
    pystray.MenuItem("Stop Server", quit_app)
)
tray_icon = pystray.Icon("rpc_client", icon_image, "Roblox Studio RPC Server", menu)

def run_tray():
    tray_icon.run()

threading.Thread(target=run_tray, daemon=True).start()

def on_closing():
    window.withdraw()

window.protocol("WM_DELETE_WINDOW", on_closing)

threading.Thread(target=start_flask, daemon=True).start()
threading.Thread(target=timeout_checker, daemon=True).start()
threading.Thread(target=discord_reconnect_checker, daemon=True).start()

window.mainloop()
