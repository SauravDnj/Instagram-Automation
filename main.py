"""
Instagram Automation Tool - Main Entry Point
Author: Instagram Automation Team
Description: Professional Instagram automation with scheduling and AI image generation
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_window import MainWindow
from utils.logger import setup_logger
from utils.config import Config

def main():
    """Main application entry point"""
    # Initialize logger
    logger = setup_logger()
    logger.info("Starting Instagram Automation Tool")
    
    # Load configuration
    config = Config()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Instagram Automation")
    app.setOrganizationName("InstaAutomate")
    
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    logger.info("Application started successfully")
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
