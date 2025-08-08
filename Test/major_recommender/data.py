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
    "ux design", "ui design"
}