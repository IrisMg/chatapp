import sqlite3

def fetch_questions(DB_PATH, quiz_type="concern", selected_concerns=None):
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    question_data = []

    if quiz_type == "concern":
        query = "SELECT id, area_of_concern, specific_concern, text, type FROM concern_questions"
        params = []
        if selected_concerns:
            placeholders = ",".join("?" for _ in selected_concerns)
            query += " WHERE " + " OR ".join("specific_concern LIKE ?" for _ in selected_concerns)
            params = [f"%{c}%" for c in selected_concerns]


        cursor.execute(query, params)
        questions = cursor.fetchall()

        for q_id, area, specific, text, q_type in questions:
            cursor.execute(
                "SELECT id, option_text, is_correct FROM concern_answer_options WHERE question_id=?",
                (q_id,)
            )
            options = cursor.fetchall()
            options = [(opt_id, opt_text, bool(is_correct)) for opt_id, opt_text, is_correct in options]

            question_data.append({
                "id": q_id,
                "area_of_concern": area,
                "specific_concern": specific,
                "text": text,
                "type": q_type,
                "options": options
            })

    elif quiz_type == "background":
        cursor.execute("SELECT id, text, type FROM userbackground_questions")
        questions = cursor.fetchall()
        for q_id, text, q_type in questions:
            cursor.execute(
                "SELECT id, text, NULL FROM userbackground_options WHERE question_id=?",
                (q_id,)
            )
            options = cursor.fetchall()
            options = [(opt_id, opt_text, None) for opt_id, opt_text, _ in options]

            question_data.append({
                "id": q_id,
                "text": text,
                "type": q_type,
                "options": options
            })
        
    conn.close()
    return question_data

def fetch_concern_data(self):
    cursor = self.conn.cursor()
    cursor.execute("""
        SELECT what_is_it, why_it_matters, dos, donts 
        FROM learn_more 
        WHERE specific_concern = ?
    """, (self.selected_concern,))
    
    row = cursor.fetchone()
    if row:
        return {
            "what_is_it": row[0],
            "why_it_matters": row[1],
            "dos": row[2],
            "donts": row[3]
        }
    return None




