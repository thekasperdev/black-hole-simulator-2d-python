import readchar
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from time import sleep

BANNER = """
---------------------------------------------------------------------
SPACE-D ENGINEERING AE-DOS OPERATING SYSTEM (AUTONOMOUS EXPERIMENTAL)
---------------------------------------------------------------------
TECH SYNC: BLACK HOLE SIMULATION TERMINAL | ALPHA-PREVIEW 0.9a (DO NOT PUSH TO PROD)
"""


def clear_screen_completely(console):
    """Clear screen completely to prevent scrollback issues."""
    # Multiple methods to ensure complete clearing across different terminals
    os.system('clear' if os.name == 'posix' else 'cls')  # System clear
    console.clear()  # Rich console clear
    
    # ANSI escape sequences for extra thorough clearing
    print("\033[2J\033[H", end="")  # Clear screen and move cursor to top
    print("\033[3J", end="")  # Clear scrollback buffer (if supported)
    sys.stdout.flush()
    
    # Position cursor at top-left
    print("\033[1;1H", end="")


def get_operator_name(console):
    """Prompt for operator name and return it, always visible at bottom."""
    while True:
        console.clear()
        console.print("[bold cyan]SPACE-D ENGINEERING AE-DOS OPERATING SYSTEM[/bold cyan]\n")
        console.print("[cyan]Please enter your name, operator: [/cyan]", end="")
        try:
            name = input().strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[red]Operation cancelled.[/red]")
            exit(0)
        if name:
            console.print(f"\n[green]Welcome aboard, Operator {name}.[/green]")
            console.print("[red]Access granted. Clearance level: COSMIC-7[/red]\n")
            return name
        else:
            console.print("[red]Please enter a valid name![/red]")


def fake_connection_sequence(console):
    """Show fake probe connection sequence with progress bar and logs."""
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
        console.print(log)
        sleep(0.22)
    sleep(0.5)

def load_log_content(log_number):
    """Load log content from file."""
    try:
        with open(f"logs/log{log_number}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: Log {log_number} file not found."


def load_mission_briefing(mission_number):
    """Load mission briefing content from file."""
    try:
        with open(f"mission_briefing/mission{mission_number}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: Mission {mission_number} briefing file not found."


def show_mission_briefing(console, operator_name, mission_number):
    """Show the mission briefing after viewing a log."""
    console.clear()
    console.print("[bold cyan]MISSION BRIEFING: Probe connection initiated.[/bold cyan]")
    fake_connection_sequence(console)
    console.print("\n[bold magenta]Probe link established. Receiving mission objective...[/bold magenta]\n")
    
    # Load and display mission briefing
    briefing_content = load_mission_briefing(mission_number)
    console.print(Panel.fit(Text(briefing_content, style="white"), border_style="yellow", title=f"[bold cyan]MISSION {mission_number}[/bold cyan]"))
    
    console.print(f"\n[bold]Good luck, Operator {operator_name}![/bold]")
    console.print(f"\n[dim]Press 'R' to return, 'L' for logs menu, 'M' for missions menu, or 'Q' to quit.[/dim]")
    while True:
        try:
            key = readchar.readkey()
        except (KeyboardInterrupt, EOFError):
            break
        if key.lower() == "r":
            # Return to previous context (will be handled by the calling function)
            return "return_to_log"
        elif key.lower() == "l":
            return "logs_menu"
        elif key.lower() == "m":
            return "missions_menu"
        elif key.lower() == "q":
            sys.exit(0)  # Quit application


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
    menu_items = ["LOGS", "MISSIONS", "EXIT"]
    selected = 0

    def print_menu(selected_idx):
        for idx, item in enumerate(menu_items):
            if idx == selected_idx:
                console.print(f"[black on yellow]➤ {idx+1}) {item}[/black on yellow]")
            else:
                console.print(f"  {idx+1}) {item}")

    while True:
        clear_screen_completely(console)
        console.print(f"[bold cyan]{logo}[/bold cyan]")
        console.print("[bold magenta]AE-DOS OPERATING SYSTEM[/bold magenta]\n")
        console.print("[bold]Select an option:[/bold]\n")
        print_menu(selected)
        console.print("\n[dim]Use ↑/↓ arrows or 1/2/3 to navigate, ENTER to select. Press 'L' for logs, 'M' for missions, 'Q' to quit.[/dim]")
        try:
            key = readchar.readkey()
        except (KeyboardInterrupt, EOFError):
            return "esc"
        
        if key in ("1", "2", "3"):
            selected = int(key) - 1
            return selected
        elif key == readchar.key.UP or key == "w":
            selected = (selected - 1) % len(menu_items)
        elif key == readchar.key.DOWN or key == "s":
            selected = (selected + 1) % len(menu_items)
        elif key == readchar.key.ENTER or key == "\r" or key == "\n":
            return selected
        elif key.lower() == "l":
            return 0  # Logs option
        elif key.lower() == "m":
            return 1  # Missions option
        elif key.lower() == "q":
            return "esc"  # Quit


def show_logs_menu(console, operator_name, unlocked_logs):
    """Display logs menu and handle log selection."""
    log_selected = 0
    while True:
        console.clear()
        console.print("[bold cyan]AE-DOS LOGS[/bold cyan]\n")
        for i in range(9):
            if i < unlocked_logs:
                if i == log_selected:
                    console.print(f"[black on green]➤ {i+1}) LOG {i+1}: Decrypted. Mission {i+1} available.[/black on green]")
                else:
                    console.print(f"[green]  {i+1}) LOG {i+1}: Decrypted. Mission {i+1} available.[/green]")
            else:
                if i == log_selected:
                    console.print(f"[black on yellow]➤ {i+1}) LOG {i+1}: [ENCRYPTED] - Requires Mission Key {i+1}[/black on yellow]")
                else:
                    console.print(f"[yellow]  {i+1}) LOG {i+1}: [ENCRYPTED] - Requires Mission Key {i+1}[/yellow]")
        console.print("\n[dim]Use ↑/↓ arrows or 1-9 to navigate, ENTER to view log. Press 'M' for main menu, 'Q' to quit.[/dim]")
        try:
            key = readchar.readkey()
        except (KeyboardInterrupt, EOFError):
            break
            
        if key in "123456789":
            log_selected = int(key) - 1
            if log_selected < unlocked_logs:
                # Direct selection with number key - view the log
                pass  # Continue to log viewing code
            else:
                continue  # Invalid selection, stay in menu
        elif key == readchar.key.UP:
            log_selected = (log_selected - 1) % 9
            continue
        elif key == readchar.key.DOWN:
            log_selected = (log_selected + 1) % 9
            continue
        elif key == readchar.key.ENTER or key == "\r" or key == "\n":
            if log_selected < unlocked_logs:
                # ENTER pressed on valid selection - view the log
                pass  # Continue to log viewing code
            else:
                continue  # Invalid selection, stay in menu
        elif key.lower() == "m":
            break  # Return to main menu
        elif key.lower() == "q":
            return  # Quit application
        else:
            continue  # Invalid key, stay in menu
            
        # If we reach here, we have a valid log selection to view
        if log_selected < unlocked_logs:
                # Show log content with better clearing
                clear_screen_completely(console)
                console.print(f"[bold green]LOG {log_selected+1} CONTENT:[/bold green]\n")
                log_content = load_log_content(log_selected + 1)
                console.print(log_content)
                console.print("\n[dim]Press ENTER to continue to mission briefing, 'R' to return to logs, 'L' for logs, 'M' for missions, or 'Q' to quit.[/dim]")
                while True:
                    try:
                        key = readchar.readkey()
                    except (KeyboardInterrupt, EOFError):
                        return
                    if key == readchar.key.ENTER or key == "\r" or key == "\n":
                        break  # Continue to mission briefing
                    elif key.lower() == "r":
                        return  # Return to logs menu
                    elif key.lower() == "l":
                        return  # Return to logs menu
                    elif key.lower() == "m":
                        return "missions_menu"  # Go to missions menu
                    elif key.lower() == "q":
                        sys.exit(0)  # Quit application
                
                # Show mission briefing after log and handle its return value
                briefing_result = show_mission_briefing(console, operator_name, log_selected + 1)
                if briefing_result == "return_to_log":
                    # Stay in this log view
                    continue
                elif briefing_result == "logs_menu":
                    return  # Return to logs menu
                elif briefing_result == "missions_menu":
                    return "missions_menu"  # Go to missions menu
        elif key.lower() == "m":
            break


def show_fake_boot_logs(console):
    """Show fake boot sequence."""
    boot_logs = [
        "[dim]AE-DOS BIOS v1.42 initializing...[/dim]",
        "[dim]Memory check: 16384K OK[/dim]",
        "[dim]Quantum processor: ACTIVE[/dim]",
        "[dim]Reality.dll: LOADED[/dim]",
        "[dim]Physics engine: PROBABLY WORKING[/dim]",
        "[dim]Coffee machine driver: CRITICAL_ERROR (priorities people!)[/dim]",
        "[dim]Sarcasm module: LOADED AND READY[/dim]",
        "[dim]Common sense driver: NOT FOUND (working as intended)[/dim]",
        "[dim]Murphy's Law compliance: 100%[/dim]",
        "[dim]Loading procrastination.exe... please wait...[/dim]",
        "[dim]Existential dread buffer: INITIALIZED[/dim]",
        "[dim]Mounting /dev/null: Successfully discarded everything[/dim]",
        "[dim]Loading sense_of_humor.dll: Version DARK_AND_TWISTED[/dim]",
        "[dim]All systems nominal. Boot sequence complete.[/dim]",
        "[green]Welcome to AE-DOS![/green]"
    ]
    for log in boot_logs:
        console.print(log)
        sleep(0.3)
    sleep(0.7)


def show_missions_menu(console, operator_name, unlocked_logs):
    """Display missions overview menu."""
    mission_selected = 0
    while True:
        console.clear()
        console.print("[bold cyan]AE-DOS MISSIONS OVERVIEW[/bold cyan]\n")
        for i in range(9):
            if i < unlocked_logs:
                if i == mission_selected:
                    console.print(f"[black on green]➤ {i+1}) MISSION {i+1}: Available[/black on green]")
                else:
                    console.print(f"[green]  {i+1}) MISSION {i+1}: Available[/green]")
            else:
                if i == mission_selected:
                    console.print(f"[black on yellow]➤ {i+1}) MISSION {i+1}: Locked[/black on yellow]")
                else:
                    console.print(f"[yellow]  {i+1}) MISSION {i+1}: Locked[/yellow]")
        console.print("\n[dim]Use ↑/↓ arrows or 1-9 to navigate, ENTER to select mission. Press 'L' for logs, 'R' to return, 'Q' to quit.[/dim]")
        
        try:
            key = readchar.readkey()
        except (KeyboardInterrupt, EOFError):
            break
            
        if key in "123456789":
            mission_selected = int(key) - 1
            if mission_selected < unlocked_logs:
                # Direct selection with number key - show mission briefing
                pass  # Continue to mission viewing code
            else:
                continue  # Invalid selection, stay in menu
        elif key == readchar.key.UP:
            mission_selected = (mission_selected - 1) % 9
            continue
        elif key == readchar.key.DOWN:
            mission_selected = (mission_selected + 1) % 9
            continue
        elif key == readchar.key.ENTER or key == "\r" or key == "\n":
            if mission_selected < unlocked_logs:
                # ENTER pressed on valid selection - show mission briefing
                pass  # Continue to mission viewing code
            else:
                continue  # Invalid selection, stay in menu
        elif key.lower() == "l":
            # Go to logs menu - need to return to main and then to logs
            return "logs_menu"
        elif key.lower() == "r":
            break  # Return to main menu
        elif key.lower() == "q":
            sys.exit(0)  # Quit application
        else:
            continue  # Invalid key, stay in menu
            
        # If we reach here, we have a valid mission selection to view
        if mission_selected < unlocked_logs:
            # Show mission briefing directly
            briefing_result = show_mission_briefing(console, operator_name, mission_selected + 1)
            if briefing_result == "return_to_log":
                # In missions context, return means go back to missions menu
                continue
            elif briefing_result == "logs_menu":
                return "logs_menu"
            elif briefing_result == "missions_menu":
                continue  # Stay in missions menu


def main():
    """Main application loop."""
    console = Console()
    console.clear()

    # Show fake boot logs first
    show_fake_boot_logs(console)
    console.clear()

    # Ask for operator name after boot
    operator_name = get_operator_name(console)

    # Mission and log system - start with all 9 logs unlocked for testing
    unlocked_logs = 9  # You can change this to 1 to start with only first log unlocked
    
    while True:
        # Show welcome menu and handle selection
        selected = show_welcome_menu(console, unlocked_logs)
        if selected == "esc" or selected == 2:
            console.print("[red]Exiting AE-DOS. Goodbye![/red]")
            return
        
        # LOGS menu
        if selected == 0:
            result = show_logs_menu(console, operator_name, unlocked_logs)
            if result == "missions_menu":
                # User pressed M in logs, show missions menu
                missions_result = show_missions_menu(console, operator_name, unlocked_logs)
                if missions_result == "logs_menu":
                    # User pressed L in missions, go back to logs
                    show_logs_menu(console, operator_name, unlocked_logs)
        # MISSIONS menu
        elif selected == 1:
            result = show_missions_menu(console, operator_name, unlocked_logs)
            if result == "logs_menu":
                # User pressed L in missions, show logs menu
                logs_result = show_logs_menu(console, operator_name, unlocked_logs)
                if logs_result == "missions_menu":
                    # User pressed M in logs, go back to missions
                    show_missions_menu(console, operator_name, unlocked_logs)

if __name__ == "__main__":
    main()