"""
Login Dialog - Simple Instagram Login
Only needs username and password - 100% FREE!
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QCheckBox,
    QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from core.instagram_client import get_instagram_client
from utils.logger import get_logger

logger = get_logger()

class LoginWorker(QThread):
    """Background worker for login to keep UI responsive"""
    finished = pyqtSignal(dict)
    
    def __init__(self, username, password, verification_code=None):
        super().__init__()
        self.username = username
        self.password = password
        self.verification_code = verification_code
        
    def run(self):
        """Perform login in background"""
        client = get_instagram_client()
        result = client.login(self.username, self.password, self.verification_code)
        self.finished.emit(result)

class LoginDialog(QDialog):
    """Login dialog for Instagram authentication"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instagram Login - 100% FREE!")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self.login_worker = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Instagram Automation")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("100% FREE - No API Keys Required!")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: green; font-size: 12px;")
        layout.addWidget(subtitle)
        
        # Info
        info = QLabel("Just enter your Instagram username and password")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(info)
        
        layout.addSpacing(10)
        
        # Username field
        username_label = QLabel("Instagram Username:")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("your_username")
        self.username_input.setMinimumHeight(35)
        layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Instagram Password:")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("your_password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_input)
        
        # 2FA code field (initially hidden)
        self.twofa_label = QLabel("Two-Factor Code (if enabled):")
        self.twofa_label.hide()
        layout.addWidget(self.twofa_label)
        
        self.twofa_input = QLineEdit()
        self.twofa_input.setPlaceholderText("123456")
        self.twofa_input.setMinimumHeight(35)
        self.twofa_input.hide()
        self.twofa_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.twofa_input)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Remember me (save session)")
        self.remember_checkbox.setChecked(True)
        layout.addWidget(self.remember_checkbox)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0095f6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #007acc;
            }
            QPushButton:disabled {
                background-color: #b0b0b0;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(40)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        # Warning
        warning = QLabel("⚠️ Your credentials are stored locally and securely.\n"
                        "This app uses the official Instagram interface - no third-party APIs!")
        warning.setAlignment(Qt.AlignCenter)
        warning.setStyleSheet("color: gray; font-size: 9px; margin-top: 10px;")
        warning.setWordWrap(True)
        layout.addWidget(warning)
        
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validation
        if not username or not password:
            self.show_status("Please enter both username and password", error=True)
            return
        
        # Get 2FA code if visible
        verification_code = None
        if self.twofa_input.isVisible():
            verification_code = self.twofa_input.text().strip()
            if not verification_code:
                self.show_status("Please enter the 2FA code", error=True)
                return
        
        # Disable inputs during login
        self.set_inputs_enabled(False)
        self.progress_bar.show()
        self.show_status("Logging in...", info=True)
        
        # Perform login in background thread
        self.login_worker = LoginWorker(username, password, verification_code)
        self.login_worker.finished.connect(self.on_login_complete)
        self.login_worker.start()
    
    def on_login_complete(self, result):
        """Handle login completion"""
        self.progress_bar.hide()
        self.set_inputs_enabled(True)
        
        if result.get('success'):
            self.show_status(result.get('message'), success=True)
            # Wait a bit then close dialog
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(1000, self.accept)
            
        elif result.get('requires_2fa'):
            # Show 2FA input
            self.twofa_label.show()
            self.twofa_input.show()
            self.twofa_input.setFocus()
            self.show_status(result.get('message'), info=True)
            
        elif result.get('requires_challenge'):
            self.show_status(result.get('message'), error=True)
            QMessageBox.warning(
                self,
                "Security Challenge",
                "Instagram requires additional verification.\n\n"
                "Please:\n"
                "1. Open Instagram app on your phone\n"
                "2. Complete any security verification\n"
                "3. Try logging in again here"
            )
            
        else:
            self.show_status(result.get('message', 'Login failed'), error=True)
    
    def show_status(self, message, success=False, error=False, info=False):
        """Show status message with color"""
        self.status_label.setText(message)
        
        if success:
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        elif error:
            self.status_label.setStyleSheet("color: red;")
        elif info:
            self.status_label.setStyleSheet("color: blue;")
        else:
            self.status_label.setStyleSheet("color: black;")
    
    def set_inputs_enabled(self, enabled):
        """Enable/disable input fields"""
        self.username_input.setEnabled(enabled)
        self.password_input.setEnabled(enabled)
        self.twofa_input.setEnabled(enabled)
        self.login_button.setEnabled(enabled)
