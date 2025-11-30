from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton, QCheckBox,
    QPushButton, QScrollArea, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from data.fetch_data import fetch_questions
from dashboard import HeaderWidget
import sqlite3

class ConcernAwarenessQuizPage(QWidget):
    show_result = pyqtSignal(int, int)  
    go_back = pyqtSignal()             

    def __init__(self, db_path, selected_concerns=None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.selected_concerns = selected_concerns or []

        # Fetch only concern questions
        self.questions = fetch_questions(
            db_path,
            quiz_type="concern",
            selected_concerns=self.selected_concerns
        )

        self.option_widgets = []  
        self.init_ui()

    def init_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Header ---
        self.header = HeaderWidget()
        main_layout.addWidget(self.header)

        # --- Page Title ---
        title = QLabel("Concern Awareness Quiz")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        # --- Quiz content ---
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)

        for question in self.questions:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #E3F2FD;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
            f_layout = QVBoxLayout()
            f_layout.setSpacing(10)

            q_label = QLabel(f" {question['text']}")
            q_label.setWordWrap(True)
            q_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            f_layout.addWidget(q_label)

            option_widgets = []
            for opt_id, opt_text, is_correct in question['options']:
                is_correct = bool(is_correct)
                opt_widget = QRadioButton(opt_text)  # single-answer only
                f_layout.addWidget(opt_widget)
                option_widgets.append((opt_widget, opt_id, is_correct))

            self.option_widgets.append((question['id'], option_widgets))
            card.setLayout(f_layout)
            content_layout.addWidget(card)

        main_layout.addLayout(content_layout)

        # --- Buttons layout (Back + Submit) ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(120)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #B0BEC5;
                color: black;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #90A4AE;
            }
        """)
        back_btn.clicked.connect(self.go_back.emit)
        button_layout.addWidget(back_btn)

        # Submit button
        submit_btn = QPushButton("Submit Quiz")
        submit_btn.setFixedWidth(200)
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #0277BD;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #01579B;
            }
        """)
        submit_btn.clicked.connect(self.handle_submit)
        button_layout.addWidget(submit_btn)

        # Add buttons layout to main layout
        main_layout.addLayout(button_layout)

        # --- Make scrollable ---
        container = QWidget()
        container.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        final_layout = QVBoxLayout(self)
        final_layout.addWidget(scroll)


    def handle_submit(self):
        total = 0
        max_score = len(self.option_widgets)
        answers_to_save = []

        for q_id, options in self.option_widgets:
            # Collect all selected answers for this question
            selected_opt_id = None
            for widget, opt_id, is_correct in options:
                if widget.isChecked():
                    selected_opt_id = opt_id
                    if is_correct:
                        total += 1
                    break  

            # Save answer if there is one
            if selected_opt_id is not None:
                answers_to_save.append((q_id, selected_opt_id))

        # Save to DB (only answered questions)
        try:
            if answers_to_save:
                self.save_answers_to_db(answers_to_save)
        except Exception as e:
            print("Error saving answers:", e)

        # Emit results no matter what
        try:
            self.show_result.emit(total, max_score)
        except Exception as e:
            print("Error emitting show_result signal:", e)


    # for next show answers page
    def get_user_answers_dict(self):
        answers = {}
        for q_id, options in self.option_widgets:
            selected = [opt_id for widget, opt_id, _ in options if widget.isChecked()]
            answers[q_id] = selected
        return answers


    def save_answers_to_db(self, answers):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_concern_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    option_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.executemany(
                "INSERT INTO user_concern_answers (question_id, option_id) VALUES (?, ?)",
                answers
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Database error:", e)
    
    def wipe_user_data(self):
       # print("Wiping user data from ConcernAwarenessQuizPage", self.user_answers)
        self.user_answers = {}
        self.questions = []
        self.selected_concerns = []

