import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from qt_material import apply_stylesheet
from dashboard import DashboardPage
from userbackground_questions import BackgroundQuestionsPage
from concern_awareness_quiz import ConcernAwarenessQuizPage
from results_page import ResultPage
from show_answer_page import ShowAnswersPage
from learn_more_page import LearnMorePage
from download_page import DownloadPDFPage
from data.fetch_data import fetch_questions
import sqlite3
from pets import PetRecommendationPage
from PyQt6.QtGui import QFont

DB_PATH = "db/questions.db"
questions = fetch_questions(DB_PATH, quiz_type="concern")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect(DB_PATH)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize pages
        self.dashboard = DashboardPage("Alice")
        self.background_page = BackgroundQuestionsPage(DB_PATH)
        self.background_page.go_to_awareness_quiz.connect(self.show_concern_quiz)

        # Add pages to stack
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.background_page)

        # Connect dashboard button
        self.dashboard.start_button.clicked.connect(self.show_background_page)
        self.background_page.header.dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )

    def show_background_page(self):
        self.stack.setCurrentWidget(self.background_page)

    def show_concern_quiz(self, selected_concerns):
        self.concern_quiz_page = ConcernAwarenessQuizPage(DB_PATH, selected_concerns)
        self.concern_quiz_page.show_result.connect(self.show_results)
        self.concern_quiz_page.header.dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )
        self.concern_quiz_page.go_back.connect(
            lambda: self.stack.setCurrentWidget(self.background_page)
        )

        self.stack.addWidget(self.concern_quiz_page)
        self.stack.setCurrentWidget(self.concern_quiz_page)

    def show_results(self, score, total):
        selected_concern = self.concern_quiz_page.selected_concerns[0]

        self.results_page = ResultPage(score, total)

        # Connect buttons
        self.results_page.header.dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )
        self.results_page.learn_more_clicked.connect(
            lambda concern_title=selected_concern: self.show_learn_more_page(concern_title)
        )
        self.results_page.show_answers_clicked.connect(self.show_answers_page)
        self.results_page.view_pet_clicked.connect(self.show_pet_page)
        self.results_page.back_to_dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )
        self.results_page.download_pdf_clicked.connect(
            lambda: self.show_download_pdf_page(
                concern_title=self.concern_quiz_page.selected_concerns[0]
            )
        )

        self.stack.addWidget(self.results_page)
        self.stack.setCurrentWidget(self.results_page)

    def show_learn_more_page(self, selected_concern):
        self.learn_more_page_widget = LearnMorePage(
            selected_concern=selected_concern, db_connection=self.conn
        )
        self.learn_more_page_widget.header.dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )
        self.learn_more_page_widget.download_pdf_clicked.connect(
            lambda title: self.show_download_pdf_page(title)
        )
        self.learn_more_page_widget.back_to_dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )
        self.learn_more_page_widget.go_back.connect(
        lambda: self.stack.setCurrentWidget(self.results_page)   
    )
        self.stack.addWidget(self.learn_more_page_widget)
        self.stack.setCurrentWidget(self.learn_more_page_widget)

    def show_download_pdf_page(self, concern_title):
        user_background = self.background_page.get_user_answers_dict() if hasattr(self.background_page, "get_user_answers_dict") else {}
        quiz_answers = self.concern_quiz_page.get_user_answers_dict() if hasattr(self, "concern_quiz_page") else {}
        pet_recommendations = getattr(self, "pet_page", None)
        if pet_recommendations:
            pet_recommendations = pet_recommendations.recommended_pets
        else:
            pet_recommendations = []

        learn_more_content = {}
        if hasattr(self, "learn_more_page_widget") and self.learn_more_page_widget:
            if hasattr(self.learn_more_page_widget, "get_content"):
                learn_more_content = self.learn_more_page_widget.get_content()
        self.download_pdf_page_widget = DownloadPDFPage(
            user_background_answers=user_background,
            quiz_questions=self.concern_quiz_page.questions,
            user_quiz_answers=quiz_answers,
            pet_recommendations=pet_recommendations,
            learn_more_content=learn_more_content,
            concern_title=concern_title
        )
        self.download_pdf_page_widget.header.dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )

        self.download_pdf_page_widget.back_to_dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )
        self.stack.addWidget(self.download_pdf_page_widget)
        self.stack.setCurrentWidget(self.download_pdf_page_widget)


    def show_answers_page(self):
        user_answers = self.concern_quiz_page.get_user_answers_dict()
        questions = self.concern_quiz_page.questions
        self.show_answers_page_widget = ShowAnswersPage(questions, user_answers)
        self.show_answers_page_widget.go_back.connect(
            lambda: self.stack.setCurrentWidget(self.results_page)
        )
        self.show_answers_page_widget.header.dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )

        self.stack.addWidget(self.show_answers_page_widget)
        self.stack.setCurrentWidget(self.show_answers_page_widget)

    def show_pet_page(self):
        # Fetch user background info
        device = self.background_page.get_user_device()
        os = self.background_page.get_user_os()
        country = self.background_page.get_user_country()
        price_pref = self.background_page.get_user_preference()

        # Awareness level from quiz result
        score = self.results_page.score
        max_score = self.results_page.max_score
        if score <= max_score * 0.4:
            awareness_level = "Low"
        elif score <= max_score * 0.7:
            awareness_level = "Moderate"
        else:
            awareness_level = "High"

        learn_more_content = {}
        if hasattr(self, 'learn_more_page_widget') and self.learn_more_page_widget:
            if hasattr(self.learn_more_page_widget, 'get_content'):
                learn_more_content = self.learn_more_page_widget.get_content()

        # Initialize PET page
        self.pet_page = PetRecommendationPage(
            selected_concern=self.concern_quiz_page.selected_concerns[0],
            awareness_level=awareness_level,
            device=device,
            os=os,
            country=country,
            db_connection=self.conn,
            user_background_answers=self.background_page.get_user_answers_dict(),
            quiz_questions=self.concern_quiz_page.questions,
            user_quiz_answers=self.concern_quiz_page.get_user_answers_dict(),
            learn_more_content=learn_more_content
        )
        self.pet_page.header.dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )
        self.pet_page.go_back.connect(
            lambda: self.stack.setCurrentWidget(self.results_page)
        )
        self.pet_page.back_to_dashboard_clicked.connect(
            lambda: self.stack.setCurrentWidget(self.dashboard)
        )

        self.pet_page.download_pdf_clicked.connect(
            lambda: self.show_download_pdf_page(
                concern_title=self.concern_quiz_page.selected_concerns[0]
            )
        )

        self.stack.addWidget(self.pet_page)
        self.stack.setCurrentWidget(self.pet_page)
    
    def closeEvent(self, event):

        # 1) delete background question data
        try:
            if hasattr(self.background_page, "wipe_user_data"):
                self.background_page.wipe_user_data()
        except:
            pass

        # 2) delete quiz answers
        try:
            if hasattr(self.concern_quiz_page, "wipe_user_data"):
                self.concern_quiz_page.wipe_user_data()
        except:
            pass

        # 3) delete learn-more content data
        try:
            if hasattr(self.learn_more_page_widget, "wipe_user_data"):
                self.learn_more_page_widget.wipe_user_data()
        except:
            pass

        # 4) delete PET data
        try:
            if hasattr(self.pet_page, "wipe_user_data"):
                self.pet_page.wipe_user_data()
        except:
            pass

        # 5) delete PDF generation data
        try:
            if hasattr(self.download_pdf_page_widget, "wipe_user_data"):
                self.download_pdf_page_widget.wipe_user_data()
        except:
            pass

        # Close DB securely
        try:
            if hasattr(self, "conn"):
                self.conn.close()
        except:
            pass

        event.accept()






if __name__ == "__main__":
    app = QApplication(sys.argv)

    apply_stylesheet(app, theme="light_blue.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


