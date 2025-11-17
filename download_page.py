import os
import tempfile
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage


class DownloadPDFPage(QWidget):
    back_to_dashboard_clicked = pyqtSignal()

    def __init__(self, user_background_answers, quiz_questions, user_quiz_answers,
                 pet_recommendations, learn_more_content, concern_title, parent=None):

        super().__init__(parent)

        # --- SAVE INPUTS --- #
        self.user_background_answers = user_background_answers
        self.quiz_questions = quiz_questions
        self.user_quiz_answers = user_quiz_answers
        self.pet_recommendations = pet_recommendations
        self.concern_title = concern_title
        self.learn_more_content = self._normalize_learn_more(learn_more_content)

        self.init_ui()

    def _normalize_learn_more(self, data):
        if not data:
            return None
        if isinstance(data, dict):
            return data
        
        if isinstance(data, list) and len(data) == 1:
            row = data[0]
            if isinstance(row, tuple):
                
                return {
                    "specific_concern": row[1],
                    "what_is_it": row[2],
                    "why_it_matters": row[3],
                    "dos": row[4],
                    "donts": row[5],
                }

            if isinstance(row, dict):
                return row
        if isinstance(data, tuple):
            return {
                "specific_concern": data[1],
                "what_is_it": data[2],
                "why_it_matters": data[3],
                "dos": data[4],
                "donts": data[5],
            }

        return None


    # UI
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel(f"📥 Download PDF - {self.concern_title}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #0277BD;")
        layout.addWidget(title)

        instruction = QLabel("Enter your email to receive the PDF report.")
        instruction.setWordWrap(True)
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(instruction)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        self.email_input.setFixedWidth(300)
        self.email_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.email_input, alignment=Qt.AlignmentFlag.AlignCenter)

        send_btn = QPushButton("📄 Send PDF")
        send_btn.clicked.connect(self.send_pdf)
        layout.addWidget(send_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton("🏠 Back to Dashboard")
        back_btn.clicked.connect(self.back_to_dashboard_clicked.emit)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    # PDF GENERATION
    def generate_pdf(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(tmp_file.name, pagesize=letter)
        width, height = letter
        margin = 50
        y = height - 50

        c.setFont("Helvetica-Bold", 20)
        c.drawString(margin, y, f"Report: {self.concern_title}")
        y -= 40

        # --- USER BACKGROUND --- 
        if self.user_background_answers:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(margin, y, "📝 User Background Answers:")
            y -= 25
            c.setFont("Helvetica", 12)

            for q, a in self.user_background_answers.items():
                y = self._draw_wrapped(c, f"{q}: {a}", margin, y)

        # --- QUIZ ANSWERS --- 
        if self.quiz_questions:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(margin, y, "❓ Awareness Quiz Answers:")
            y -= 25
            c.setFont("Helvetica", 12)

            for q in self.quiz_questions:
                text = q["text"]
                ans = self.user_quiz_answers.get(text, "No answer")
                y = self._draw_wrapped(c, f"Q: {text}", margin, y)
                y = self._draw_wrapped(c, f"Your answer: {ans}", margin + 15, y)
                y -= 5

        # --- PET RECOMMENDATIONS --- 
        if self.pet_recommendations:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(margin, y, "🐾 PET Recommendations:")
            y -= 25
            c.setFont("Helvetica", 12)

            for pet in self.pet_recommendations:
                y = self._draw_wrapped(c, f"Name: {pet.get('pet_name', '')}", margin, y)
                y = self._draw_wrapped(c, f"Price: {pet.get('pet_price', '')}", margin + 15, y)
                y = self._draw_wrapped(c, f"Description: {pet.get('pet_description', '')}", margin + 15, y)
                y = self._draw_wrapped(c, f"Company: {pet.get('pet_company', '')}", margin + 15, y)
                y -= 10

        # --- LEARN MORE --- 
        learn_more_content = {}
        if hasattr(self, "conn") and self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT specific_concern, what_is_it, why_it_matters, dos, donts
                FROM learn_more
                WHERE TRIM(specific_concern) = TRIM(?)
            """, (self.concern_title,))
            row = cursor.fetchone()
            if row:
                learn_more_content = {
                    "specific_concern": row[0],
                    "what_is_it": row[1],
                    "why_it_matters": row[2],
                    "dos": row[3],
                    "donts": row[4]
                }

        c.save()
        return tmp_file.name

    # WRAPPED TEXT
    def _draw_wrapped(self, c, text, x, y, width=500, size=12):
        lines = []
        words = text.split()

        line = ""
        for w in words:
            test = line + " " + w if line else w
            if c.stringWidth(test, "Helvetica", size) < width:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)

        for l in lines:
            c.drawString(x, y, l)
            y -= 14
            if y < 80:
                c.showPage()
                y = 750
                c.setFont("Helvetica", size)

        return y

    # EMAIL SENDING
    def send_pdf_email(self, to_email, pdf_path):
        msg = EmailMessage()
        msg["Subject"] = f"PDF Report: {self.concern_title}"
        msg["From"] = "privacyassistantapp@gmail.com"
        msg["To"] = to_email
        msg.set_content(f"Here is your PDF report for {self.concern_title}.")

        with open(pdf_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf",
                               filename=f"{self.concern_title}.pdf")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("privacyassistantapp@gmail.com", "vgilgbjchpujmcir")  
            smtp.send_message(msg)

    # SEND BUTTON
    def send_pdf(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Missing Email", "Please enter your email address.")
            return

        pdf_path = self.generate_pdf()

        try:
            self.send_pdf_email(email, pdf_path)
            QMessageBox.information(self, "Success",
                                    f"📤 PDF for '{self.concern_title}' sent to {email}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send PDF: {e}")
        finally:
            os.remove(pdf_path)
            self.email_input.clear()
