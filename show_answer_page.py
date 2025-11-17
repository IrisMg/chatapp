from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QRadioButton, QCheckBox, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from dashboard import HeaderWidget

class ShowAnswersPage(QWidget):
    go_back = pyqtSignal()  # Signal to go back to results page

    def __init__(self, questions, user_answers, parent=None):
        """
        questions: list of dicts from fetch_questions()
        user_answers: dict mapping question_id -> list of selected option_ids
        """
        super().__init__(parent)
        self.questions = questions
        self.user_answers = user_answers
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # Header
        self.header = HeaderWidget()
        main_layout.addWidget(self.header)

        # Title
        title = QLabel("📖 Review Your Answers")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #0277BD; margin: 10px;")
        main_layout.addWidget(title)

        # Scroll area for questions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(20, 20, 20, 20)

        for q in self.questions:
            q_selected_ids = self.user_answers.get(q['id'], [])

            # --- Question card ---
            top_card = QFrame()
            top_card.setStyleSheet("""
                QFrame {
                    background-color: #E3F2FD;
                    border-radius: 12px;
                    padding: 15px;
                    border: 1px solid #90CAF9;
                }
            """)
            top_layout = QVBoxLayout()
            top_layout.setSpacing(8)

            q_label = QLabel(f"{q.get('category','')} - {q['text']}")
            q_label.setWordWrap(True)
            q_label.setStyleSheet("font-weight: bold; font-size: 16px;")
            top_layout.addWidget(q_label)

            for opt_id, opt_text, is_correct in q['options']:
                if q['type'] == "single":
                    opt_widget = QRadioButton(opt_text)
                    opt_widget.setAutoExclusive(False)  
                else:
                    opt_widget = QCheckBox(opt_text)

                if opt_id in q_selected_ids:
                    opt_widget.setChecked(True)
                opt_widget.setEnabled(False)
                top_layout.addWidget(opt_widget)

            top_card.setLayout(top_layout)
            container_layout.addWidget(top_card)

            # --- Feedback card ---
            feedback_card = QFrame()
            feedback_card.setStyleSheet("""
                QFrame {
                    background-color: #F1F8E9;
                    border-radius: 10px;
                    padding: 10px;
                    border: 1px solid #C5E1A5;
                }
            """)
            feedback_layout = QVBoxLayout()
            feedback_layout.setSpacing(6)

            # User choices feedback
            for opt_id, opt_text, is_correct in q['options']:
                if opt_id in q_selected_ids:
                    if is_correct:
                        text = f"✅ You chose: {opt_text} — Correct!"
                        color = "#2E7D32"
                    else:
                        text = f"❌ You chose: {opt_text} — Incorrect"
                        color = "#C62828"
                    lbl = QLabel(text)
                    lbl.setWordWrap(True)
                    lbl.setStyleSheet(f"color: {color}; font-size: 14px; padding-left: 12px;")
                    feedback_layout.addWidget(lbl)

            # Show correct answers missed
            for opt_id, opt_text, is_correct in q['options']:
                if is_correct and opt_id not in q_selected_ids:
                    text = f"✅ Correct answer: {opt_text}"
                    color = "#2E7D32"
                    lbl = QLabel(text)
                    lbl.setWordWrap(True)
                    lbl.setStyleSheet(f"color: {color}; font-size: 14px; padding-left: 12px;")
                    feedback_layout.addWidget(lbl)

            feedback_card.setLayout(feedback_layout)
            container_layout.addWidget(feedback_card)

        container.setLayout(container_layout)
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        # --- Back button ---
        back_btn = QPushButton("← Back to Results")
        back_btn.setFixedWidth(180)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #B0BEC5;
                color: black;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #90A4AE;
            }
        """)
        back_btn.clicked.connect(self.go_back.emit)
        main_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
