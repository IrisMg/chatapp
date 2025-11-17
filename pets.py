from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import os
from download_page import DownloadPDFPage

class PetRecommendationPage(QWidget):
    back_to_dashboard_clicked = pyqtSignal()
    view_pet_clicked = pyqtSignal(str)
    download_pdf_clicked = pyqtSignal()

    def __init__(self, selected_concern, awareness_level, device, os, country, db_connection,
             user_background_answers, quiz_questions, user_quiz_answers, learn_more_content, parent=None):
        super().__init__(parent)
        self.selected_concern = selected_concern
        self.awareness_level = awareness_level
        self.device = device
        self.os = os
        self.country = country
        self.conn = db_connection
    
        # --- NEW ---
        self.user_background_answers = user_background_answers
        self.quiz_questions = quiz_questions
        self.user_quiz_answers = user_quiz_answers
        self.learn_more_content = learn_more_content

        # Fetch PETs
        self.recommended_pets, self.other_pets = self.fetch_pets()

        # If no recommended, show first 2–3 other pets as recommended
        if not self.recommended_pets:
            self.recommended_pets = self.other_pets[:3]
            # Remove other pets entirely
            self.other_pets = []
        
        self.init_ui()

    def fetch_pets(self):
        recommended = []
        others = []

        cursor = self.conn.cursor()
        # Exact match
        cursor.execute("""
            SELECT pet_name, pet_price, pet_description, pet_company, pet_link, logo_link, why_use, popularity
            FROM user_pets_recommendations
            WHERE TRIM(selected_concern) = TRIM(?)
            AND TRIM(awareness_level) = TRIM(?)
            AND TRIM(device) = TRIM(?)
            AND TRIM(os) = TRIM(?)
            AND TRIM(country) = TRIM(?)
        """, (self.selected_concern, self.awareness_level, self.device, self.os, self.country))
        rows = cursor.fetchall()
        for row in rows:
            recommended.append({
                "name": row[0],
                "price": row[1],
                "description": row[2],
                "company_name": row[3],
                "link": row[4],
                "logo": row[5],
                "why_use": row[6],
                "popularity": int(row[7]) if row[7] else 0
            })

        # Other PETs
        cursor.execute("""
            SELECT pet_name, pet_price, pet_description, pet_company, pet_link, logo_link, why_use, popularity
            FROM user_pets_recommendations
            WHERE TRIM(selected_concern) != TRIM(?)
            LIMIT 5
        """, (self.selected_concern,))
        rows = cursor.fetchall()
        for row in rows:
            others.append({
                "name": row[0],
                "price": row[1],
                "description": row[2],
                "company_name": row[3],
                "link": row[4],
                "logo": row[5],
                "why_use": row[6],
                "popularity": int(row[7]) if row[7] else 0
            })

        return recommended, others

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        container.setLayout(self.layout)
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Title
        title = QLabel("🔒 Your PET Recommendations")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #0277BD;")
        self.layout.addWidget(title)

        # Recommended PETs
        rec_label = QLabel("🌟 Recommended PETs")
        rec_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #0288D1;")
        self.layout.addWidget(rec_label)

        for pet in self.recommended_pets:
            self.layout.addWidget(self.create_horizontal_pet_card(pet, highlight=True))

        # Other PETs
        if self.other_pets:
            other_label = QLabel("💡 Other Privacy PETs")
            other_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #555555;")
            self.layout.addWidget(other_label)

            self.other_pets_container = QVBoxLayout()
            self.layout.addLayout(self.other_pets_container)

            for pet in self.other_pets:
                self.other_pets_container.addWidget(self.create_collapsible_other_pet(pet))

        # Footer buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        # Download PDF button
        download_pdf_btn = QPushButton("📄 Download PDF")
        download_pdf_btn.setStyleSheet("""
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
        download_pdf_btn.clicked.connect(lambda: self.download_pdf_clicked.emit())


        btn_layout.addWidget(download_pdf_btn)

        # Back button
        back_btn = QPushButton("🏠 Back to Dashboard")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #B0BEC5;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #90A4AE;
            }
        """)
        back_btn.clicked.connect(self.back_to_dashboard_clicked.emit)
        btn_layout.addWidget(back_btn)

        self.layout.addLayout(btn_layout)



    def create_horizontal_pet_card(self, pet, highlight=False):
        #Recommended PET card or expanded other PET card: logo left, details right.
        frame = QFrame()
        bg_color = "#E3F2FD" if highlight else "#F5F5F5"
        frame.setStyleSheet(f"QFrame {{ background-color: {bg_color}; border-radius: 10px; padding: 10px; }}")
        h_layout = QHBoxLayout()
        frame.setLayout(h_layout)

        # Details
        v_layout = QVBoxLayout()
        name_label = QLabel(f"🛡️ {pet['name']}")
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        v_layout.addWidget(name_label)

        # Popularity stars
        popularity = pet.get("popularity", 0)
        stars = "★" * popularity + "☆" * (5 - popularity)
        v_layout.addWidget(QLabel(f"Popularity: {stars}"))

        v_layout.addWidget(QLabel(f"💰 Price: {pet['price']}"))
        desc_label = QLabel(f"📖 {pet['description']}")
        desc_label.setWordWrap(True)
        v_layout.addWidget(desc_label)
        why_label = QLabel(f"✅ Why use: {pet['why_use']}")
        why_label.setWordWrap(True)
        v_layout.addWidget(why_label)
        v_layout.addWidget(QLabel(f"🏢 {pet['company_name']}"))
        link_label = QLabel(f"🔗 <a href='{pet['link']}'>{pet['link']}</a>")
        link_label.setOpenExternalLinks(True)
        v_layout.addWidget(link_label)

        h_layout.addLayout(v_layout)
        return frame

    def create_collapsible_other_pet(self, pet):
        #Other PET row: name,price shown, expand to horizontal card with logo,details.
        container = QWidget()
        v_layout = QVBoxLayout()
        container.setLayout(v_layout)

        # Button row
        btn_row = QPushButton(f"🛡️ {pet['name']}  💰 {pet['price']}")
        btn_row.setStyleSheet("text-align: left; padding: 5px; background-color: #F5F5F5;")
        v_layout.addWidget(btn_row)

        # Placeholder for expanded card
        expanded_layout = QVBoxLayout()
        v_layout.addLayout(expanded_layout)

        # Toggle on click
        btn_row.clicked.connect(lambda _, p=pet, ph=expanded_layout: self.toggle_expand_card(p, ph))
        return container

    def toggle_expand_card(self, pet, layout):
        #Toggle expand/collapse horizontal PET card
        if layout.count() > 0:
            # Collapse
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        else:
            # Expand
            layout.addWidget(self.create_horizontal_pet_card(pet, highlight=False))
        
    
    

