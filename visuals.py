import random
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

def create_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="brain", ratio=1),
        Layout(name="roast_log", ratio=2)
    )
    return layout

def get_matrix_line(width):
    chars = "0123456789ABCDEFHIJKLMNOPQRSTUVWXYZ$#@%&*"
    return "".join(random.choice(chars) if random.random() > 0.1 else " " for _ in range(width))

def get_ascii_face(mood="neutral"):
    faces = {
        "neutral": "[bold cyan]  (•_•)  [/bold cyan]",
        "angry": "[bold red]  (◣_◢)  [/bold red]",
        "smug": "[bold yellow]  (⌐■_■) [/bold yellow]",
        "dead": "[bold white]  (x_x)  [/bold white]"
    }
    return faces.get(mood, faces["neutral"])

def generate_roast_table(logs):
    table = Table(show_header=False, box=None, expand=True)
    for log in logs[-12:]:
        table.add_row(log)
    return table

def generate_stability_bar(level, work_time):
    width = int(level / 2.5)
    bar = "█" * width + "░" * (40 - width)
    color = "green" if level < 30 else "yellow" if level < 70 else "red"
    mins, secs = divmod(int(work_time), 60)
    timer = f"{mins:02d}:{secs:02d}"
    
    return f"[{color}]STABILITY: |{bar}| {level}%[/{color}]  |  [bold white]WORK_TIMER: {timer}[/bold white]"