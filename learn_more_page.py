import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal

class LearnMorePage(QWidget):
    download_pdf_clicked = pyqtSignal(str)
    pet_clicked = pyqtSignal(str)
    back_to_dashboard_clicked = pyqtSignal()
    go_back = pyqtSignal() 

    def __init__(self, selected_concern, db_connection: sqlite3.Connection, parent=None):
        super().__init__(parent)
        self.selected_concern = selected_concern
        print(f"LearnMorePage initialized for concern: {self.selected_concern}")
        self.conn = db_connection
        self.init_ui()

    # Fetch Learn More content from database
    def fetch_concern_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT what_is_it, why_it_matters, dos, donts 
            FROM learn_more 
            WHERE specific_concern = ?
        """, (self.selected_concern,))
        print('selected concern:', self.selected_concern)
        
        row = cursor.fetchone()
        if row:
            print("Learn More data fetched from DB:", row)
            return {
                "what_is_it": row[0],
                "why_it_matters": row[1],
                "dos": row[2],
                "donts": row[3]
            }
        return None
    
    def get_content(self):
        """Return the data dict for the PDF page"""
        data = self.fetch_concern_data()
        if data:
            return data
        return {
            "what_is_it": "Information not available.",
            "why_it_matters": "No data found.",
            "dos": "—",
            "donts": "—"
        }
    
    def init_ui(self):
        data = self.fetch_concern_data()

        if not data:
            data = {
                "what_is_it": "Information not available.",
                "why_it_matters": "No data found.",
                "dos": "—",
                "donts": "—"
            }

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

       
        # Title
        title = QLabel(f"📘 {self.selected_concern} - Learn More")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #0277BD;")
        layout.addWidget(title)

        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(18)

        cards = [
            ("📖 Definition", data["what_is_it"]),
            ("❗ Why it matters?", data["why_it_matters"]),
            ("✅ Dos", data["dos"]),
            ("❌ Don'ts", data["donts"])
        ]

        for c_title, text in cards:
            title_label = QLabel(f"<b>{c_title}</b>")
            title_label.setStyleSheet("font-size:16px; font-weight:bold; color:#0277BD;")
            container_layout.addWidget(title_label)

            content_label = QLabel(text.replace("\n", "<br>"))
            content_label.setWordWrap(True)
            content_label.setStyleSheet("""
                font-size: 14px;
                background-color: #E3F2FD;
                border-radius: 8px;
                padding: 10px 12px;
            """)
            container_layout.addWidget(content_label)
        
        container.setLayout(container_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        
        # Buttons
        download_btn = QPushButton("📥 Download PDF")
        download_btn.clicked.connect(lambda: self.download_pdf_clicked.emit(self.selected_concern))
        layout.addWidget(download_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton("🏠 Back to Dashboard")
        back_btn.clicked.connect(self.back_to_dashboard_clicked.emit)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

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
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
