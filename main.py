import time
import random
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from visuals import create_layout, get_ascii_face, generate_roast_table, generate_stability_bar, get_matrix_line
from logic import get_system_status, generate_insult, start_watching

console = Console()
layout = create_layout()
roasts = ["SENTINEL v2.0 (GOD MODE) INITIALIZED.", "SCANNING FOR MEDIOCRE CODE... FOUND PLENTY."]
stability_level = 0
start_time = time.time()

def notify_save(msg):
    roasts.append(msg)

observer = start_watching(notify_save)

try:
    with Live(layout, refresh_per_second=6, screen=True) as live:
        while True:
            cpu, mem, distracted, mood = get_system_status()
            work_duration = time.time() - start_time
     
            if distracted:
                stability_level = min(100, stability_level + 3)
            else:
                stability_level = max(0, stability_level - 1)

            header_content = get_matrix_line(console.width - 4)
            if stability_level > 50 or cpu > 70:
                header_content = f"[bold green]{header_content}[/bold green]"
            layout["header"].update(Panel(header_content, style="green on black"))
            
            current_face = get_ascii_face(mood if stability_level < 95 else "dead")
            brain_display = f"\n{current_face}\n\n[bold yellow]NEURAL STATE: {mood.upper()}[/bold yellow]\n"
            if stability_level > 60:
                brain_display += "[blink red]CRITICAL DISTRACTION[/blink red]"
            
            layout["brain"].update(Panel(brain_display, title="Core Consciousness"))
            
            if random.random() < 0.04:
                roasts.append(f"[bold red]>[/bold red] {generate_insult(cpu, distracted)}")
            
            layout["roast_log"].update(Panel(generate_roast_table(roasts), title="Judgment Log"))
            
            layout["footer"].update(Panel(generate_stability_bar(stability_level, work_duration)))
            
            time.sleep(0.1)

except KeyboardInterrupt:
    observer.stop()
    console.print("\n[bold red]SENTINEL: You can't run from the truth. Shutdown complete.[/bold red]\n")

observer.join()