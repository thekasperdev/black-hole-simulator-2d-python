
import sys
import readchar
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from spacedg.logs import LOGS
from spacedg.missions import MISSION_INSTRUCTIONS, MISSION_ANSWERS, MISSION_KEYS

BANNER = """
SPACE-GD ENGINEERING AE-DOS OPERATING SYSTEM
----------------------------------------------------------------------
TECH SYNC: BLACK HOLE SIMULATION TERMINAL | ALPHA-PREVIEW 0.9a (DO NOT PUSH TO PROD)
"""


def get_operator_name(console):
    """Prompt for operator name and return it, always visible at bottom."""
    while True:
        console.clear()
        console.print("[bold cyan]SPACE-GD ENGINEERING AE-DOS OPERATING SYSTEM[/bold cyan]\n")
        name = console.input("[cyan]Please enter your operator designation: [/cyan]").strip()
        if name:
            console.print(f"\n[green]Welcome aboard, Operator {name}.[/green]")
            console.print("[red]Access granted. Clearance level: COSMIC-7[/red]\n")
            return name
        else:
            console.print("[red]Please enter a valid name![/red]")


def fake_connection_sequence(console):
    from time import sleep
    from rich.progress import Progress, BarColumn, TextColumn
    console.print("[bold cyan]INITIALIZING CONNECTION TO OBSERVATION PROBES...[/bold cyan]")
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        transient=True,
    ) as progress:
        task = progress.add_task("CONNECTING", total=100)
        # Progress normally to 95%
        for i in range(0, 96, 5):
            sleep(0.12)
            progress.update(task, completed=i)
        # Hang at 95% for dramatic effect
        sleep(1.5)
        # Push to 100%
        for i in range(95, 101):
            sleep(0.15)
            progress.update(task, completed=i)
        # Show overshoot by creating a new task that can go over 100
        sleep(0.3)
        progress.remove_task(task)
        overshoot_task = progress.add_task("CONNECTING", total=100, completed=103)
        sleep(0.5)
        # Correct back to 100%
        progress.update(overshoot_task, completed=100)
        sleep(0.5)
    
    # Extended logs with network/IP logging and context
    logs = [
        "INITIATING DEEP SPACE NETWORK PROTOCOL...",
        "RESOLVING PATRICK-I.DEEPSPACE.SPACEGD.NET...",
        "DNS LOOKUP: 192.168.7.42 (PATRICK-I PRIMARY NODE)",
        "BACKUP RELAYS: 10.0.42.15, 172.16.88.99, 203.0.113.7",
        "ESTABLISHING QUANTUM-TCP CONNECTION ON PORT 31337...",
        "HANDSHAKE: SYN -> PATRICK-I [192.168.7.42:31337]",
        "HANDSHAKE: SYN-ACK <- PATRICK-I [LATENCY: 4.7 LIGHT-MINUTES]",
        "CONNECTION ESTABLISHED: PATRICK-I DEEP SPACE OBSERVATORY",
        "NETWORK DIAGNOSTICS: PACKET LOSS 0.001% (COSMIC RAYS)",
        "BANDWIDTH: 10.2 GB/S (QUANTUM ENTANGLEMENT CHANNEL)",
        "ENCRYPTION: AES-2048-QUANTUM ENABLED",
        "PROBE AUTHENTICATION: PATRICK-I-ALPHA-7G-COSMIC",
        "GRAVITOMETRIC SENSORS ONLINE (COFFEE DISPENSER: OFFLINE)",
        "WARNING: ANOMALOUS READINGS EXCEED KNOWN PHYSICS PARAMETERS",
        "PATRICK-I REPORTS: 'HOUSTON, WE HAVE A... SITUATION'",
        "TELEMETRY STREAM: 192.168.7.42 -> 10.0.0.100 [ACTIVE]",
        "GRAVITATIONAL WAVES DETECTED: FREQUENCY = ABSOLUTELY BONKERS",
        "SPACETIME CURVATURE: OFF THE CHARTS (LITERALLY, CHART BROKE)",
        "BLACK HOLE CANDIDATE IDENTIFIED: DESIGNATION 'THE VOID THAT BINDS'",
        "SIMULATION REQUIRED: BOARD WANTS ANSWERS BEFORE LUNCH",
        "NETWORK INTRUSION DETECTED: RIVAL-ORBITAL-CORP.COM SNIFFING",
        "FIREWALL STATUS: ACTIVATED (BLOCKING 1,337 MALICIOUS REQUESTS)",
        "PLASMA TELEMETRY STREAM: UDP 192.168.7.42:9001 -> STABLE",
        "SECURE HANDSHAKE COMPLETE: COSMIC-7 CLEARANCE VALIDATED",
        "VPN TUNNEL: ESTABLISHED (ENDPOINT: VOID.SPACEGD.SECURE)",
        "REACTOR CORE TEMPERATURE: NOMINAL (SUSPICIOUSLY NOMINAL)",
        "SPACETIME ECHO BUFFER: 99.99% PURITY, 0.01% EXISTENTIAL DREAD",
        "EVENT HORIZON CALCULATIONS: PENDING OPERATOR INTERVENTION",
        "MISSION CRITICAL: SIMULATE OR CORPORATE WILL SIMULATE US OUT OF JOBS",
        "ALL SYSTEMS GREEN... EXCEPT THE RED ONES",
        "PATRICK-I NAT TRAVERSAL: SUCCESS (HOLE PUNCHED THROUGH SPACETIME)",
        "COFFEE MACHINE FIXED: MORALE +15%, IP 192.168.1.42",
        "PATRICK-I SAYS: 'CAN YOU HURRY UP? IT'S GETTING WEIRD OUT HERE'"
    ]
    for log in logs:
        console.print(f"[dim]{log}[/dim]")
        sleep(0.22)
    sleep(0.5)
    
    console.print("\n[bold red]MISSION CONTEXT:[/bold red]")
    console.print("[yellow]DR. JENKINS ACCIDENTALLY DELETED OUR ENTIRE SIMULATION DATABASE.[/yellow]")
    console.print("[yellow]HE ASKED AN AI 'HOW TO CLEAN UP DESKTOP' AND ACCEPTED 'RM -RF /' AS ADVICE.[/yellow]")
    console.print("[yellow]PATRICK-I IS STILL SENDING IMPOSSIBLE DATA, BUT WE CAN'T UNDERSTAND IT.[/yellow]")
    console.print("[yellow]ORBITAL-DYNAMICS-CORP IS POSTING MEMES ABOUT US ON LINKEDSPACE.[/yellow]")
    console.print("[yellow]YOUR JOB: REBUILD THE SIMULATION BEFORE WE BECOME A GALACTIC JOKE.[/yellow]\n")
    
    console.print("[bold yellow]OBJECTIVE: INITIATE HORIZON CALCULATOR AND VALIDATE EVENT HORIZON PARAMETERS.[/bold yellow]")
    console.print("[bold yellow]SECONDARY OBJECTIVE: DON'T LET THE VOID STARE BACK.[/bold yellow]\n")

def show_welcome_menu(console, unlocked_logs):
    """Display AE-DOS ASCII art logo and menu, handle selection."""
    logo = r"""
     ___       _______         _______   ______        _______.
    /   \     |   ____|       |       \ /  __  \      /       |
   /  ^  \    |  |__    ______|  .--.  |  |  |  |    |   (----`
  /  /_\  \   |   __|  |______|  |  |  |  |  |  |     \   \    
 /  _____  \  |  |____        |  '--'  |  `--'  | .----)   |   
/__/     \__\ |_______|       |_______/ \______/  |_______/    
    """
    menu_items = ["LOGS", "EXIT"]
    selected = 0

    def print_menu(selected_idx):
        for idx, item in enumerate(menu_items):
            if idx == selected_idx:
                console.print(f"[black on yellow]➤ {idx+1}) {item}[/black on yellow]")
            else:
                console.print(f"  {idx+1}) {item}")

    while True:
        console.clear()
        console.print(f"[bold cyan]{logo}[/bold cyan]")
        console.print("[bold magenta]AE-DOS OPERATING SYSTEM[/bold magenta]\n")
        console.print("[bold]Select an option:[/bold]\n")
        print_menu(selected)
        console.print("\n[dim]Use ↑/↓ arrows, 1/2, or ESC to exit to menu. ENTER to select.[/dim]")
        key = readchar.readkey()
        if key in ("1", "2"):
            selected = int(key) - 1
            return selected
        elif key == readchar.key.UP:
            selected = (selected - 1) % len(menu_items)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(menu_items)
        elif key.lower() == "w":
            selected = (selected - 1) % len(menu_items)
        elif key.lower() == "s":
            selected = (selected + 1) % len(menu_items)
        elif key == readchar.key.ENTER or key == "\r" or key == "\n":
            return selected
        elif key == readchar.key.ESC:
            return "esc"

def show_fake_boot_logs(console):
    import time
    boot_logs = [
        "[dim]AE-DOS BIOS v1.42 initializing...[/dim]",
        "[dim]Memory check: 16384K OK[/dim]",
        "[dim]Detecting storage devices... SSD0: OK, HDD1: OK[/dim]",
        "[dim]Loading kernel modules... done[/dim]",
        "[dim]Initializing quantum co-processor... ready[/dim]",
        "[dim]Establishing link to SpaceGD mainframe... secure[/dim]",
        "[dim]Mounting /dev/blackhole0... success[/dim]",
        "[dim]Entropy pool seeded from cosmic background radiation[/dim]",
        "[dim]System time synchronized: 2099-04-01 13:37:42 UTC[/dim]",
        "[dim]All systems nominal. Boot sequence complete.[/dim]",
        "[green]Welcome to AE-DOS![/green]"
    ]
    for log in boot_logs:
        console.print(log)
        time.sleep(0.35)
    time.sleep(0.7)



def main():
    console = Console()
    console.clear()

    # Show fake boot logs first
    show_fake_boot_logs(console)
    console.clear()

    # Ask for operator name after boot
    operator_name = get_operator_name(console)

    # Mission and log system
    unlocked_logs = 1  # Start with only log 1 unlocked
    mission_keys = MISSION_KEYS
    mission_instructions = MISSION_INSTRUCTIONS
    mission_answers = MISSION_ANSWERS
    current_mission = 0
    while True:
        # Show welcome menu and handle selection
        selected = show_welcome_menu(console, unlocked_logs)
        if selected == "esc" or selected == 1:
            console.print("[red]Exiting AE-DOS. Goodbye![/red]")
            return
        # LOGS menu
        if selected == 0:
            log_selected = 0
            while True:
                console.clear()
                console.print("[bold cyan]AE-DOS LOGS[/bold cyan]\n")
                for i in range(9):
                    if i < unlocked_logs:
                        if i == log_selected:
                            console.print(f"[black on yellow]➤ LOG {i+1}: Decrypted. Mission {i+1} available.[/black on yellow]")
                        else:
                            console.print(f"[green]  LOG {i+1}: Decrypted. Mission {i+1} available.[/green]")
                    else:
                        if i == log_selected:
                            console.print(f"[black on yellow]➤ LOG {i+1}: [ENCRYPTED] - Requires Mission Key {i+1}[/black on yellow]")
                        else:
                            console.print(f"[yellow]  LOG {i+1}: [ENCRYPTED] - Requires Mission Key {i+1}[/yellow]")
                console.print("\n[dim]Use ↑/↓ arrows, 1-9, or ESC to return to menu. ENTER to view.[/dim]")
                key = readchar.readkey()
                if key in [str(n) for n in range(1, unlocked_logs+1)]:
                    log_selected = int(key) - 1
                elif key == readchar.key.UP:
                    log_selected = (log_selected - 1) % 9
                elif key == readchar.key.DOWN:
                    log_selected = (log_selected + 1) % 9
                elif key == readchar.key.ENTER or key == "\r" or key == "\n":
                    if log_selected < unlocked_logs:
                        console.clear()
                        console.print(f"[bold green]LOG {log_selected+1} CONTENT:[/bold green]")
                        console.print(LOGS[log_selected])
                        console.print("\n[dim]Press ESC to return to logs.[/dim]")
                        while True:
                            if readchar.readkey() == readchar.key.ESC:
                                break
                elif key == readchar.key.ESC:
                    break
        # Mission terminal
        while True:
            console.clear()
            console.print(Panel.fit(Text(BANNER, style="bold cyan"), border_style="cyan"))
            fake_connection_sequence(console)
            console.print(f"[bold]INITIAL DIAGNOSTICS REQUIRED, Operator {operator_name}.[/bold]")
            console.print("- TYPE 'HELP' FOR COMMANDS.")
            console.print("- TYPE 'START' TO INITIALISE MISSION SEQUENCE.")
            console.print("- TYPE 'QUIT' TO EXIT.\n")
            cmd = console.input(f"[cyan]{operator_name}@AE>[/cyan] ").strip().lower()
            if cmd in ("quit", "exit"):
                console.print(f"[red]SESSION TERMINATED. SAFE TRAVELS, OPERATOR {operator_name}.[/red]")
                return
            elif cmd == "help":
                console.print("AVAILABLE: HELP, START, QUIT")
            elif cmd == "start":
                # Show mission instructions and prompt for answer
                while current_mission < unlocked_logs:
                    console.clear()
                    console.print(f"[bold yellow]MISSION {current_mission+1} INSTRUCTIONS:[/bold yellow]")
                    console.print(mission_instructions[current_mission])
                    answer = console.input("\n[cyan]Enter your answer (or type ESC to return): [/cyan]").strip()
                    if answer.lower() == "esc":
                        break
                    # Placeholder for validation/unit test
                    if answer == mission_answers[current_mission]:
                        console.print(f"[green]Correct! Mission Key: {mission_keys[current_mission]}[/green]")
                        unlocked_logs = max(unlocked_logs, current_mission+2)
                        current_mission += 1
                        break
                    else:
                        console.print("[red]Incorrect. Try again or type ESC to return.[/red]")
            elif cmd == "":
                continue
            elif cmd == "\x1b":  # ESC key
                break
            else:
                console.print(f"[yellow]UNRECOGNISED COMMAND:[/yellow] {cmd.upper()}")

if __name__ == "__main__":
    main()