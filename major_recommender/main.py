import sys
import re
from knowledge_base import KNOWLEDGE_BASE
from data import (
    DEFAULT_TRAINING_DATA, SYNONYMS, SUBJECTS
)
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QTabWidget, QStatusBar, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier

def normalize_text(text: str) -> str:
    """Lowercase and replace synonyms with canonical words."""
    text = text.lower()
    for synonym, canonical in SYNONYMS.items():
        text = re.sub(rf"\b{re.escape(synonym)}\b", canonical, text, flags=re.IGNORECASE)
    return text

def extract_subjects(text: str) -> str:
    """Extract recognized subject keywords from normalized text, prioritizing multi-word subjects."""
    text = normalize_text(text)
    found_subjects = set()

    # First, try to find multi-word subjects
    multi_word_subjects = sorted([s for s in SUBJECTS if ' ' in s], key=len, reverse=True)
    for mw_subject in multi_word_subjects:
        if mw_subject in text:
            found_subjects.add(mw_subject)
            # Replace found multi-word subject with a placeholder to avoid re-matching its parts
            text = text.replace(mw_subject, "")

    # Then, find individual word subjects from the remaining text
    tokens = re.findall(r"\b\w+\b", text)
    for token in tokens:
        if token in SUBJECTS:
            found_subjects.add(token)
            
    return " ".join(sorted(list(found_subjects))) # Sort for consistent output

def train_model(training_data):
    texts, labels = zip(*training_data)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    clf = DecisionTreeClassifier()
    clf.fit(X, labels)
    return clf, vectorizer

class AIMajorRecommendationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Find Your Future Major")
        self.setFixedSize(1366, 768)
        
        try:
            self.set_background("./major_recommender/image/background.png")
        except:
            self.setStyleSheet("background-color: #f0f0f0;")
        
        # Initialize model
        self.classifier, self.vectorizer = train_model(DEFAULT_TRAINING_DATA)
        
        self.init_ui()
        
    def init_ui(self):
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 100, 0, 50)
        main_layout.setSpacing(50)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(main_layout)

        # Title
        title = QLabel("Find Your Future Major")
        title.setFont(QFont("Comic Sans MS", 40, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c2c63;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Search Bar Layout
        search_layout = QHBoxLayout()
        search_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        search_layout.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setFixedHeight(50)
        self.search_box.setFixedWidth(600)
        self.search_box.setPlaceholderText("Enter your interests or favorite subjects...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 25px;
                padding-left: 20px;
                font-size: 18px;
                color: black;
                border: 0.5px solid #eee;
            }
        """)

        self.search_box.returnPressed.connect(self.recommend_major)
        search_layout.addWidget(self.search_box)

        # Search Button
        self.search_btn = QPushButton("🔍")
        self.search_btn.setFixedSize(50, 50)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: none;
                border-radius: 25px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.search_btn.clicked.connect(self.recommend_major)
        search_layout.addWidget(self.search_btn)

        # Cancel Button
        self.cancel_btn = QPushButton("❌")
        self.cancel_btn.setFixedSize(50, 50)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffdddd;
                border: none;
                border-radius: 25px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #ffcccc;
            }
        """)
        self.cancel_btn.clicked.connect(self.clear_all)
        search_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(search_layout)

        # Create Tab Widget
        tab_container = QHBoxLayout()
        tab_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tabs = QTabWidget()
        self.tabs.setFixedWidth(900)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 15px;
            }
            QTabBar::tab {
                background: #add8e6;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
            }
            QTabBar::tab:selected {
                background: #2c2c63;
                color: white;
            }
        """)

        self.create_major_uni_tab()
        self.create_curriculum_tab()
        self.create_career_tab()
        self.create_skills_tab()

        tab_container.addWidget(self.tabs)
        main_layout.addLayout(tab_container)

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: rgba(255, 255, 255, 0.7);
                color: #333;
                font-size: 14px;
                padding: 5px;
            }
        """)
        tab_layout = QHBoxLayout()
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tab_layout.addWidget(self.tabs)
        main_layout.addLayout(tab_layout)

    def create_major_uni_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.text_major_uni = QTextEdit()
        self.text_major_uni.setReadOnly(True)
        self.text_major_uni.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                font-size: 16px;
                color: black;
            }
        """)
        
        layout.addWidget(self.text_major_uni)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Major & University")

    def create_curriculum_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.text_curriculum = QTextEdit()
        self.text_curriculum.setReadOnly(True)
        self.text_curriculum.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                font-size: 16px;
                font-family: monospace;
                color: black;
            }
        """)
        
        layout.addWidget(self.text_curriculum)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Curriculum")

    def create_career_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.text_career = QTextEdit()
        self.text_career.setReadOnly(True)
        self.text_career.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                font-size: 16px;
                color: black;
            }
        """)
        
        layout.addWidget(self.text_career)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Career Paths")

    def create_skills_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.text_skills = QTextEdit()
        self.text_skills.setReadOnly(True)
        self.text_skills.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                font-size: 16px;
                color: black;
            }
        """)
        
        layout.addWidget(self.text_skills)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Skills & Growth")

    def set_background(self, path):
        background = QPixmap(path).scaled(
            self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

    def recommend_major(self):
        user_text = self.search_box.text().strip()
        if not user_text:
            self.status_bar.showMessage("⚠️ Please enter your favorite subjects or interests.", 5000)
            return

        # Extract normalized subjects
        processed_text = extract_subjects(user_text)
        if not processed_text:
            self.status_bar.showMessage(
                "❌ Sorry, no recognizable subjects found in your input. Try using keywords like 'biology', 'math', 'programming', 'design', 'history', etc.", 8000
            )
            self.clear_outputs()
            return

        X_test = self.vectorizer.transform([processed_text])
        predicted_major = self.classifier.predict(X_test)[0]

        # Fetch knowledge base details
        kb = KNOWLEDGE_BASE.get(predicted_major)
        if not kb:
            self.status_bar.showMessage(f"❌ No detailed information available for predicted major: {predicted_major}", 5000)
            self.clear_outputs()
            return

        self.update_recommendation_ui(predicted_major, kb)
        self.status_bar.showMessage(f"✅ Major '{predicted_major}' recommended based on your interests.", 8000)
        self.tabs.setCurrentIndex(0)

    def update_recommendation_ui(self, major, kb):
        # Major & Universities Tab
        uni_str = "\n   - ".join(kb["universities"])
        major_uni_text = (
            f"🎓 <b>Recommended Major</b>: {major} <br>"
            f"🏫 <b>Top Universities</b>:\n   - {uni_str} <br>"
            f"💰 <b>Average Tuition Fee (per year)</b>: ${kb['average_price']:,} <br>"
        )
        self.text_major_uni.setHtml(major_uni_text)

        # Curriculum Tab
        self.text_curriculum.setPlainText(kb.get("curriculum", "Curriculum information not available."))

        # Career Paths Tab
        career_str = "\n   - ".join(kb["career_paths"])
        career_detail = (
            f"💼 <b>Career Paths for {major}</b>:  - {career_str} <br>"
            f"💵 <b>Average Salary</b>: ${kb['average_salary']:,} per year <br>"
            f"📚 <b>Internships</b>:   - " + "  - ".join(kb.get("internships", ["N/A"])) + "<br>"
            f"🏅 <b>Professional Certifications</b>:   - " + "   - ".join(kb.get("professional_certifications", ["N/A"]))
        )
        self.text_career.setHtml(career_detail)

        # Skills & Growth Tab
        skills_detail = (
            f"🛠️ <b>Skills Required</b>: <br>"
            + "<br>".join([f"- {skill}" for skill in kb["skills_required"]])
            + f"<br>📈 <b>Growth Prospects</b>:{kb.get('growth_prospects', 'N/A')}"
        )
        self.text_skills.setHtml(skills_detail)

    def clear_outputs(self):
        self.text_major_uni.clear()
        self.text_curriculum.clear()
        self.text_career.clear()
        self.text_skills.clear()

    def clear_all(self):
        self.search_box.clear()
        self.clear_outputs()
        self.status_bar.clearMessage()
        self.tabs.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIMajorRecommendationApp()
    window.show()
    sys.exit(app.exec())