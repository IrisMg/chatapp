from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt, pyqtSignal

class HeaderWidget(QFrame):
    dashboard_clicked = pyqtSignal()

    def __init__(self, title="Privacy Assistant", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {          
                background-color: #1565C0;  /* dark blue */
                color: white;
                padding: 10px;
            }
            QLabel { color: white; }
        """)
        layout = QHBoxLayout()
        self.label = QLabel(title)
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.label.mousePressEvent = self.on_click
        layout.addWidget(self.label)
        layout.addStretch()
        self.setLayout(layout)

    def on_click(self, event):
        self.dashboard_clicked.emit()


class DashboardPage(QWidget):
    start_clicked = pyqtSignal()

    def __init__(self, user_name="User", parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header = HeaderWidget()
        main_layout.addWidget(header)

        # --- Start Section ---
        start_frame = QFrame()
        start_frame.setStyleSheet("""
            QFrame {
                background-color: #BBDEFB;
                border-radius: 10px;
            }
        """)
        start_layout = QVBoxLayout()
        start_layout.setSpacing(20)
        start_layout.setContentsMargins(30, 30, 30, 30)

        start_title = QLabel("Start Your Privacy Assistant")
        start_title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        start_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_desc = QLabel(
            "Get personalized Privacy Enhancing Tools recommendations based on your knowledge level and specific concerns."
        )
        start_desc.setFont(QFont("Arial", 14))
        start_desc.setWordWrap(True)
        start_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_time = QLabel("Takes approximately 5-15 minutes.")
        start_time.setFont(QFont("Arial", 12))
        start_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(200)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0D47A1;
            }
        """)
        self.start_button.clicked.connect(self.start_clicked.emit)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()

        start_layout.addWidget(start_title)
        start_layout.addWidget(start_desc)
        start_layout.addWidget(start_time)
        start_layout.addLayout(button_layout)
        start_frame.setLayout(start_layout)
        main_layout.addWidget(start_frame)

        # --- Assessment Section ---
        assessment_box = QFrame()
        assessment_box.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        assessment_layout = QVBoxLayout()
        assessment_layout.setSpacing(20)

        box_title = QLabel("📖 How the Assessment Works")
        box_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        box_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        assessment_layout.addWidget(box_title)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        cards_info = [
            ("Share Background", "Tell us about your privacy background.", "👤"),
            ("Answer Awareness Questions", "Discuss your specific privacy concerns.", "❓"),
            ("Learning or Recommendations", "Receive personalized privacy guidance.", "✔️"),
        ]

        for title, desc, emoji in cards_info:
            card = self.create_card(title, desc, emoji)
            cards_layout.addWidget(card)

        assessment_layout.addLayout(cards_layout)
        assessment_box.setLayout(assessment_layout)
        main_layout.addWidget(assessment_box)

        # --- What You'll Learn ---
        learn_box = QFrame()
        learn_box.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        learn_layout = QVBoxLayout()
        learn_layout.setSpacing(15)

        learn_title = QLabel("🔒 What You'll Learn")
        learn_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        learn_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        learn_layout.addWidget(learn_title)

        inner_box = QFrame()
        inner_box.setStyleSheet("""
            QFrame {
                background-color: #64B5F6;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        inner_layout = QVBoxLayout()
        inner_layout.setSpacing(8)

        bullet_points = [
            "Browser Fingerprinting",
            "Location Tracking by Apps",
            "Unprotected File Sharing Links",
            "Using Public Wi-Fi Without Protection"
        ]

        for point in bullet_points:
            lbl = QLabel(f"• {point}")
            lbl.setFont(QFont("Arial", 12))
            lbl.setStyleSheet("color: white;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
            lbl.setWordWrap(True)
            inner_layout.addWidget(lbl)

        inner_box.setLayout(inner_layout)
        learn_layout.addWidget(inner_box)
        learn_box.setLayout(learn_layout)
        main_layout.addWidget(learn_box)

        main_layout.addStretch()

        # --- Make Scrollable ---
        container = QWidget()
        container.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        final_layout = QVBoxLayout(self)
        final_layout.addWidget(scroll)

    def create_card(self, title, description, emoji):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #64B5F6;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        frame.setMinimumWidth(200)
        frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        avatar = QLabel(emoji)
        avatar.setFont(QFont("Arial", 32))
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)

        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 11))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)

        layout.addWidget(avatar)
        layout.addSpacing(10)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        frame.setLayout(layout)
        return frame
    
    def wipe_user_data(self):
        #print("Wiping user data...", self.user_answers)
        self.user_answers = {}
        #print("User data wiped.",)

