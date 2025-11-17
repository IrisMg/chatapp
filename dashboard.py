from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import pyqtSignal,Qt

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
        self.label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # show hand cursor
        self.label.mousePressEvent = self.on_click  # override click event
        layout.addWidget(self.label)
        layout.addStretch()
        self.setLayout(layout)

    def on_click(self, event):
        self.dashboard_clicked.emit()  # emit signal when clicked

class DashboardPage(QWidget):
    def __init__(self, user_name="User", parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # --- Header ---
        header = HeaderWidget()
        main_layout.addWidget(header)
        

        # --- Start Section ---
        start_frame = QFrame()
        start_frame.setStyleSheet("""
            QFrame {
                background-color: #BBDEFB;  /* light blue */
                border-radius: 10px;
            }
        """)
        start_layout = QVBoxLayout()
        start_layout.setSpacing(20)
        start_layout.setContentsMargins(50, 50, 50, 50)

        # Title
        start_title = QLabel("Start Your Privacy Assistant")
        start_title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        start_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Description
        start_desc = QLabel(
            "Get personalized PETs and product recommendations based on your knowledge level and specific concerns."
        )
        start_desc.setFont(QFont("Arial", 14))
        start_desc.setWordWrap(True)
        start_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Estimated time
        start_time = QLabel("Takes approximately 5-10 minutes.")
        start_time.setFont(QFont("Arial", 12))
        start_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(200)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;  /* medium blue */
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0D47A1;  /* darker blue */
            }
        """)
        # Center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()

        # Add widgets to start layout
        start_layout.addWidget(start_title)
        start_layout.addWidget(start_desc)
        start_layout.addWidget(start_time)
        start_layout.addLayout(button_layout)
        start_frame.setLayout(start_layout)
        main_layout.addWidget(start_frame)

        # --- Assessment Box ---
        assessment_box = QFrame()
        assessment_box.setFrameShape(QFrame.Shape.StyledPanel)
        assessment_box.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;  /* very light blue */
                border-radius: 10px;
                padding: 20px;
            }
        """)
        box_layout = QVBoxLayout()
        box_layout.setSpacing(20)

        # Box title with book emoji aligned left
        box_title = QLabel("📖 How the Assessment Works")
        box_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        box_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        box_title.setContentsMargins(10, 0, 0, 0)
        box_layout.addWidget(box_title)

        # Cards inside the box (3 cards)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Cards content: (title, description, emoji)
        cards_info = [
            ("Share Background", "Tell us about your privacy background.", "👤"),
            ("Answer Awareness Questions", "Discuss your specific privacy concerns.", "❓"),
            ("Learning or Recommendations", "Receive personalized privacy guidance.", "✔️"),
        ]

        for title, desc, emoji in cards_info:
            card = self.create_card(title, desc, emoji)
            cards_layout.addWidget(card)

        box_layout.addLayout(cards_layout)
        assessment_box.setLayout(box_layout)
        main_layout.addWidget(assessment_box)
        main_layout.addStretch()

        # --- What You'll Learn Box ---
        learn_box = QFrame()
        learn_box.setFrameShape(QFrame.Shape.StyledPanel)
        learn_box.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;  /* very light blue */
                border-radius: 10px;
                padding: 20px;
            }
        """)
        learn_layout = QVBoxLayout()
        learn_layout.setSpacing(15)

        # Box title with emoji
        learn_title = QLabel("🔒 What You'll Learn")
        learn_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        learn_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        learn_title.setContentsMargins(10, 0, 0, 0)
        learn_layout.addWidget(learn_title)

        # --- Inner box for bullet points ---
        inner_box = QFrame()
        inner_box.setFrameShape(QFrame.Shape.StyledPanel)
        inner_box.setStyleSheet("""
            QFrame {
                background-color: #64B5F6;  
                border-radius: 10px;
                padding: 15px;
            }
        """)
        inner_layout = QVBoxLayout()
        inner_layout.setSpacing(8)

        # Bullet points
        bullet_points = [
            "Browser Fingerprinting",
            "Location Tracking by Apps",
            "Unprotected File Sharing Links",
            "Using Public Wi-Fi Without Protection"
        ]

        for point in bullet_points:
            point_label = QLabel(f"• {point}")
            point_label.setFont(QFont("Arial", 12))
            point_label.setStyleSheet("color: white;")  
            point_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            inner_layout.addWidget(point_label)

        inner_box.setLayout(inner_layout)
        learn_layout.addWidget(inner_box)

        learn_box.setLayout(learn_layout)
        main_layout.addWidget(learn_box)




        # --- Make Scrollable ---
        container = QWidget()
        container.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scroll)

    def create_card(self, title, description, emoji):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #64B5F6;  /* medium blue */
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Emoji as avatar
        avatar_label = QLabel(emoji)
        avatar_label.setFont(QFont("Arial", 32))  # big emoji
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 11))
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(avatar_label)
        layout.addSpacing(10)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        frame.setLayout(layout)
        return frame
