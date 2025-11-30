from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from dashboard import HeaderWidget

class ResultPage(QWidget):
    # Signals for navigation
    show_answers_clicked = pyqtSignal()
    learn_more_clicked = pyqtSignal()
    back_to_dashboard_clicked = pyqtSignal()
    view_pet_clicked = pyqtSignal()
    header_dashboard_clicked = pyqtSignal()
    download_pdf_clicked = pyqtSignal()


    def __init__(self, score, max_score, parent=None):
        super().__init__(parent)
        self.score = score
        self.max_score = max_score
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        # --- Header ---
        self.header = HeaderWidget()
        layout.addWidget(self.header)

        # --- Title above the circle ---
        title = QLabel("🎉 Quiz Completed!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #0277BD;")
        layout.addWidget(title)

        # --- Circle with tick ---
        circle_label = QLabel("✅")  # Tick emoji
        circle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        circle_label.setFixedSize(150, 150)
        circle_label.setStyleSheet("""
            QLabel {
                font-size: 72px;
                background-color: #E3F2FD;  /* light blue */
                border: 4px solid #0288D1;
                border-radius: 75px;
            }
        """)
        layout.addWidget(circle_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- Score below circle ---
        score_label = QLabel(f"{self.score} / {self.max_score}")
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0288D1;")
        layout.addWidget(score_label)

        # --- Motivational text ---
        if self.score == self.max_score:
            msg = "💯 Perfect Score! Excellent work!"
        elif self.score >= self.max_score / 2:
            msg = "👍 Good Job! Keep learning!"
        else:
            msg = "💡 Don't worry! Keep improving!"

        msg_label = QLabel(msg)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setStyleSheet("font-size: 16px; color: #555555; font-style: italic;")
        layout.addWidget(msg_label)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.show_answers_btn = QPushButton("👍 Show Answers")
        self.show_answers_btn.setStyleSheet("""
            QPushButton {
                background-color: #81C784;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)
        self.show_answers_btn.clicked.connect(self.show_answers_clicked.emit)

        button_layout.addWidget(self.show_answers_btn)

        self.learn_more_btn = QPushButton("📚 Learn More")
        self.learn_more_btn.setStyleSheet("""
            QPushButton {
                background-color: #64B5F6;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #42A5F5;
            }
        """)
        self.learn_more_btn.clicked.connect(self.learn_more_clicked.emit)
        button_layout.addWidget(self.learn_more_btn)

        layout.addLayout(button_layout)

        # --- PET Recommendation button ---
        self.view_pet_btn = QPushButton("🔒 View Privacy Eenchnacing Tools")
        self.view_pet_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFB74D;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFA726;
            }
        """)
        self.view_pet_btn.clicked.connect(self.view_pet_clicked.emit)
        button_layout.addWidget(self.view_pet_btn)

        layout.addLayout(button_layout)

        # Download PDF
        download_pdf_btn = QPushButton("📄 Download PDF")
        download_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #6a0dad;  /* Purple */
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #5b0ca1;  /* Darker purple on hover */
            }
        """)
        download_pdf_btn.clicked.connect(lambda: self.download_pdf_clicked.emit())
        button_layout.addWidget(download_pdf_btn)

        # --- Back to dashboard ---
        self.finish_button = QPushButton("🏠 Back to Dashboard")
        self.finish_button.setStyleSheet("""
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #009E88;
            }
        """)
        self.finish_button.clicked.connect(self.back_to_dashboard_clicked.emit)
        layout.addWidget(self.finish_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        

        

