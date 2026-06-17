"""Terminal UI utilities."""
import os
import sys
import time
import threading
from colorama import init, Fore, Style

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
  ██╗   ██╗███████╗███╗   ███╗ █████╗ ███╗   ██╗
  ██║   ██║██╔════╝████╗ ████║██╔══██╗████╗  ██║
  ██║   ██║███████╗██╔████╔██║███████║██╔██╗ ██║
  ██║   ██║╚════██║██║╚██╔╝██║██╔══██║██║╚██╗██║
  ╚██████╔╝███████║██║ ╚═╝ ██║██║  ██║██║ ╚████║
   ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Fore.YELLOW}         TikTok Analyzer - Created By Muhammad Usman
{Style.RESET_ALL}
"""
    print(banner)

def print_success(msg):
    print(f"{Fore.GREEN}[✓] {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}[✗] {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.CYAN}[i] {msg}{Style.RESET_ALL}")

def print_warning(msg):
    print(f"{Fore.YELLOW}[!] {msg}{Style.RESET_ALL}")

class Spinner:
    """Simple spinner context manager."""
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.thread = None

    def _spin(self):
        symbols = ['|', '/', '-', '\\']
        idx = 0
        while self.running:
            sys.stdout.write(f"\r{Fore.CYAN}[{symbols[idx]}] {self.message}...{Style.RESET_ALL}")
            sys.stdout.flush()
            idx = (idx + 1) % len(symbols)
            time.sleep(0.1)
        # Clear line
        sys.stdout.write('\r' + ' ' * (len(self.message) + 20) + '\r')
        sys.stdout.flush()

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.thread:
            self.thread.join()
        return False

def menu_loop(analyzer, config, logger):
    """Main interactive menu."""
    while True:
        clear_screen()
        show_banner()
        print(f"\n{Fore.MAGENTA}╔══════════════════════╗")
        print(f"║       MAIN MENU      ║")
        print(f"╠══════════════════════╣")
        print(f"║ 1. Analyze Username  ║")
        print(f"║ 2. Generate Report   ║")
        print(f"║ 3. Help              ║")
        print(f"║ 4. Check for Updates ║")
        print(f"║ 5. Exit              ║")
        print(f"╚══════════════════════╝{Style.RESET_ALL}")

        choice = input(f"{Fore.CYAN}Select option (1-5): {Style.RESET_ALL}").strip()
        if choice == '1':
            username = input("Enter TikTok username (without @): ").strip()
            analyzer.analyze_username(username)
            input("\nPress Enter to continue...")
        elif choice == '2':
            username = input("Enter username for report: ").strip()
            if analyzer.validate_username(username):
                try:
                    profile = analyzer.fetch_profile(username)
                    json_path, txt_path = analyzer.generate_report(username, profile)
                    print_success(f"Reports saved:\n  {json_path}\n  {txt_path}")
                except Exception as e:
                    print_error(f"Report generation failed: {e}")
            else:
                print_error("Invalid username format.")
            input("\nPress Enter to continue...")
        elif choice == '3':
            show_help()
            input("\nPress Enter to continue...")
        elif choice == '4':
            from modules.updater import update_app
            update_app()
            input("\nPress Enter to continue...")
        elif choice == '5':
            print("Goodbye!")
            sys.exit(0)
        else:
            print_error("Invalid choice!")
            time.sleep(1)

def show_help():
    clear_screen()
    print(f"{Fore.YELLOW}USMAN TikTok Analyzer - Help{Style.RESET_ALL}")
    print("This tool lets you fetch public TikTok profile info and generate reports.")
    print("\nOptions:")
    print("  1. Analyze Username - Enter a username to view profile stats and save data.")
    print("  2. Generate Report   - Create fresh JSON/TXT reports for an already saved profile.")
    print("  3. Help              - Show this message.")
    print("  4. Check for Updates - Pull latest version from GitHub (requires git).")
    print("  5. Exit              - Quit the application.")
    print("\nReports are stored in the 'reports/' folder. Raw data in 'data/'.")
    print("Configuration can be changed in 'config/settings.ini'.")
