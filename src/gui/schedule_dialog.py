"""
Schedule Post Dialog - Create scheduled posts
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QDateTimeEdit, QTextEdit, QComboBox,
    QFileDialog, QMessageBox, QGroupBox, QFormLayout,
    QRadioButton, QButtonGroup, QSpinBox
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta

from core.scheduler import get_scheduler
from database.models import PostType, ScheduleFrequency
from utils.logger import get_logger

logger = get_logger()

class SchedulePostDialog(QDialog):
    """Dialog for scheduling Instagram posts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule Post - FREE Instagram Automation")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        
        self.scheduler = get_scheduler()
        self.selected_file = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📅 Schedule Instagram Post")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Schedule Type
        type_group = QGroupBox("Schedule Type")
        type_layout = QVBoxLayout(type_group)
        
        self.schedule_type_group = QButtonGroup()
        
        self.one_time_radio = QRadioButton("One-Time Post (schedule for specific date/time)")
        self.one_time_radio.setChecked(True)
        self.one_time_radio.toggled.connect(self.on_schedule_type_changed)
        self.schedule_type_group.addButton(self.one_time_radio)
        type_layout.addWidget(self.one_time_radio)
        
        self.recurring_radio = QRadioButton("Recurring Schedule (daily/weekly/monthly)")
        self.recurring_radio.toggled.connect(self.on_schedule_type_changed)
        self.schedule_type_group.addButton(self.recurring_radio)
        type_layout.addWidget(self.recurring_radio)
        
        layout.addWidget(type_group)
        
        # One-time schedule options
        self.one_time_widget = QGroupBox("One-Time Schedule")
        one_time_layout = QFormLayout(self.one_time_widget)
        
        self.datetime_picker = QDateTimeEdit()
        self.datetime_picker.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.datetime_picker.setMinimumDateTime(QDateTime.currentDateTime().addSecs(60))
        self.datetime_picker.setCalendarPopup(True)
        self.datetime_picker.setDisplayFormat("yyyy-MM-dd HH:mm")
        one_time_layout.addRow("Schedule For:", self.datetime_picker)
        
        layout.addWidget(self.one_time_widget)
        
        # Recurring schedule options
        self.recurring_widget = QGroupBox("Recurring Schedule")
        recurring_layout = QFormLayout(self.recurring_widget)
        
        self.schedule_name_input = QTextEdit()
        self.schedule_name_input.setPlaceholderText("My Daily Post")
        self.schedule_name_input.setMaximumHeight(30)
        recurring_layout.addRow("Schedule Name:", self.schedule_name_input)
        
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(["Daily", "Weekly", "Monthly", "Yearly"])
        self.frequency_combo.currentTextChanged.connect(self.on_frequency_changed)
        recurring_layout.addRow("Frequency:", self.frequency_combo)
        
        # Time picker for recurring
        self.time_picker = QDateTimeEdit()
        self.time_picker.setDisplayFormat("HH:mm")
        self.time_picker.setTime(QDateTime.currentDateTime().time())
        recurring_layout.addRow("Time of Day:", self.time_picker)
        
        # Day of week (for weekly)
        self.day_of_week_combo = QComboBox()
        self.day_of_week_combo.addItems([
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ])
        self.day_of_week_label = QLabel("Day of Week:")
        recurring_layout.addRow(self.day_of_week_label, self.day_of_week_combo)
        self.day_of_week_combo.hide()
        self.day_of_week_label.hide()
        
        # Day of month (for monthly/yearly)
        self.day_of_month_spin = QSpinBox()
        self.day_of_month_spin.setRange(1, 31)
        self.day_of_month_spin.setValue(1)
        self.day_of_month_label = QLabel("Day of Month:")
        recurring_layout.addRow(self.day_of_month_label, self.day_of_month_spin)
        self.day_of_month_spin.hide()
        self.day_of_month_label.hide()
        
        # Month (for yearly)
        self.month_combo = QComboBox()
        self.month_combo.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.month_label = QLabel("Month:")
        recurring_layout.addRow(self.month_label, self.month_combo)
        self.month_combo.hide()
        self.month_label.hide()
        
        # Media folder for recurring
        media_folder_layout = QHBoxLayout()
        self.media_folder_input = QTextEdit()
        self.media_folder_input.setPlaceholderText("Select folder containing media files")
        self.media_folder_input.setMaximumHeight(30)
        media_folder_layout.addWidget(self.media_folder_input)
        
        browse_folder_btn = QPushButton("Browse...")
        browse_folder_btn.clicked.connect(self.select_media_folder)
        media_folder_layout.addWidget(browse_folder_btn)
        
        recurring_layout.addRow("Media Folder:", media_folder_layout)
        
        layout.addWidget(self.recurring_widget)
        self.recurring_widget.hide()
        
        # Post Type
        post_type_group = QGroupBox("Post Type")
        post_type_layout = QHBoxLayout(post_type_group)
        
        self.post_type_combo = QComboBox()
        self.post_type_combo.addItems(["Photo", "Video/Reel", "Story"])
        post_type_layout.addWidget(self.post_type_combo)
        
        layout.addWidget(post_type_group)
        
        # Media File (for one-time only)
        self.media_group = QGroupBox("Media File")
        media_layout = QHBoxLayout(self.media_group)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: gray;")
        media_layout.addWidget(self.file_label)
        
        select_file_btn = QPushButton("Select File")
        select_file_btn.clicked.connect(self.select_file)
        media_layout.addWidget(select_file_btn)
        
        layout.addWidget(self.media_group)
        
        # Caption
        caption_group = QGroupBox("Caption")
        caption_layout = QVBoxLayout(caption_group)
        
        self.caption_input = QTextEdit()
        self.caption_input.setPlaceholderText(
            "Enter your caption here...\n\n"
            "You can add:\n"
            "- Text and emojis 😊\n"
            "- Hashtags #like #this\n"
            "- Multiple lines"
        )
        self.caption_input.setMaximumHeight(120)
        caption_layout.addWidget(self.caption_input)
        
        layout.addWidget(caption_group)
        
        # Quick schedule buttons
        quick_group = QGroupBox("Quick Schedule")
        quick_layout = QHBoxLayout(quick_group)
        
        quick_1h_btn = QPushButton("In 1 Hour")
        quick_1h_btn.clicked.connect(lambda: self.set_quick_time(hours=1))
        quick_layout.addWidget(quick_1h_btn)
        
        quick_tomorrow_btn = QPushButton("Tomorrow 9 AM")
        quick_tomorrow_btn.clicked.connect(lambda: self.set_quick_time(days=1, hour=9))
        quick_layout.addWidget(quick_tomorrow_btn)
        
        quick_week_btn = QPushButton("Next Week")
        quick_week_btn.clicked.connect(lambda: self.set_quick_time(days=7))
        quick_layout.addWidget(quick_week_btn)
        
        layout.addWidget(quick_group)
        self.quick_group = quick_group
        
        # Buttons
        button_layout = QHBoxLayout()
        
        schedule_btn = QPushButton("Schedule Post")
        schedule_btn.setMinimumHeight(40)
        schedule_btn.setStyleSheet("""
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
        """)
        schedule_btn.clicked.connect(self.handle_schedule)
        button_layout.addWidget(schedule_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def on_schedule_type_changed(self):
        """Handle schedule type change"""
        is_one_time = self.one_time_radio.isChecked()
        
        self.one_time_widget.setVisible(is_one_time)
        self.recurring_widget.setVisible(not is_one_time)
        self.media_group.setVisible(is_one_time)
        self.quick_group.setVisible(is_one_time)
    
    def on_frequency_changed(self, frequency):
        """Handle frequency change"""
        # Hide all extra fields first
        self.day_of_week_combo.hide()
        self.day_of_week_label.hide()
        self.day_of_month_spin.hide()
        self.day_of_month_label.hide()
        self.month_combo.hide()
        self.month_label.hide()
        
        # Show relevant fields
        if frequency == "Weekly":
            self.day_of_week_combo.show()
            self.day_of_week_label.show()
        elif frequency == "Monthly":
            self.day_of_month_spin.show()
            self.day_of_month_label.show()
        elif frequency == "Yearly":
            self.day_of_month_spin.show()
            self.day_of_month_label.show()
            self.month_combo.show()
            self.month_label.show()
    
    def select_file(self):
        """Select media file"""
        post_type = self.post_type_combo.currentText()
        
        if "Video" in post_type or "Story" in post_type:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Media File",
                "",
                "All Media (*.jpg *.jpeg *.png *.mp4 *.mov);;Images (*.jpg *.jpeg *.png);;Videos (*.mp4 *.mov)"
            )
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Image",
                "",
                "Images (*.jpg *.jpeg *.png *.gif *.bmp)"
            )
        
        if file_path:
            self.selected_file = file_path
            import os
            self.file_label.setText(os.path.basename(file_path))
            self.file_label.setStyleSheet("color: green; font-weight: bold;")
    
    def select_media_folder(self):
        """Select media folder for recurring posts"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Media Folder",
            ""
        )
        
        if folder:
            self.media_folder_input.setText(folder)
    
    def set_quick_time(self, hours=0, days=0, hour=None):
        """Set quick schedule time"""
        dt = datetime.now() + timedelta(hours=hours, days=days)
        if hour is not None:
            dt = dt.replace(hour=hour, minute=0, second=0)
        
        self.datetime_picker.setDateTime(QDateTime.fromString(
            dt.strftime("%Y-%m-%d %H:%M"),
            "yyyy-MM-dd HH:mm"
        ))
    
    def handle_schedule(self):
        """Handle schedule button click"""
        caption = self.caption_input.toPlainText().strip()
        
        # Get post type
        post_type_text = self.post_type_combo.currentText()
        if "Photo" in post_type_text:
            post_type = PostType.IMAGE
        elif "Video" in post_type_text or "Reel" in post_type_text:
            post_type = PostType.REEL
        else:
            post_type = PostType.STORY
        
        if self.one_time_radio.isChecked():
            # One-time schedule
            if not self.selected_file:
                QMessageBox.warning(self, "No File", "Please select a media file!")
                return
            
            scheduled_time = self.datetime_picker.dateTime().toPyDateTime()
            
            result = self.scheduler.schedule_post(
                media_path=self.selected_file,
                post_type=post_type,
                caption=caption,
                scheduled_time=scheduled_time
            )
            
            if result.get('success'):
                QMessageBox.information(
                    self,
                    "Success!",
                    f"✅ {result.get('message')}\n\n"
                    f"Your post will be published automatically!"
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Failed",
                    f"❌ {result.get('message')}"
                )
        else:
            # Recurring schedule
            schedule_name = self.schedule_name_input.toPlainText().strip()
            media_folder = self.media_folder_input.toPlainText().strip()
            
            if not schedule_name:
                QMessageBox.warning(self, "No Name", "Please enter a schedule name!")
                return
            
            if not media_folder:
                QMessageBox.warning(self, "No Folder", "Please select a media folder!")
                return
            
            # Get frequency
            freq_text = self.frequency_combo.currentText()
            frequency_map = {
                "Daily": ScheduleFrequency.DAILY,
                "Weekly": ScheduleFrequency.WEEKLY,
                "Monthly": ScheduleFrequency.MONTHLY,
                "Yearly": ScheduleFrequency.YEARLY
            }
            frequency = frequency_map[freq_text]
            
            time_of_day = self.time_picker.time().toString("HH:mm")
            
            day_of_week = self.day_of_week_combo.currentIndex() if freq_text == "Weekly" else None
            day_of_month = self.day_of_month_spin.value() if freq_text in ["Monthly", "Yearly"] else None
            month = self.month_combo.currentIndex() + 1 if freq_text == "Yearly" else None
            
            result = self.scheduler.create_recurring_schedule(
                name=schedule_name,
                post_type=post_type,
                frequency=frequency,
                time_of_day=time_of_day,
                caption_template=caption,
                media_folder=media_folder,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                month=month
            )
            
            if result.get('success'):
                QMessageBox.information(
                    self,
                    "Success!",
                    f"✅ {result.get('message')}\n\n"
                    f"Posts will be published automatically according to schedule!"
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Failed",
                    f"❌ {result.get('message')}"
                )
