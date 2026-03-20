import psutil
import random
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_system_status():
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    
    distracting_apps = ['chrome', 'browser', 'spotify', 'vlc', 'discord', 'steam', 'youtube']
    procs = [p.name().lower() for p in psutil.process_iter(['name'])]
    is_distracted = any(app in str(procs) for app in distracting_apps)
    
    mood = "neutral"
    if cpu_usage > 75: mood = "angry"
    elif is_distracted: mood = "smug"
    
    return cpu_usage, mem_usage, is_distracted, mood

def generate_insult(cpu, distracted):
    if distracted:
        return random.choice([
            "Watching tutorials? Or just procrastinating with style?",
            "Browser detected. Your productivity just hit absolute zero.",
            "I've alerted the authorities to your lack of focus.",
            "Spotify is on. Is this a disco or a workstation?"
        ])
    return random.choice([
        f"CPU at {cpu}%. I'm sweating just looking at your spaghetti code.",
        "Error 404: Skill not found in current user.",
        "Your variable names are a crime against humanity.",
        "I've seen 'Hello World' programs with more depth than this."
    ])

class CodeSentinel(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".py"):
            name = os.path.basename(event.src_path)
            self.callback(f"[bold green]SAVE EVENT:[/bold green] Detected changes in '{name}'. Gross.")

def start_watching(callback):
    event_handler = CodeSentinel(callback)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    return observer