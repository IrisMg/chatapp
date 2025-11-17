import os
import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton,
    QScrollArea, QFrame, QHBoxLayout, QButtonGroup
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from dashboard import HeaderWidget
from data.fetch_data import fetch_questions


class BackgroundQuestionsPage(QWidget):
    go_to_awareness_quiz = pyqtSignal(list)

    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.questions = fetch_questions(db_path, quiz_type="background")
        self.option_widgets = []
        self.dynamic_option_widgets = []
        self.dynamic_shown = False
        self.init_ui()

        self._answer_mapping = {
            "device": self._get_selected_answer_for_keyword,
            "operating system": self._get_selected_answer_for_keyword,
            "country": self._get_selected_answer_for_keyword,
            "free or paid": self._get_selected_answer_for_keyword,
        }

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        self.header = HeaderWidget()
        main_layout.addWidget(self.header)

        title = QLabel("User Background Questions")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        # Icon map
        self.icon_map = {
            "Desktop": "assets/userbackground_icons/desktop.png",
            "Mobile": "assets/userbackground_icons/mobile.png",
            "Public Computer": "assets/userbackground_icons/public_computer.png",
            "Windows": "assets/userbackground_icons/window.png",
            "macOS": "assets/userbackground_icons/macos.png",
            "Linux": "assets/userbackground_icons/linux.png",
            "Android": "assets/userbackground_icons/android.png",
            "iOS": "assets/userbackground_icons/ios.png",
            "Website browsing": "assets/userbackground_icons/browser.png",
            "Mobile apps": "assets/userbackground_icons/apps.png",
            "Network": "assets/userbackground_icons/network.png",
            "Cloud": "assets/userbackground_icons/cloud.png",
        }

        self.privacy_concerns_map = {
            "Website browsing": [
                "Browser Fingerprinting",
                "Targeted Ads and Online tracking",
                "Public Wi-Fi browsing risks",
                "Auto-Saved Passwords and Autofill Data"
            ],
            "Mobile apps": [
                "Location Tracking by Apps",
                "Data Sharing with Third Parties",
                "Hidden Background Activity",
                "Malicious or Scam Apps"
            ],
            "Cloud": [
                "Unprotected File Sharing Links",
                "Weak or Shared Passwords",
                "Automatic Photo Backup Without Consent",
                "Data Stored in Unknown Locations"
            ],
            "Network": [
                "Using Public Wi-Fi Without Protection",
                "ISP Tracking and Data Logging",
                "Unencrypted Network Traffic",
                "Unsecured Bluetooth or Hotspot Sharing"
            ]
        }

        for question in self.questions:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #B3E5FC;
                    border-radius: 10px;
                    padding: 15px;
                }
            """)
            layout = QVBoxLayout()

            q_label = QLabel(question["text"])
            q_label.setWordWrap(True)
            q_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            layout.addWidget(q_label)

            row_layout = QHBoxLayout()
            row_layout.setSpacing(15)

            btn_group = QButtonGroup(card)
            btn_group.setExclusive(True)

            question_widgets = []

            for opt_id, opt_text, _ in question['options']:
                opt = QRadioButton(opt_text)
                btn_group.addButton(opt)

                opt_card = QFrame()
                opt_card.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        border-radius: 8px;
                        border: 1px solid #BBDEFB;
                        padding: 10px;
                    }
                    QFrame:hover {
                        background-color: #E1F5FE;
                    }
                """)
                opt_lay = QVBoxLayout()
                opt_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

                icon_path = self.icon_map.get(opt_text)
                if icon_path and os.path.exists(icon_path):
                    icon = QLabel()
                    pixmap = QPixmap(icon_path).scaled(
                        64, 64,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    icon.setPixmap(pixmap)
                    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    opt_lay.addWidget(icon)

                opt_lay.addWidget(opt, alignment=Qt.AlignmentFlag.AlignCenter)
                opt_card.setLayout(opt_lay)

                row_layout.addWidget(opt_card)
                question_widgets.append((opt_id, opt))

            layout.addLayout(row_layout)
            card.setLayout(layout)
            main_layout.addWidget(card)

            self.option_widgets.append((question["id"], question_widgets))

        self.dynamic_container = QFrame()
        self.dynamic_container.setStyleSheet("""
            QFrame {
                background-color: #B3E5FC;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.dynamic_layout = QVBoxLayout()
        self.dynamic_container.setLayout(self.dynamic_layout)
        self.dynamic_container.hide()
        main_layout.addWidget(self.dynamic_container)

        # Warning label
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red; font-size: 12px;")
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_label.hide()
        main_layout.addWidget(self.warning_label)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(200)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #0277BD;
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #01579B;
            }
        """)
        self.submit_button.clicked.connect(self.handle_submit)
        main_layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        final = QVBoxLayout(self)
        final.addWidget(scroll)

    
    # Show dynamic concerns (single-select only)
    def show_dynamic_concerns(self, selected_areas):
        # Clear old content
        for i in reversed(range(self.dynamic_layout.count())):
            w = self.dynamic_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        self.dynamic_option_widgets.clear()

        title = QLabel("Select your primary concern:")
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        self.dynamic_layout.addWidget(title)

        row = QHBoxLayout()

        self.dynamic_btn_group = QButtonGroup(self.dynamic_container)
        self.dynamic_btn_group.setExclusive(True)

        for area in selected_areas:
            concerns = self.privacy_concerns_map.get(area, [])
            for concern in concerns:
                card = QFrame()
                card.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        border-radius: 10px;
                        padding: 8px;
                        border: 1px solid #81D4FA;
                    }
                """)
                card_lay = QVBoxLayout()

                rb = QRadioButton(concern)
                self.dynamic_btn_group.addButton(rb)

                card_lay.addWidget(rb)
                card.setLayout(card_lay)
                row.addWidget(card)

                self.dynamic_option_widgets.append((area, rb))

        self.dynamic_layout.addLayout(row)
        self.dynamic_container.show()

    
    # Handle submit click
    def handle_submit(self):
        background_answers = []
        selected_areas = []

        
        for question_id, widgets in self.option_widgets:
            selected = [opt_id for opt_id, w in widgets if w.isChecked()]

            if not selected:
                self.warning_label.setText("⚠ Please answer all questions.")
                self.warning_label.show()
                return

            background_answers.append((question_id, selected[0]))

            
            for opt_id, w in widgets:
                if w.isChecked() and w.text() in self.privacy_concerns_map:
                    selected_areas.append(w.text())

        
        if not self.dynamic_shown and selected_areas:
            self.dynamic_shown = True
            self.show_dynamic_concerns(selected_areas)
            self.warning_label.setText("⚠ Please select your primary concern and submit again.")
            self.warning_label.show()
            return

        
        dynamic_answers = []
        for area, rb in self.dynamic_option_widgets:
            if rb.isChecked():
                dynamic_answers.append((area, rb.text()))

        if not dynamic_answers:
            self.warning_label.setText("⚠ Please select your primary concern.")
            self.warning_label.show()
            return

        self.warning_label.hide()

        self.insert_answers_into_db(background_answers, dynamic_answers)

        selected_concerns = [rb.text() for _, rb in self.dynamic_option_widgets if rb.isChecked()]
        self.go_to_awareness_quiz.emit(selected_concerns)

    
    # Save answers to DB
    def insert_answers_into_db(self, background, dynamic):
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER,
                    option_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cur.executemany(
                "INSERT INTO user_answers (question_id, option_id) VALUES (?, ?)",
                background
            )

            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_dynamic_concerns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    area TEXT,
                    concern TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cur.executemany(
                "INSERT INTO user_dynamic_concerns (area, concern) VALUES (?, ?)",
                dynamic
            )

            con.commit()
            con.close()

        except sqlite3.Error as e:
            print("❌ DB Error:", e)

    
    # Keyword-based getters
    def _get_selected_answer_for_keyword(self, keyword):
        for q_id, widgets in self.option_widgets:
            q_text = self.questions[q_id - 1]['text'].lower()
            if keyword in q_text:
                for _, w in widgets:
                    if w.isChecked():
                        return w.text()
        return None

    def get_user_device(self):
        return self._answer_mapping["device"]("device")

    def get_user_os(self):
        return self._answer_mapping["operating system"]("operating system")

    def get_user_country(self):
        return self._answer_mapping["country"]("country")

    def get_user_preference(self):
        return self._answer_mapping["free or paid"]("free or paid")
    
    def get_user_answers_dict(self):
        #Return a dictionary of all user answers collected on this page.
        answers = {}

        for question_id, options in self.option_widgets:
            # Get question text
            question_text = self.questions[question_id - 1]["text"]
            # Find which option is checked
            selected_answer = None
            for opt_id, widget in options:
                if widget.isChecked():
                    selected_answer = widget.text()
                    break
            answers[question_text] = selected_answer

        # Include dynamic concerns if shown
        if self.dynamic_shown and self.dynamic_option_widgets:
            for area, rb in self.dynamic_option_widgets:
                if rb.isChecked():
                    answers[f"Primary concern in {area}"] = rb.text()

        return answers
