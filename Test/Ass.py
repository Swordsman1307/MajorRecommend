import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QGroupBox, QTabWidget, QStatusBar, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier

DEFAULT_TRAINING_DATA = [
    # Doctor
    ("I love biology and chemistry", "Doctor"),
    ("I want to study human anatomy and medicine", "Doctor"),
    ("Medical science and health interest me", "Doctor"),
    ("I am passionate about helping patients and surgery", "Doctor"),
    ("I want to become a general practitioner", "Doctor"),
    # Architect
    ("Math and art are my favorite", "Architect"),
    ("I want to design buildings and urban spaces", "Architect"),
    ("I enjoy technical drawing and creative design", "Architect"),
    ("I like planning cities and landscapes", "Architect"),
    ("I am interested in sustainable architecture", "Architect"),
    # IT
    ("Programming and computer science", "IT"),
    ("I want to learn software development and coding", "IT"),
    ("Computer networks and cybersecurity fascinate me", "IT"),
    ("I enjoy building apps and websites", "IT"),
    ("I like data science and machine learning", "IT"),
    # Designer (General, could be Graphic, Product, etc.)
    ("I like drawing and design", "Designer"),
    ("I love creating logos and digital art", "Designer"),
    ("Graphic design and visuals excite me", "Designer"),
    ("I want to work with Photoshop and Illustrator", "Designer"),
    ("I am passionate about UX and UI design", "Designer"),
    # Marketing
    ("I enjoy communication and english", "Marketing"),
    ("I like studying markets and advertising strategies", "Marketing"),
    ("I want to understand consumer behavior", "Marketing"),
    ("I am interested in digital marketing and social media", "Marketing"),
    ("Brand management and promotion fascinate me", "Marketing"),
    # Business
    ("Economics and math interest me", "Business"),
    ("I want to start my own company and learn management", "Business"),
    ("Finance and entrepreneurship excite me", "Business"),
    ("I enjoy studying business strategies and markets", "Business"),
    ("I am passionate about leadership and negotiation", "Business"),
    # Lawyer
    ("History and civics are my strong points", "Lawyer"),
    ("I enjoy debating laws and legal systems", "Lawyer"),
    ("I want to study criminal and civil law", "Lawyer"),
    ("I am interested in human rights and justice", "Lawyer"),
    ("Legal research and courtroom work excite me", "Lawyer"),
    # Psychology
    ("I am interested in human behavior and mind", "Psychology"),
    ("I want to understand mental health and therapy", "Psychology"),
    ("I enjoy studying cognitive processes and emotions", "Psychology"),
    ("I am fascinated by behavioral science", "Psychology"),
    ("I want to help people with psychological issues", "Psychology"),
    # Engineering (General)
    ("I like building and designing machines", "Engineering"),
    ("I enjoy physics and solving engineering problems", "Engineering"),
    ("I want to work on mechanical systems and robotics", "Engineering"),
    ("I am interested in electrical and civil engineering", "Engineering"),
    ("I like designing innovative technology solutions", "Engineering"),
    # Finance
    ("Finance, stocks and investments interest me", "Finance"),
    ("I want to learn about financial markets and banking", "Finance"),
    ("I enjoy portfolio management and analysis", "Finance"),
    ("Economics and accounting fascinate me", "Finance"),
    ("I am passionate about risk management and auditing", "Finance"),
    # Education
    ("Teaching and learning new things excites me", "Education"),
    ("I want to become a teacher and help students learn", "Education"),
    ("I enjoy curriculum development and pedagogy", "Education"),
    ("I am interested in educational psychology", "Education"),
    ("I want to promote lifelong learning and training", "Education"),
    # Journalism
    ("I enjoy writing and news reporting", "Journalism"),
    ("I want to work in media and broadcasting", "Journalism"),
    ("I like investigative journalism and storytelling", "Journalism"),
    ("I am interested in press ethics and freedom", "Journalism"),
    ("I want to cover current events and social issues", "Journalism"),
    # Environmental Science
    ("I care about the environment and sustainability", "Environmental Science"),
    ("I want to work on climate change and conservation", "Environmental Science"),
    ("I enjoy studying ecosystems and biodiversity", "Environmental Science"),
    ("I am interested in renewable energy and green tech", "Environmental Science"),
    ("I want to promote environmental policies and education", "Environmental Science"),
    # Graphic Design
    ("I love creating graphics and visuals", "Graphic Design"),
    ("I want to design posters, ads, and brand materials", "Graphic Design"),
    ("I enjoy digital art and animation", "Graphic Design"),
    ("I am passionate about creative software and typography", "Graphic Design"),
    ("I want to build strong visual communication skills", "Graphic Design"),
    # Civil Engineering
    ("I want to build bridges and roads", "Civil Engineering"),
    ("I am interested in structural design and construction", "Civil Engineering"),
    ("I enjoy working on infrastructure projects", "Civil Engineering"),
    ("I like surveying and materials engineering", "Civil Engineering"),
    ("I want to improve urban planning and transportation", "Civil Engineering"),
]

SYNONYMS = {
    "coding": "programming",
    "software": "programming",
    "development": "programming",
    "drawing": "design",
    "visuals": "design",
    "communication": "english",
    "law": "civics",
    "machines": "engineering",
    "teaching": "education",
    "stocks": "finance",
    "environment": "sustainability",
    "graphics": "design"
}

# Added multi-word subjects for better recognition
SUBJECTS = {
    "biology", "chemistry", "math", "art", "programming", "computer", "science",
    "design", "english", "economics", "history", "civics", "psychology",
    "engineering", "finance", "education", "journalism", "sustainability",
    "computer science", "digital marketing", "social media", "machine learning",
    "human anatomy", "medical science", "urban planning", "civil engineering",
    "environmental science", "graphic design", "electrical engineering",
    "mechanical engineering", "data science", "user experience", "user interface",
    "ux design", "ui design" # Explicitly add UX/UI
}

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

KNOWLEDGE_BASE = {
    "Doctor": {
        "universities": ["Harvard University", "Johns Hopkins University", "Stanford University"],
        "average_price": 55000,
        "career_paths": ["Surgeon", "General Practitioner", "Medical Researcher"],
        "average_salary": 150000,
        "skills_required": ["Anatomy knowledge", "Attention to detail", "Strong communication"],
        "growth_prospects": "High demand globally with many specialization options.",
        "internships": ["Hospital Internship", "Medical Research Assistant"],
        "professional_certifications": ["USMLE", "Board Certification"],
        "curriculum": """Year 1-2: Basic sciences (Anatomy, Biochemistry, Physiology)
Year 3: Clinical rotations (Surgery, Pediatrics, Internal Medicine)
Year 4: Clinical rotations continuation
Year 5+: Specializations, Research projects"""
    },
    "Architect": {
        "universities": ["MIT", "University of California, Berkeley", "University of Michigan"],
        "average_price": 42000,
        "career_paths": ["Architect", "Urban Planner", "Interior Designer"],
        "average_salary": 80000,
        "skills_required": ["Creative design", "Technical drawing", "Project management"],
        "growth_prospects": "Moderate growth with urbanization and renovation demands.",
        "internships": ["Architecture firm internship", "Urban planning agencies"],
        "professional_certifications": ["AIA Membership", "LEED Accredited Professional"],
        "curriculum": """Year 1: Fundamentals of Design and Drawing
Year 2: Structural Systems
Year 3: Environmental Design
Year 4: Professional Practice
Year 5: Thesis Project"""
    },
    "IT": {
        "universities": ["MIT", "Stanford University", "Carnegie Mellon University"],
        "average_price": 47000,
        "career_paths": ["Software Engineer", "Data Scientist", "Cybersecurity Analyst"],
        "average_salary": 90000,
        "skills_required": ["Programming", "Data Analysis", "Problem Solving"],
        "growth_prospects": "Very high with rapid tech evolution and demand.",
        "internships": ["Tech company internships", "Research labs"],
        "professional_certifications": ["AWS Certified", "Cisco CCNA", "Certified Data Scientist"],
        "curriculum": """Year 1: Programming, Data Structures, Algorithms
Year 2: Programming, Data Structures, Algorithms continued
Year 3: Databases, Networks, Operating Systems
Year 4: AI, Cybersecurity, Capstone Project"""
    },
    "Designer": {
        "universities": ["Rhode Island School of Design", "Parsons School of Design", "Savannah College of Art and Design"],
        "average_price": 38000,
        "career_paths": ["Graphic Designer", "UI/UX Designer", "Product Designer"],
        "average_salary": 65000,
        "skills_required": ["Creativity", "Software skills (Photoshop, Illustrator)", "Communication"],
        "growth_prospects": "Growing with digital and product design demand.",
        "internships": ["Design studios", "Marketing agencies"],
        "professional_certifications": ["Adobe Certified Expert", "Certified UX Professional"],
        "curriculum": """Year 1: Fundamentals of Design
Year 2: Digital Media and Tools
Year 3: Digital Media and Tools continued
Year 4: Portfolio Development and Internship"""
    },
    "Marketing": {
        "universities": ["University of Pennsylvania", "Northwestern University", "University of Michigan"],
        "average_price": 40000,
        "career_paths": ["Marketing Manager", "Brand Strategist", "Digital Marketing Specialist"],
        "average_salary": 70000,
        "skills_required": ["Communication", "Data Analysis", "Creativity"],
        "growth_prospects": "Steady growth with focus on digital marketing.",
        "internships": ["Advertising agencies", "Corporate marketing departments"],
        "professional_certifications": ["Google Ads Certification", "HubSpot Content Marketing"],
        "curriculum": """Year 1: Principles of Marketing and Communication
Year 2: Principles of Marketing and Communication continued
Year 3: Market Research, Digital Marketing
Year 4: Marketing Strategy and Campaigns"""
    },
    "Business": {
        "universities": ["Harvard Business School", "Wharton School", "London Business School"],
        "average_price": 60000,
        "career_paths": ["Business Analyst", "Entrepreneur", "Management Consultant"],
        "average_salary": 85000,
        "skills_required": ["Leadership", "Financial literacy", "Strategic thinking"],
        "growth_prospects": "Consistent demand in all sectors.",
        "internships": ["Consulting firms", "Corporate business units"],
        "professional_certifications": ["MBA", "PMP"],
        "curriculum": """Year 1: Fundamentals of Business and Economics
Year 2: Fundamentals of Business and Economics continued
Year 3: Finance, Management
Year 4: Strategic Planning and Entrepreneurship"""
    },
    "Lawyer": {
        "universities": ["Harvard Law School", "Yale Law School", "Stanford Law School"],
        "average_price": 55000,
        "career_paths": ["Corporate Lawyer", "Public Defender", "Judge"],
        "average_salary": 120000,
        "skills_required": ["Critical thinking", "Negotiation", "Legal knowledge"],
        "growth_prospects": "Competitive but stable demand.",
        "internships": ["Law firms", "Government legal offices"],
        "professional_certifications": ["Bar Exam", "Legal Practice Course"],
        "curriculum": """Year 1: Legal Foundations
Year 2: Legal Foundations continued
Year 3: Specializations and Moot Courts
Year 4: Specializations and Moot Courts continued
Year 5: Internship and Bar Preparation"""
    },
    "Psychology": {
        "universities": ["University of California, Berkeley", "University of Cambridge", "University of Oxford"],
        "average_price": 35000,
        "career_paths": ["Clinical Psychologist", "Counselor", "Researcher"],
        "average_salary": 70000,
        "skills_required": ["Empathy", "Research skills", "Critical thinking"],
        "growth_prospects": "Increasing demand in mental health awareness.",
        "internships": ["Hospitals", "Counseling centers"],
        "professional_certifications": ["Licensed Psychologist", "Certified Counselor"],
        "curriculum": """Year 1: Intro to Psychology, Research Methods
Year 2: Intro to Psychology continued
Year 3: Clinical Psychology, Counseling Techniques
Year 4: Clinical Psychology continued
Year 5+: Practicum and Thesis"""
    },
    "Engineering": {
        "universities": ["MIT", "Stanford University", "California Institute of Technology"],
        "average_price": 48000,
        "career_paths": ["Mechanical Engineer", "Electrical Engineer", "Project Engineer"],
        "average_salary": 90000,
        "skills_required": ["Math and physics", "Problem solving", "Technical skills"],
        "growth_prospects": "Strong demand in multiple industries.",
        "internships": ["Engineering firms", "Manufacturing companies"],
        "professional_certifications": ["PE License", "Six Sigma"],
        "curriculum": """Year 1: Math, Physics, Basic Engineering
Year 2: Math, Physics, Basic Engineering continued
Year 3: Specialized Engineering Courses
Year 4: Specialized Engineering Courses continued
Year 5: Capstone Project and Internship"""
    },
    "Finance": {
        "universities": ["Wharton School", "London School of Economics", "University of Chicago"],
        "average_price": 45000,
        "career_paths": ["Financial Analyst", "Investment Banker", "Portfolio Manager"],
        "average_salary": 95000,
        "skills_required": ["Analytical skills", "Financial modeling", "Attention to detail"],
        "growth_prospects": "High in banking and investment sectors.",
        "internships": ["Investment banks", "Financial institutions"],
        "professional_certifications": ["CFA", "CPA"],
        "curriculum": """Year 1: Finance, Accounting, Economics
Year 2: Finance, Accounting, Economics continued
Year 3: Investment Analysis, Risk Management
Year 4: Investment Analysis continued
Year 5: Internship and Thesis"""
    },
    "Education": {
        "universities": ["University of Wisconsin-Madison", "University of Toronto", "University of Melbourne"],
        "average_price": 32000,
        "career_paths": ["Teacher", "Curriculum Developer", "Educational Consultant"],
        "average_salary": 55000,
        "skills_required": ["Communication", "Patience", "Subject expertise"],
        "growth_prospects": "Stable with regional variations.",
        "internships": ["Schools", "Educational NGOs"],
        "professional_certifications": ["Teaching License", "TESOL"],
        "curriculum": """Year 1: Educational Psychology, Pedagogy
Year 2: Educational Psychology, Pedagogy continued
Year 3: Curriculum Design, Practicum
Year 4: Curriculum Design, Practicum continued
Year 5: Student Teaching Internship"""
    },
    "Journalism": {
        "universities": ["Columbia University", "Northwestern University", "University of Missouri"],
        "average_price": 38000,
        "career_paths": ["Reporter", "Editor", "Broadcast Journalist"],
        "average_salary": 60000,
        "skills_required": ["Writing skills", "Research", "Critical thinking"],
        "growth_prospects": "Changing industry, but demand for digital journalism.",
        "internships": ["News agencies", "Media outlets"],
        "professional_certifications": ["Certified Journalism Professional"],
        "curriculum": """Year 1: News Writing, Media Ethics
Year 2: News Writing, Media Ethics continued
Year 3: Broadcast Journalism, Investigative Reporting
Year 4: Broadcast Journalism continued
Year 5: Internship and Portfolio Development"""
    },
    "Environmental Science": {
        "universities": ["University of California, Davis", "University of Edinburgh", "ETH Zurich"],
        "average_price": 40000,
        "career_paths": ["Environmental Consultant", "Research Scientist", "Conservationist"],
        "average_salary": 65000,
        "skills_required": ["Field research", "Data analysis", "Problem solving"],
        "growth_prospects": "Growing with environmental concerns worldwide.",
        "internships": ["Environmental agencies", "NGOs"],
        "professional_certifications": ["Certified Environmental Scientist"],
        "curriculum": """Year 1: Ecology, Chemistry, Geography
Year 2: Ecology, Chemistry, Geography continued
Year 3: Environmental Policy, Research Methods
Year 4: Environmental Policy continued
Year 5: Field Work and Thesis"""
    },
    "Graphic Design": {
        "universities": ["California Institute of the Arts", "Royal College of Art", "Savannah College of Art and Design"],
        "average_price": 35000,
        "career_paths": ["Graphic Designer", "Art Director", "Illustrator"],
        "average_salary": 60000,
        "skills_required": ["Creativity", "Adobe Suite", "Typography"],
        "growth_prospects": "Good growth in digital media.",
        "internships": ["Design studios", "Advertising agencies"],
        "professional_certifications": ["Adobe Certified Expert"],
        "curriculum": """Year 1: Design Fundamentals
Year 2: Digital Illustration, Typography
Year 3: Digital Illustration, Typography continued
Year 4: Portfolio Development"""
    },
    "Civil Engineering": {
        "universities": ["Georgia Institute of Technology", "University of Illinois Urbana-Champaign", "University of Texas at Austin"],
        "average_price": 45000,
        "career_paths": ["Structural Engineer", "Construction Manager", "Transportation Engineer"],
        "average_salary": 80000,
        "skills_required": ["Math and physics", "Project management", "Design software"],
        "growth_prospects": "Good with infrastructure projects worldwide.",
        "internships": ["Construction companies", "Engineering firms"],
        "professional_certifications": ["PE License"],
        "curriculum": """Year 1: Math, Physics, Engineering Basics
Year 2: Math, Physics, Engineering Basics continued
Year 3: Structural Design, Materials Science
Year 4: Construction Management, Transportation Engineering
Year 5: Internship and Capstone Project""" 
    },
}
# [Previous training data and knowledge base remains the same...]

class AIMajorRecommendationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Find Your Future Major")
        self.setFixedSize(1366, 768)
        
        try:
            self.set_background("./Test/img/background.png")
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
        self.tabs.setFixedWidth(900)  # Optional: fixed width to center more nicely
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 15px;
            }
            QTabBar::tab {
                background: #f0f0f0;
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

        # Update UI with recommendation
        self.update_recommendation_ui(predicted_major, kb)
        self.status_bar.showMessage(f"✅ Major '{predicted_major}' recommended based on your interests.", 8000)
        self.tabs.setCurrentIndex(0)

    def update_recommendation_ui(self, major, kb):
        # Major & Universities Tab
        uni_str = "\n   - ".join(kb["universities"])
        major_uni_text = (
            f"🎓 <b>Recommended Major</b>: {major}\n\n"
            f"🏫 <b>Top Universities</b>:\n   - {uni_str}\n\n"
            f"💰 <b>Average Tuition Fee (per year)</b>: ${kb['average_price']:,}\n"
        )
        self.text_major_uni.setHtml(major_uni_text)

        # Curriculum Tab
        self.text_curriculum.setPlainText(kb.get("curriculum", "Curriculum information not available."))

                # Career Paths Tab
        career_str = "\n   - ".join(kb["career_paths"])
        career_detail = (
            f"💼 <b>Career Paths for {major}</b>:\n   - {career_str}\n\n"
            f"💵 <b>Average Salary</b>: ${kb['average_salary']:,} per year\n\n"
            f"📚 <b>Internships</b>:\n   - " + "\n   - ".join(kb.get("internships", ["N/A"])) + "\n\n"
            f"🏅 <b>Professional Certifications</b>:\n   - " + "\n   - ".join(kb.get("professional_certifications", ["N/A"]))
        )
        self.text_career.setHtml(career_detail)

        # Skills & Growth Tab
        skills_detail = (
            f"🛠️ <b>Skills Required</b>:\n"
            + "\n".join([f"- {skill}" for skill in kb["skills_required"]])
            + f"\n\n📈 <b>Growth Prospects</b>:\n{kb.get('growth_prospects', 'N/A')}"
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