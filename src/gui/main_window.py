"""
Main Window for Instagram Automation Tool
100% FREE - Only Instagram Login Required!
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QMessageBox, QFileDialog,
    QTextEdit, QTabWidget, QGroupBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from gui.login_dialog import LoginDialog
from gui.schedule_dialog import SchedulePostDialog
from core.instagram_client import get_instagram_client
from core.scheduler import get_scheduler
from utils.logger import get_logger
from utils.config import get_config

logger = get_logger()

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.config = get_config()
        self.instagram_client = get_instagram_client()
        self.scheduler = get_scheduler()
        
        # Start scheduler
        self.scheduler.start()
        
        self.init_ui()
        
        # Auto-refresh scheduled posts
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_scheduled_posts)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
        
        # Show login dialog on startup
        self.show_login()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Instagram Automation - 100% FREE!")
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel("📸 Instagram Automation")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        header.setFont(font)
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        # Login status
        self.status_label = QLabel("Not logged in")
        self.status_label.setStyleSheet("color: red; font-size: 12px;")
        header_layout.addWidget(self.status_label)
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.show_login)
        header_layout.addWidget(self.login_btn)
        
        main_layout.addLayout(header_layout)
        
        # FREE badge
        free_label = QLabel("✅ 100% FREE - No API Keys Required!")
        free_label.setAlignment(Qt.AlignCenter)
        free_label.setStyleSheet("color: green; font-size: 14px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(free_label)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Quick Post
        post_tab = self.create_post_tab()
        self.tabs.addTab(post_tab, "📤 Quick Post")
        
        # Tab 2: Scheduled Posts
        schedule_tab = self.create_schedule_tab()
        self.tabs.addTab(schedule_tab, "📅 Scheduled Posts")
        
        # Tab 3: Info
        info_tab = self.create_info_tab()
        self.tabs.addTab(info_tab, "ℹ️ Info")
        
        main_layout.addWidget(self.tabs)
        
        logger.info("Main window initialized")
    
    def create_post_tab(self):
        """Create quick post tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Post type buttons
        type_group = QGroupBox("Select Post Type")
        type_layout = QHBoxLayout(type_group)
        
        self.photo_btn = QPushButton("📷 Photo")
        self.photo_btn.setMinimumHeight(60)
        self.photo_btn.clicked.connect(lambda: self.quick_post('photo'))
        type_layout.addWidget(self.photo_btn)
        
        self.video_btn = QPushButton("🎥 Video/Reel")
        self.video_btn.setMinimumHeight(60)
        self.video_btn.clicked.connect(lambda: self.quick_post('video'))
        type_layout.addWidget(self.video_btn)
        
        self.story_btn = QPushButton("📖 Story")
        self.story_btn.setMinimumHeight(60)
        self.story_btn.clicked.connect(lambda: self.quick_post('story'))
        type_layout.addWidget(self.story_btn)
        
        layout.addWidget(type_group)
        
        # Schedule Button
        schedule_btn = QPushButton("📅 Schedule Post for Later")
        schedule_btn.setMinimumHeight(50)
        schedule_btn.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6c3483;
            }
        """)
        schedule_btn.clicked.connect(self.show_schedule_dialog)
        layout.addWidget(schedule_btn)
        
        # Caption
        caption_group = QGroupBox("Caption (for Photo/Video posts)")
        caption_layout = QVBoxLayout(caption_group)
        
        self.caption_input = QTextEdit()
        self.caption_input.setPlaceholderText("Enter your caption here... (optional)\n\nYou can add:\n- Text\n- Hashtags #like #this\n- Emojis 😊")
        self.caption_input.setMaximumHeight(150)
        caption_layout.addWidget(self.caption_input)
        
        layout.addWidget(caption_group)
        
        # Instructions
        instructions = QLabel(
            "📝 How to use:\n\n"
            "1. Click 'Login' to connect your Instagram account\n"
            "2. Choose post type (Photo, Video/Reel, or Story)\n"
            "3. Select your media file\n"
            "4. Add caption (optional for photos/videos)\n"
            "5. Post instantly!\n\n"
            "✅ Works 100% FREE - just your Instagram login!"
        )
        instructions.setStyleSheet("background-color: #f0f0f0; padding: 15px; border-radius: 5px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        layout.addStretch()
        
        return widget
    
    def create_info_tab(self):
        """Create info tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_text = QLabel(
            "<h2>Instagram Automation - 100% FREE!</h2>"
            "<p><b>What you can do:</b></p>"
            "<ul>"
            "<li>✅ Post photos to your feed</li>"
            "<li>✅ Post videos and reels</li>"
            "<li>✅ Post stories (photo and video)</li>"
            "<li>✅ Add captions and hashtags</li>"
            "<li>✅ Schedule posts for later (NEW!)</li>"
            "<li>✅ Recurring schedules - daily/weekly/monthly (NEW!)</li>"
            "</ul>"
            "<p><b>What you need:</b></p>"
            "<ul>"
            "<li>✅ Just your Instagram username and password</li>"
            "<li>✅ NO API keys required</li>"
            "<li>✅ NO monthly fees</li>"
            "<li>✅ Completely FREE!</li>"
            "</ul>"
            "<p><b>Coming soon:</b></p>"
            "<ul>"
            "<li>📊 Post history and analytics</li>"
            "<li>🖼️ Image editing tools</li>"
            "<li>📱 Multiple account support</li>"
            "</ul>"
            "<p><b>Security:</b></p>"
            "<ul>"
            "<li>🔒 Your credentials are stored locally</li>"
            "<li>🔒 Sessions are encrypted</li>"
            "<li>🔒 No data sent to third parties</li>"
            "</ul>"
            "<p style='color: gray; font-size: 11px; margin-top: 20px;'>"
            "⚠️ Use responsibly and follow Instagram's terms of service.<br>"
            "This tool automates posting to your own account.</p>"
        )
        info_text.setWordWrap(True)
        info_text.setTextFormat(Qt.RichText)
        
        layout.addWidget(info_text)
        layout.addStretch()
        
        return widget
    
    def show_login(self):
        """Show login dialog"""
        dialog = LoginDialog(self)
        if dialog.exec_():
            # Login successful
            self.update_login_status()
            QMessageBox.information(
                self,
                "Login Successful",
                f"Welcome! You're now logged in.\n\n"
                f"You can now start posting to Instagram!"
            )
    
    def update_login_status(self):
        """Update login status display"""
        if self.instagram_client.is_logged_in:
            self.status_label.setText(f"✅ Logged in as: {self.instagram_client.username}")
            self.status_label.setStyleSheet("color: green; font-size: 12px; font-weight: bold;")
            self.login_btn.setText("Logout")
            self.login_btn.clicked.disconnect()
            self.login_btn.clicked.connect(self.handle_logout)
        else:
            self.status_label.setText("❌ Not logged in")
            self.status_label.setStyleSheet("color: red; font-size: 12px;")
            self.login_btn.setText("Login")
            try:
                self.login_btn.clicked.disconnect()
            except:
                pass
            self.login_btn.clicked.connect(self.show_login)
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.instagram_client.logout()
            self.update_login_status()
            QMessageBox.information(self, "Logged Out", "You have been logged out successfully.")
    
    def quick_post(self, post_type):
        """Handle quick post"""
        if not self.instagram_client.is_logged_in:
            QMessageBox.warning(
                self,
                "Not Logged In",
                "Please login first to post to Instagram!"
            )
            self.show_login()
            return
        
        # File dialog based on type
        if post_type == 'photo' or post_type == 'story':
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Image",
                "",
                "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
            )
        else:  # video
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Video",
                "",
                "Videos (*.mp4 *.mov *.avi *.mkv)"
            )
        
        if not file_path:
            return  # User cancelled
        
        caption = self.caption_input.toPlainText().strip()
        
        # Post based on type
        result = None
        
        if post_type == 'photo':
            result = self.instagram_client.post_photo(file_path, caption)
        elif post_type == 'video':
            result = self.instagram_client.post_video(file_path, caption)
        elif post_type == 'story':
            if file_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                result = self.instagram_client.post_story_video(file_path)
            else:
                result = self.instagram_client.post_story_photo(file_path)
        
        # Show result
        if result and result.get('success'):
            QMessageBox.information(
                self,
                "Success!",
                f"✅ {result.get('message')}\n\n"
                f"Your {post_type} has been posted to Instagram!"
            )
            self.caption_input.clear()
        else:
            QMessageBox.critical(
                self,
                "Failed",
                f"❌ {result.get('message') if result else 'Unknown error'}"
            )
    
    def create_schedule_tab(self):
        """Create scheduled posts tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Scheduled Posts")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_scheduled_posts)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels([
            "ID", "Type", "Caption", "Scheduled Time", "Status"
        ])
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.schedule_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.schedule_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("❌ Cancel Selected")
        cancel_btn.clicked.connect(self.cancel_selected_post)
        button_layout.addWidget(cancel_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Info
        info = QLabel(
            "💡 Tip: Posts will be automatically published at their scheduled times.\n"
            "Keep this application running in the background for scheduled posts to work!"
        )
        info.setStyleSheet("background-color: #e3f2fd; padding: 10px; border-radius: 5px; color: #1976d2;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Load scheduled posts
        self.refresh_scheduled_posts()
        
        return widget
    
    def show_schedule_dialog(self):
        """Show schedule post dialog"""
        if not self.instagram_client.is_logged_in:
            QMessageBox.warning(
                self,
                "Not Logged In",
                "Please login first to schedule posts!"
            )
            self.show_login()
            return
        
        dialog = SchedulePostDialog(self)
        if dialog.exec_():
            # Refresh the scheduled posts table
            self.refresh_scheduled_posts()
            self.tabs.setCurrentIndex(1)  # Switch to scheduled posts tab
    
    def refresh_scheduled_posts(self):
        """Refresh scheduled posts table"""
        try:
            posts = self.scheduler.get_scheduled_posts(100)
            
            self.schedule_table.setRowCount(len(posts))
            
            for row, post in enumerate(posts):
                self.schedule_table.setItem(row, 0, QTableWidgetItem(str(post['id'])))
                self.schedule_table.setItem(row, 1, QTableWidgetItem(post['type']))
                self.schedule_table.setItem(row, 2, QTableWidgetItem(post['caption']))
                self.schedule_table.setItem(row, 3, QTableWidgetItem(post['scheduled_time']))
                
                status_item = QTableWidgetItem(post['status'])
                if post['status'] == 'scheduled':
                    status_item.setForeground(Qt.blue)
                self.schedule_table.setItem(row, 4, status_item)
                
        except Exception as e:
            logger.error(f"Error refreshing scheduled posts: {e}")
    
    def cancel_selected_post(self):
        """Cancel selected scheduled post"""
        selected_rows = self.schedule_table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a post to cancel!")
            return
        
        row = selected_rows[0].row()
        post_id = int(self.schedule_table.item(row, 0).text())
        
        reply = QMessageBox.question(
            self,
            "Cancel Post",
            "Are you sure you want to cancel this scheduled post?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = self.scheduler.cancel_post(post_id)
            
            if result.get('success'):
                QMessageBox.information(self, "Success", "Post cancelled successfully!")
                self.refresh_scheduled_posts()
            else:
                QMessageBox.critical(self, "Failed", result.get('message', 'Failed to cancel post'))
    
    def closeEvent(self, event):
        """Handle window close"""
        # Scheduler will keep running in background
        logger.info("Application closed (scheduler still running)")
        event.accept()

