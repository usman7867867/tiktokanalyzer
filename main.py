#!/usr/bin/env python3
"""USMAN TikTok Analyzer - Main Entry Point."""
import os
import sys
import time
from modules.config_manager import load_config, get_setting
from modules.logger_setup import setup_logging
from modules.ui import show_banner, clear_screen, print_error, menu_loop
from modules.updater import check_for_updates
from modules.tiktok_analyzer import TikTokAnalyzer

def main():
    # Ensure project directories exist
    for folder in ['data', 'reports']:
        os.makedirs(folder, exist_ok=True)

    # Load configuration
    config = load_config()
    log_file = get_setting(config, 'Logging', 'log_file', fallback='data/app.log')
    log_level = get_setting(config, 'Logging', 'log_level', fallback='INFO')

    # Setup logging
    logger = setup_logging(log_file, log_level)
    logger.info("Application started")

    # Show banner
    clear_screen()
    show_banner()
    time.sleep(1)

    # Check for updates (optional, based on config)
    auto_check = get_setting(config, 'Updates', 'auto_check', fallback='true').lower() == 'true'
    if auto_check:
        update_available = check_for_updates()
        if update_available:
            print("\n[!] A new version is available. Use the update option in the menu.")
            time.sleep(2)

    # Start main menu
    analyzer = TikTokAnalyzer(config, logger)
    menu_loop(analyzer, config, logger)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
        sys.exit(0)
