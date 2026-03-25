from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from PIL import Image


ROOT = Path(r"e:\Christ University\Trimester 6\Project")
OUTPUT = ROOT / "CareerPilot_AI_Project_Report_60_Pages.docx"

SCREENSHOTS = [
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416053707.png"),
        "caption": "Fig. 4.1 Landing page hero section of CareerPilot AI",
        "title": "LANDING PAGE HERO INTERFACE",
        "text": "The landing page introduces the platform as an AI-powered career companion. The hero section communicates the product value proposition, highlights the platform's focus on personalized guidance, and directs new users toward registration or sign-in actions.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416060227.png"),
        "caption": "Fig. 4.2 Feature cards and call-to-action section on the landing page",
        "title": "LANDING PAGE FEATURES AND CALL TO ACTION",
        "text": "This section of the landing page summarizes core capabilities such as AI roadmap generation, daily plans, and interactive topic learning. The lower call-to-action banner encourages conversion from visitor to registered user and improves onboarding clarity.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416065617.png"),
        "caption": "Fig. 4.3 User registration interface",
        "title": "REGISTRATION PAGE",
        "text": "The registration page collects full name, email, username, and password in a minimal form layout. Input validation and a clear primary action button are used to reduce registration friction and establish secure account creation.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416070145.png"),
        "caption": "Fig. 4.4 Login page for authenticated access",
        "title": "LOGIN PAGE",
        "text": "The login page supports returning users through a simple username and password workflow. Its design focuses on usability, rapid authentication, and consistent visual identity with the remainder of the platform.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416075452.png"),
        "caption": "Fig. 4.5 Dashboard overview showing progress metrics and quick actions",
        "title": "DASHBOARD OVERVIEW",
        "text": "After authentication, the dashboard presents a consolidated summary of the learner's current status. Metrics such as number of roadmaps, completed days, streak count, pending tasks, and overall progress help the user understand present readiness at a glance.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416083442.png"),
        "caption": "Fig. 4.6 Dashboard section with recent roadmaps and motivational panel",
        "title": "DASHBOARD SUPPORTING SECTIONS",
        "text": "The lower dashboard region provides continuity features such as recent roadmaps and motivational guidance. These elements reinforce user engagement by surfacing active learning paths and encouraging sustained completion behavior.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416091309.png"),
        "caption": "Fig. 4.7 Skill customization interface before roadmap generation",
        "title": "ROADMAP SKILL CUSTOMIZATION",
        "text": "The roadmap generation workflow permits users to review AI-suggested skills and append their own custom skill tags before final generation. This step increases personalization and allows the roadmap to reflect individual interests or project-specific needs.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416099649.png"),
        "caption": "Fig. 4.8 Generated roadmap overview with required skills and learning path",
        "title": "GENERATED ROADMAP OVERVIEW",
        "text": "The generated roadmap displays role-specific required skills and breaks them into sequential learning phases. This page operationalizes the core project objective by converting an abstract career target into a practical plan with milestones.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416108645.png"),
        "caption": "Fig. 4.9 Recommended project list and daily plan generation action",
        "title": "ROADMAP PROJECT RECOMMENDATIONS",
        "text": "The lower roadmap section proposes project ideas aligned to the selected path and offers a direct action to generate a daily plan. This bridge from static roadmap content to executable daily tasks is one of the system's key integration points.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416118617.png"),
        "caption": "Fig. 4.10 Daily learning plan interface with day-wise progress tracking",
        "title": "DAILY LEARNING PLAN INTERFACE",
        "text": "The daily plan page expands a generated roadmap into a day-wise checklist. Completed days are highlighted visually, estimated study hours are shown for each day, and the progress bar quantifies journey completion within the selected role.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416129814.png"),
        "caption": "Fig. 4.11 Interactive learning page for AI-generated topic explanations",
        "title": "INTERACTIVE LEARNING PAGE",
        "text": "The learn page accepts any topic entered by the user and is designed to return AI-generated conceptual explanations, examples, and resource suggestions. It turns the system into an on-demand study assistant rather than a static planning tool.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416144697.png"),
        "caption": "Fig. 4.12 Smart mock test generation page",
        "title": "SMART MOCK TEST PAGE",
        "text": "The smart mock test page allows the learner to configure the number of MCQ and coding questions, review time allocation, and generate assessments strictly from completed topics. This design ensures both relevance and progressive difficulty control.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416156697.png"),
        "caption": "Fig. 4.13 Performance analytics dashboard",
        "title": "PERFORMANCE ANALYTICS PAGE",
        "text": "The performance page summarizes testing progress through total tests completed, average score, best score, trend indicators, strong areas, and areas for improvement. This page closes the learning loop by turning test outcomes into measurable insight.",
    },
    {
        "path": Path(r"C:\Users\SHAHID\AppData\Roaming\Code\User\workspaceStorage\vscode-chat-images\image-1773416169864.png"),
        "caption": "Fig. 4.14 User profile page with account details and learning statistics",
        "title": "PROFILE PAGE",
        "text": "The profile page presents user identity information together with high-level learning statistics and account actions. It centralizes essential account data and gives the learner a clear summary of personal platform activity.",
    },
]


def set_font(run, size=12, bold=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold


def set_cell_text(cell, text, bold=False, size=10):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(str(text))
    set_font(r, size=size, bold=bold)


def add_page_number(footer_paragraph):
    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_paragraph.add_run()
    set_font(run, size=10)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.append(fld)


def configure_document(doc):
    for section in doc.sections:
        section.left_margin = Inches(1.5)
        section.right_margin = Inches(1.0)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.header_distance = Inches(0.3)
        section.footer_distance = Inches(0.3)
        for p in section.header.paragraphs:
            p.clear()
        footer = section.footer
        for p in footer.paragraphs:
            p.clear()
        add_page_number(footer.paragraphs[0])

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(12)


def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text.upper())
    set_font(r, size=16, bold=True)
    return p


def add_subheading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text.upper())
    set_font(r, size=12, bold=True)
    return p


def add_body(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    set_font(r, size=12)
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run(text)
    set_font(r, size=12)
    return p


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    set_font(r, size=10, bold=True)
    return p


def add_image(doc, image_path):
    with Image.open(image_path) as img:
        width_px, height_px = img.size
    max_width = 6.0
    max_height = 6.2
    ratio = min(max_width / width_px, max_height / height_px)
    width_inches = width_px * ratio
    doc.add_picture(str(image_path), width=Inches(width_inches))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_table(doc, rows, title=None, col_widths=None, font_size=10):
    if title:
        add_caption(doc, title)
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    table.autofit = True
    for r_idx, row in enumerate(rows):
        for c_idx, value in enumerate(row):
            set_cell_text(table.cell(r_idx, c_idx), value, bold=(r_idx == 0), size=font_size)
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
    return table


def add_toc_table(doc, rows):
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = "Table Grid"
    for idx, (title, page) in enumerate(rows):
        set_cell_text(table.cell(idx, 0), title, bold=(idx == 0), size=11)
        set_cell_text(table.cell(idx, 1), page, bold=(idx == 0), size=11)
        table.cell(idx, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    return table


def page_break(doc, current_page, total_pages):
    if current_page < total_pages:
        doc.add_page_break()


def add_standard_page(doc, title, paragraphs=None, bullets=None, table=None, table_title=None):
    add_title(doc, title)
    for paragraph in paragraphs or []:
        add_body(doc, paragraph)
    for bullet in bullets or []:
        add_bullet(doc, bullet)
    if table is not None:
        add_table(doc, table, title=table_title)


def add_image_page(doc, spec):
    add_title(doc, spec["title"])
    add_body(doc, spec["text"])
    add_image(doc, spec["path"])
    add_caption(doc, spec["caption"])


def build_pages():
    pages = []

    pages.append({
        "title": "CAREERPILOT AI",
        "paragraphs": [
            "A Project Report submitted in partial fulfillment of the requirements for the Bachelor of Computer Applications programme in the Department of Computer Science, CHRIST (Deemed to be University).",
            "Project Title: CareerPilot AI - An AI-Powered Career Roadmap, Daily Planning, Assessment, and Learning Platform.",
            "Submitted by: Mohammad Shahid Raza.",
            "Academic Year: 2025-2026.",
            "Guide: ________________________________."
        ],
        "centered": True,
    })

    pages.append({
        "title": "CERTIFICATE",
        "paragraphs": [
            "This is to certify that the project entitled CareerPilot AI is a bonafide work carried out by the student under the guidance of the project supervisor in the Department of Computer Science, CHRIST (Deemed to be University), during the academic year 2025-2026.",
            "The work presented in this report is original and has not been submitted, either in part or in full, to any other university or institution for the award of any degree, diploma, or similar academic recognition.",
            "Project Guide Signature: ________________________________.",
            "Head of Department Signature: _________________________."
        ]
    })

    pages.append({
        "title": "ACKNOWLEDGMENTS",
        "paragraphs": [
            "The successful completion of this project was possible because of the continued support, guidance, and encouragement received throughout its development. I express sincere gratitude to my project guide for providing valuable direction in planning the system, evaluating design choices, and reviewing the implementation of the platform.",
            "I also thank the Department of Computer Science, CHRIST (Deemed to be University), for providing the academic environment and structure needed to complete a full-stack software project with practical relevance. The feedback from faculty members and peers helped improve the usability, presentation, and overall quality of the system.",
            "Finally, I acknowledge the support of my family and friends whose encouragement helped me remain focused during the design, development, testing, and documentation stages of CareerPilot AI."
        ]
    })

    pages.append({
        "title": "ABSTRACT",
        "paragraphs": [
            "CareerPilot AI is a full-stack educational technology platform designed to convert career aspirations into structured, measurable, and adaptive learning journeys. The system integrates a FastAPI backend, PostgreSQL database, and Next.js frontend to provide secure authentication, AI-generated roadmaps, daily learning plans, intelligent topic explanations, mock tests, coding assessment, performance analytics, and profile management. By combining planning, execution, and feedback within one platform, the system addresses a common limitation of conventional learning portals, namely the lack of continuity between career goals and everyday study activity.",
            "The application uses role-based personalization so that a learner can choose a target role, receive a roadmap of skills and phases, and then expand that roadmap into daily tasks. Progress tracking and mock-test generation are tied to completed topics, thereby ensuring that the assessment engine remains relevant to actual learning history. Performance data is stored and analyzed to produce trend-based metrics, strong and weak areas, and readiness indicators.",
            "The project demonstrates the feasibility of an AI-supported career preparation environment that is practical for student use, extensible for future analytics enhancements, and suitable for deployment using contemporary cloud platforms."
        ]
    })

    toc_rows = [
        ["SECTION", "PAGE NO."],
        ["Acknowledgments", "3"],
        ["Abstract", "4"],
        ["1. Introduction", "9"],
        ["2. System Analysis and Requirements", "14"],
        ["3. System Design", "21"],
        ["4. Implementation", "31"],
        ["5. Testing", "50"],
        ["6. Conclusion", "56"],
        ["Appendix", "59"],
        ["References", "60"],
    ]
    pages.append({"title": "TABLE OF CONTENTS", "table": toc_rows, "table_title": None})

    list_tables_rows = [
        ["TABLE NO.", "TITLE", "PAGE NO."],
        ["Table 2.1", "Functional Requirements of the Proposed System", "16"],
        ["Table 2.2", "Non-Functional Requirements", "17"],
        ["Table 2.3", "Software and Hardware Requirements", "19"],
        ["Table 3.1", "Core Backend and Frontend Modules", "23"],
        ["Table 3.2", "Core Database Tables", "25"],
        ["Table 3.3", "Assessment and Testing Tables", "26"],
        ["Table 3.4", "Career Intelligence Tables", "27"],
        ["Table 4.1", "Coding Standards and Development Practices", "32"],
        ["Table 5.1", "Authentication and Profile Test Cases", "51"],
        ["Table 5.2", "Roadmap and Daily Plan Test Cases", "52"],
        ["Table 5.3", "Mock Test and Analytics Test Cases", "53"],
        ["Table 5.4", "Observed Test Report Summary", "54"],
        ["Table 6.1", "Advantages and Limitations", "57"],
    ]
    pages.append({"title": "LIST OF TABLES", "table": list_tables_rows})

    list_figures_rows = [
        ["FIGURE NO.", "TITLE", "PAGE NO."],
        ["Fig. 4.1", "Landing page hero section of CareerPilot AI", "36"],
        ["Fig. 4.2", "Feature cards and call-to-action section on the landing page", "37"],
        ["Fig. 4.3", "User registration interface", "38"],
        ["Fig. 4.4", "Login page for authenticated access", "39"],
        ["Fig. 4.5", "Dashboard overview showing progress metrics and quick actions", "40"],
        ["Fig. 4.6", "Dashboard section with recent roadmaps and motivational panel", "41"],
        ["Fig. 4.7", "Skill customization interface before roadmap generation", "42"],
        ["Fig. 4.8", "Generated roadmap overview with required skills and learning path", "43"],
        ["Fig. 4.9", "Recommended project list and daily plan generation action", "44"],
        ["Fig. 4.10", "Daily learning plan interface with day-wise progress tracking", "45"],
        ["Fig. 4.11", "Interactive learning page for AI-generated topic explanations", "46"],
        ["Fig. 4.12", "Smart mock test generation page", "47"],
        ["Fig. 4.13", "Performance analytics dashboard", "48"],
        ["Fig. 4.14", "User profile page with account details and learning statistics", "49"],
    ]
    pages.append({"title": "LIST OF FIGURES", "table": list_figures_rows})

    pages.append({
        "title": "LIST OF ABBREVIATIONS",
        "paragraphs": [
            "AI - Artificial Intelligence.",
            "API - Application Programming Interface.",
            "JWT - JSON Web Token.",
            "ORM - Object Relational Mapper.",
            "LLM - Large Language Model.",
            "UI - User Interface.",
            "UX - User Experience.",
            "MCQ - Multiple Choice Question.",
            "SQL - Structured Query Language.",
            "ER - Entity Relationship.",
            "KPI - Key Performance Indicator.",
            "JSON - JavaScript Object Notation."
        ]
    })

    pages.extend([
        {
            "title": "CHAPTER 1: INTRODUCTION",
            "paragraphs": [
                "Career development has become increasingly nonlinear, requiring learners to combine planning, self-directed study, practice, and continuous assessment. Students often know the role they want to pursue, yet they struggle to identify which skills to learn first, how much time to allocate, and how to measure actual progress in a disciplined way.",
                "CareerPilot AI was conceived to solve this practical problem by integrating roadmap generation, day-wise planning, AI-assisted learning, and performance evaluation into a single application. Instead of separating these functions across multiple tools, the proposed system combines them into an end-to-end environment where each module contributes to a coherent learning journey.",
                "The project is implemented as a full-stack web application in which a Next.js frontend communicates with a FastAPI backend secured through JWT authentication and backed by a PostgreSQL database."
            ]
        },
        {
            "title": "PROJECT DESCRIPTION",
            "paragraphs": [
                "CareerPilot AI is an intelligent career planning platform that allows a learner to enter a target role and receive a generated roadmap of required skills, phases, and suggested projects. The generated roadmap is not intended to remain a static output. It becomes the basis for a more detailed daily learning plan, which is then tracked by the user through completion indicators and progress summaries.",
                "The system also includes a learning assistant module in which the learner can request AI explanations of any topic. This gives the platform both planning and instructional capabilities. The same role-based context is used to generate mock tests so that users are assessed only on topics they have already completed, thereby keeping testing personalized and pedagogically relevant."
            ]
        },
        {
            "title": "EXISTING SYSTEM",
            "paragraphs": [
                "Most existing systems related to technical learning solve only isolated parts of the problem. Course platforms provide content but usually do not map learning to a target career role. Coding practice platforms provide assessment but generally assume the learner already knows what to study. Productivity applications support checklists but lack domain intelligence and personalized technical progression.",
                "Because these systems are fragmented, learners must manually combine roadmaps, notes, practice problems, progress tracking, and feedback. This fragmentation creates inefficiency, inconsistency, and poor long-term discipline. CareerPilot AI improves upon these limitations by linking planning, action, and evaluation through a shared user-role context."
            ]
        },
        {
            "title": "OBJECTIVES, PURPOSE, AND SCOPE",
            "paragraphs": [
                "The primary objective of the project is to build a secure web platform that transforms a chosen career role into a structured learning journey supported by day-wise tasks and measurable assessments. The platform is intended to help students and self-learners maintain continuity between ambition and execution.",
                "The purpose of the system is to reduce ambiguity in career preparation, improve study consistency, and provide evidence-based feedback through testing and analytics. The scope of the project includes user authentication, roadmap generation, daily planning, topic learning, mock tests, performance reporting, and account/profile management."
            ],
            "bullets": [
                "Generate role-based roadmaps for target technical careers.",
                "Convert roadmap phases into daily learning plans.",
                "Provide AI-driven explanations for requested topics.",
                "Generate personalized mock tests from completed topics.",
                "Track user performance through analytics and profile statistics."
            ]
        },
        {
            "title": "APPLICABILITY AND OVERVIEW OF THE REPORT",
            "paragraphs": [
                "The system is applicable to undergraduate students, placement candidates, career switchers, and self-taught learners who need structure in technical preparation. It may also support mentors or instructors who want to recommend guided progression paths for learners with different goals.",
                "The remainder of this report is organized as follows. Chapter 2 defines the problem in engineering terms and specifies functional and non-functional requirements. Chapter 3 discusses the design of the architecture, modules, database, and interfaces. Chapter 4 describes implementation decisions and presents screenshots of the completed product. Chapter 5 records testing approaches and outcomes, while Chapter 6 concludes the work with advantages, limitations, and future scope."
            ]
        },
        {
            "title": "CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENTS",
            "paragraphs": [
                "System analysis was carried out by considering the needs of a learner who wants to prepare for a software role in a structured and measurable way. The analysis identified a recurring gap between high-level aspiration and day-to-day execution. Learners frequently begin with enthusiasm but fail to sustain progress because there is no coherent link between planning, learning, practice, and feedback.",
                "The proposed system therefore has to act not merely as a content source, but as a guided workflow engine. The backend must store users, roles, plans, tests, and analytics, while the frontend must expose those features through a clear route-driven experience."
            ]
        },
        {
            "title": "PROBLEM DEFINITION",
            "paragraphs": [
                "The central problem addressed by the project is the absence of an integrated platform that can personalize a technical learning path for a specific career role and then keep the learner accountable through executable daily tasks and assessments. Traditional systems are either static or domain-limited, causing users to depend on manual planning and self-enforced consistency.",
                "From a software engineering perspective, this problem can be decomposed into several sub-problems: user identity management, role-specific content generation, daily task scheduling, topic clarification, test generation, code evaluation, performance measurement, and user-facing visualization of progress."
            ]
        },
        {
            "title": "FUNCTIONAL REQUIREMENTS",
            "table": [
                ["REQUIREMENT ID", "DESCRIPTION"],
                ["FR1", "The system shall allow user registration with full name, email, username, and password."],
                ["FR2", "The system shall authenticate users and issue JWT access tokens."],
                ["FR3", "The system shall generate a career roadmap from a selected role and duration."],
                ["FR4", "The system shall generate a day-wise learning plan from the chosen roadmap."],
                ["FR5", "The system shall allow users to mark daily plan items complete or incomplete."],
                ["FR6", "The system shall provide AI-generated topic explanations and resources."],
                ["FR7", "The system shall generate mock tests using completed topics only."],
                ["FR8", "The system shall store test attempts and compute analytics."],
            ],
            "table_title": "Table 2.1 Functional Requirements of the Proposed System"
        },
        {
            "title": "NON-FUNCTIONAL REQUIREMENTS",
            "table": [
                ["CATEGORY", "REQUIREMENT"],
                ["Security", "Passwords must be stored in hashed form and protected APIs must require tokens."],
                ["Performance", "The platform should return dashboard and history data with acceptable latency."],
                ["Reliability", "Stored plans, tests, and user records must remain consistent across sessions."],
                ["Usability", "Pages should present clear calls to action and readable progress indicators."],
                ["Maintainability", "Backend components should be separated into routers, models, schemas, and services."],
                ["Scalability", "The architecture should support adding new intelligence or assessment modules."],
                ["Portability", "Configuration must be environment-driven for local and hosted deployment."],
            ],
            "table_title": "Table 2.2 Non-Functional Requirements"
        },
        {
            "title": "USER CHARACTERISTICS AND CONSTRAINTS",
            "paragraphs": [
                "The primary users of the platform are students and aspiring developers preparing for roles such as Python Developer, Full Stack Developer, or similar technology-oriented careers. These users may have limited prior structure in their learning and therefore need visual guidance, incremental tasking, and confidence-building through measurable achievement.",
                "Constraints identified during analysis include dependence on a third-party AI service for generation quality, sensitivity of generated output to prompt formulation, the need for reliable internet connectivity during hosted usage, and time constraints associated with a student project schedule."
            ],
            "bullets": [
                "Users need simple onboarding and clear dashboard orientation.",
                "The system must manage evolving user requirements without breaking core flows.",
                "Assessment logic must remain aligned with user progress data stored in the database."
            ]
        },
        {
            "title": "SOFTWARE AND HARDWARE REQUIREMENTS",
            "table": [
                ["ITEM", "SPECIFICATION"],
                ["Operating System", "Windows 10 or above"],
                ["Backend Runtime", "Python 3.8+ with FastAPI and Uvicorn"],
                ["Frontend Runtime", "Node.js 18+ with Next.js and React"],
                ["Database", "PostgreSQL"],
                ["Libraries", "SQLAlchemy, Pydantic, Axios, Framer Motion, Lucide React"],
                ["Processor", "Modern multi-core processor"],
                ["Memory", "Minimum 8 GB RAM recommended"],
                ["Network", "Internet access for AI API and cloud deployment"],
            ],
            "table_title": "Table 2.3 Software and Hardware Requirements"
        },
        {
            "title": "CHAPTER 3: SYSTEM DESIGN",
            "paragraphs": [
                "System design for CareerPilot AI focuses on a layered full-stack architecture that is modular enough for academic development while still practical for deployment. The frontend is implemented as a route-based Next.js application, while the backend is implemented as a FastAPI service with database-backed domain entities and dedicated routers.",
                "The design philosophy followed in this project is to keep business responsibilities explicit, reduce tight coupling, and allow future features to be integrated with minimal changes to existing modules."
            ]
        },
        {
            "title": "SYSTEM ARCHITECTURE",
            "paragraphs": [
                "The architecture follows a client-server model. Users interact through browser-based interfaces built with React and Next.js. These interfaces call backend APIs through Axios, sending authentication tokens where required. The FastAPI backend validates the request, executes application logic, and persists results using SQLAlchemy models connected to PostgreSQL.",
                "AI-powered outputs are generated through a dedicated integration layer that communicates with the Groq API. This layer is isolated from presentation concerns so that prompt engineering and response normalization can evolve independently of the frontend."
            ]
        },
        {
            "title": "BACKEND AND FRONTEND MODULES",
            "table": [
                ["MODULE", "RESPONSIBILITY", "KEY IMPLEMENTATION AREA"],
                ["Authentication", "Registration, login, token validation", "backend/app/routers/auth.py"],
                ["AI Roadmap", "Roadmap, daily plan, topic teaching", "backend/app/routers/ai.py"],
                ["Mock Tests", "Test generation and submission", "backend/app/routers/mock_tests.py"],
                ["Performance", "Metrics, trends, daily quote", "backend/app/routers/performance.py"],
                ["Career Intelligence", "Readiness, DNA, coaching data", "backend/app/routers/career_intelligence.py"],
                ["Frontend Pages", "User interaction and visualization", "frontend/app/*/page.tsx"],
            ],
            "table_title": "Table 3.1 Core Backend and Frontend Modules"
        },
        {
            "title": "DATABASE DESIGN OVERVIEW",
            "paragraphs": [
                "The database is designed to preserve both core identity data and rapidly changing learning artifacts. The user_roles table is a central design choice because it allows one user to maintain role-based contexts over time. This role context then becomes the parent reference for generated roadmaps, daily plans, tests, and intelligence records.",
                "The schema balances normalized relational structure with practical JSON fields for variable outputs such as generated topics, score trends, strengths, recommendations, and learning plans."
            ]
        },
        {
            "title": "CORE DATABASE TABLES",
            "table": [
                ["TABLE", "PURPOSE", "KEY FIELDS"],
                ["users", "Stores user identity information", "id, email, username, password_hash, full_name"],
                ["user_roles", "Stores role context for each user", "id, user_id, role_name, duration_days"],
                ["roadmaps", "Stores generated role roadmaps", "id, user_role_id, roadmap_text, generated_at"],
                ["daily_plans", "Stores day-wise learning tasks", "id, user_role_id, day_number, topic, estimated_hours"],
                ["topic_progress", "Tracks daily completion status", "id, daily_plan_id, is_completed, completed_at"],
            ],
            "table_title": "Table 3.2 Core Database Tables"
        },
        {
            "title": "ASSESSMENT AND TESTING TABLES",
            "table": [
                ["TABLE", "PURPOSE", "KEY FIELDS"],
                ["mock_tests_v2", "Stores generated tests", "id, user_role_id, test_name, topics_used, status"],
                ["mock_test_questions", "Stores MCQ and coding questions", "id, test_id, question_type, topic, difficulty"],
                ["mock_test_attempts", "Stores attempt-level scoring", "id, test_id, total_score, weak_topics, strong_topics"],
                ["mock_test_section_scores", "Stores section summaries", "id, attempt_id, section_type, percentage"],
                ["coding_submissions", "Stores submitted code and verdicts", "id, question_id, code, status, passed_count"],
            ],
            "table_title": "Table 3.3 Assessment and Testing Tables"
        },
        {
            "title": "CAREER INTELLIGENCE TABLES",
            "table": [
                ["TABLE", "PURPOSE", "KEY FIELDS"],
                ["user_performance_metrics", "Stores trend and performance statistics", "average_score, best_score, score_trend"],
                ["career_dna_profiles", "Stores readiness dimensions", "logical_ability, consistency, overall_score"],
                ["skill_graphs", "Stores skill mastery details", "skill_name, mastery_level, trend, practice_count"],
                ["career_forecasts", "Stores readiness forecasts", "internship_readiness, placement_readiness, predicted_salary_range"],
                ["ai_coaching_sessions", "Stores weekly strategy outputs", "week_number, weekly_focus, study_plan"],
                ["learning_velocity", "Stores pace and retention metrics", "topics_per_week, daily_streak, velocity_score"],
            ],
            "table_title": "Table 3.4 Career Intelligence Tables"
        },
        {
            "title": "API DESIGN",
            "paragraphs": [
                "API design in CareerPilot AI follows route-level separation. Authentication endpoints handle registration, login, and current-user retrieval. AI endpoints generate roadmaps, daily plans, and topic explanations. Mock-test endpoints generate personalized tests and submit attempts. Performance endpoints summarize trends, while career intelligence endpoints expose DNA, skill, and forecast information.",
                "The advantage of this design is that frontend pages interact with clear resource-oriented endpoints instead of monolithic service calls. It also simplifies debugging and progressive extension."
            ]
        },
        {
            "title": "USER INTERFACE DESIGN",
            "paragraphs": [
                "User interface design emphasizes clarity, action visibility, and continuity between steps. The dashboard uses cards and metric summaries to orient the learner. The roadmap page blends generation and customization. The daily plan page uses expandable lists and progress bars. The learn page uses focused inputs. The mock-test page favors configuration and history, while analytics pages convert raw scores into understandable insight.",
                "A consistent sidebar navigation pattern is used after authentication so that users can move quickly between modules without losing context."
            ]
        },
        {
            "title": "PROCEDURAL DESIGN",
            "paragraphs": [
                "Procedural design for the platform revolves around a repeated pattern: accept user input, validate role and authorization, generate or retrieve structured data, persist it if needed, and return a response that the frontend can render directly. This pattern is visible in roadmap generation, daily plan generation, test generation, and score reporting.",
                "In the mock-test workflow specifically, the procedure verifies completed topics, requests suitable questions, stores the generated test, records attempts, and updates long-term performance metrics."
            ]
        },
        {
            "title": "CHAPTER 4: IMPLEMENTATION",
            "paragraphs": [
                "Implementation proceeded in stages that mirror the major modules of the system. Authentication and database foundation were established first. AI-assisted roadmap and daily-plan generation were then integrated. Afterwards, frontend pages were expanded to support role creation, progress tracking, and topic learning. Advanced assessment and analytics modules were added as later phases of the project.",
                "The implementation approach favored incremental feature completion with repeated testing after each integration milestone."
            ]
        },
        {
            "title": "CODING STANDARDS",
            "table": [
                ["STANDARD", "APPLICATION IN PROJECT"],
                ["Naming", "snake_case in Python and readable camelCase or descriptive identifiers in TypeScript"],
                ["Validation", "Pydantic schemas used for request and response validation"],
                ["Security", "Passwords hashed with bcrypt and APIs protected through JWT checks"],
                ["Separation of Concerns", "Routers, models, schemas, and services kept distinct"],
                ["Error Handling", "HTTPException and structured user-facing error messages"],
                ["Configuration", "Environment-based settings for keys, URLs, and deployment values"],
            ],
            "table_title": "Table 4.1 Coding Standards and Development Practices"
        },
        {
            "title": "BACKEND IMPLEMENTATION",
            "paragraphs": [
                "The backend implementation centers on FastAPI because of its concise route declaration model, validation support, and compatibility with asynchronous request handling. The application entry point in main.py registers routers for authentication, AI generation, mock tests, performance, career intelligence, and code execution. This structure gives each feature group a dedicated area for request handling and future maintenance.",
                "SQLAlchemy models represent persisted entities, while Alembic migrations track schema changes. Password hashing is performed before user creation, and JWT tokens are issued on successful login."
            ]
        },
        {
            "title": "FRONTEND IMPLEMENTATION",
            "paragraphs": [
                "The frontend implementation uses Next.js and React to create a clean route-driven experience. Every major system feature has a dedicated page under the app directory. Styling is achieved with Tailwind CSS and UI primitives, while Axios is used to call backend endpoints and transmit authorization tokens where required.",
                "The use of React context for authentication enables consistent access control across pages and helps preserve the user's logged-in session during navigation."
            ]
        },
        {
            "title": "DEPLOYMENT AND CONFIGURATION",
            "paragraphs": [
                "The project is structured for cloud deployment with the backend and frontend hosted separately. Backend deployment configuration is prepared for Render, and frontend deployment configuration is prepared for Vercel. This separation allows each side of the application to scale independently and use environment variables suited to its hosting platform.",
                "Critical values such as database connection strings, JWT secrets, model names, CORS origins, and public API base URLs are externalized so that the same codebase can run in development and production environments."
            ]
        },
    ])

    for screenshot in SCREENSHOTS:
        pages.append({"image": screenshot})

    pages.extend([
        {
            "title": "CHAPTER 5: TESTING",
            "paragraphs": [
                "Testing was performed to verify that each module of the platform behaves correctly in isolation and in end-to-end flows. Since CareerPilot AI combines authentication, generated content, stored progress, and performance feedback, testing had to cover both individual APIs and the continuity between modules.",
                "The chosen testing approach includes scenario-based validation, endpoint testing, and user-interface verification using representative workflows."
            ]
        },
        {
            "title": "AUTHENTICATION AND PROFILE TEST CASES",
            "table": [
                ["TEST CASE", "INPUT", "EXPECTED RESULT", "STATUS"],
                ["Register user", "Valid form data", "User record is created successfully", "Pass"],
                ["Register duplicate email", "Existing email", "Validation error is returned", "Pass"],
                ["Login user", "Valid username and password", "JWT token and user data are returned", "Pass"],
                ["Login invalid password", "Wrong password", "Unauthorized response is returned", "Pass"],
                ["Fetch profile", "Valid token", "Current user details are returned", "Pass"],
            ],
            "table_title": "Table 5.1 Authentication and Profile Test Cases"
        },
        {
            "title": "ROADMAP AND DAILY PLAN TEST CASES",
            "table": [
                ["TEST CASE", "INPUT", "EXPECTED RESULT", "STATUS"],
                ["Generate roadmap", "Role name and duration", "Structured roadmap is created and stored", "Pass"],
                ["Customize skills", "User-added skill input", "Custom skill is included before final generation", "Pass"],
                ["Generate daily plan", "Existing user role", "Day-wise plan is created", "Pass"],
                ["Toggle completion", "Plan day clicked", "Completion state changes and persists", "Pass"],
                ["View roadmap list", "Authenticated request", "Saved roadmaps are returned", "Pass"],
            ],
            "table_title": "Table 5.2 Roadmap and Daily Plan Test Cases"
        },
        {
            "title": "MOCK TEST AND ANALYTICS TEST CASES",
            "table": [
                ["TEST CASE", "INPUT", "EXPECTED RESULT", "STATUS"],
                ["Generate mock test", "Completed topics and question counts", "Relevant MCQ and coding questions are returned", "Pass"],
                ["Submit mock test", "Answers and code submissions", "Scores and feedback are stored", "Pass"],
                ["Run code", "Question id and source code", "Execution verdict and pass counts are produced", "Pass"],
                ["View performance", "Valid role id", "Trend and score summary are shown", "Pass"],
                ["View profile statistics", "Authenticated request", "Role and completion statistics are visible", "Pass"],
            ],
            "table_title": "Table 5.3 Mock Test and Analytics Test Cases"
        },
        {
            "title": "TEST REPORT SUMMARY",
            "table": [
                ["AREA", "OBSERVATION"],
                ["Authentication", "Registration and login flows operate correctly under valid and invalid credentials."],
                ["Planning", "Roadmap and daily-plan generation produce role-aligned outputs."],
                ["Assessment", "Question generation and submission tracking work as expected."],
                ["Analytics", "Summary metrics, trends, and weak/strong topic outputs are retrievable."],
                ["User Interface", "Navigation between authenticated pages remains consistent."],
            ],
            "table_title": "Table 5.4 Observed Test Report Summary"
        },
        {
            "title": "TESTING APPROACHES",
            "paragraphs": [
                "Unit-level checks are applicable to utility and schema components, while integration checks are essential for verifying chained workflows such as registration to dashboard access or roadmap generation to daily-plan tracking. Since this project has a significant user-interface component, manual flow testing also played an important role.",
                "The combined testing approach ensures that individual functions behave as expected and that the application remains coherent when the learner moves across multiple routes and modules."
            ],
            "bullets": [
                "Unit testing for validation and helper logic.",
                "Integration testing for router-to-database behavior.",
                "Manual end-to-end testing for user journeys and interface consistency."
            ]
        },
        {
            "title": "SECURITY, RELIABILITY, AND TESTING OBSERVATIONS",
            "paragraphs": [
                "The testing phase confirmed that JWT-protected routes remain inaccessible without proper authentication and that user-specific resources are tied to the active context. Password hashing, token-based route protection, and controlled role references contribute to the platform's baseline security posture.",
                "From a reliability perspective, the most important observation is that the application's value depends on continuity across modules. The system must not only generate content, but also preserve that content and relate it accurately to progress and test results. The implemented design supports this continuity through consistent identifiers and relational mappings."
            ]
        },
        {
            "title": "CHAPTER 6: CONCLUSION",
            "paragraphs": [
                "CareerPilot AI successfully demonstrates a full-stack platform that transforms career planning into an interactive and measurable workflow. The final implementation supports registration, authentication, roadmap generation, daily planning, topic learning, personalized assessments, performance analytics, and user profile management within one integrated environment.",
                "The project meets its original objective of creating a practical AI-assisted career preparation tool for learners who need structured progress and actionable feedback."
            ]
        },
        {
            "title": "DESIGN ISSUES, ADVANTAGES, AND LIMITATIONS",
            "table": [
                ["ADVANTAGES", "LIMITATIONS"],
                ["Unifies planning, learning, and testing within one product", "Quality of generated outputs depends on external AI responses"],
                ["Uses secure authentication and role-based personalization", "Internet connectivity is required for full hosted functionality"],
                ["Tracks progress using stored daily completion and test history", "Advanced proctoring remains limited in the current scope"],
                ["Provides data-driven performance visibility", "Forecast outputs are heuristic and can be improved with more historical data"],
            ],
            "table_title": "Table 6.1 Advantages and Limitations"
        },
        {
            "title": "FUTURE SCOPE OF THE PROJECT",
            "paragraphs": [
                "Several directions exist for future enhancement of CareerPilot AI. The recommendation engine can be expanded to support richer explanation of why certain roles, skills, or projects are suggested. Analytics can be improved with longitudinal trend analysis across larger datasets and with better visual interpretation of learning velocity.",
                "The platform can also be extended with mentor collaboration features, scheduled notifications, richer coding-language support, stronger anti-cheat instrumentation, and employer-oriented readiness reports. These additions would further strengthen the product as a serious career preparation environment."
            ]
        },
        {
            "title": "APPENDIX A: USER MANUAL",
            "paragraphs": [
                "To use the system, a learner first creates an account through the registration page and then signs in. After successful login, the learner opens the roadmap page, enters a target role and duration, optionally customizes skills, and generates a roadmap. The roadmap can then be converted into a daily plan, whose day-wise items can be marked complete from the daily-plan page.",
                "The learn page accepts any topic for AI-generated explanation. The mock-test page creates tests from completed topics, while the performance page summarizes outcomes. The profile page displays user information and cumulative statistics.",
                "For local development, the backend is started with FastAPI and the frontend is started with the Next.js development server after environment variables and database migration have been configured."
            ]
        },
        {
            "title": "REFERENCES",
            "paragraphs": [
                "[1] Roger S. Pressman, Software Engineering: A Practitioner's Approach. New York: McGraw-Hill Education, 2010.",
                "[2] FastAPI Documentation. Available: https://fastapi.tiangolo.com/.",
                "[3] Next.js Documentation. Available: https://nextjs.org/docs.",
                "[4] SQLAlchemy Documentation. Available: https://docs.sqlalchemy.org/.",
                "[5] PostgreSQL Documentation. Available: https://www.postgresql.org/docs/.",
                "[6] Pydantic Documentation. Available: https://docs.pydantic.dev/.",
                "[7] Axios Documentation. Available: https://axios-http.com/.",
                "[8] Framer Motion Documentation. Available: https://www.framer.com/motion/.",
                "[9] Render Documentation. Available: https://render.com/docs.",
                "[10] Vercel Documentation. Available: https://vercel.com/docs.",
                "[11] Groq API Documentation. Available: https://console.groq.com/docs.",
                "[12] JSON Web Token Introduction. Available: https://jwt.io/introduction/."
            ]
        },
    ])

    if len(pages) != 60:
        raise ValueError(f"Expected 60 pages, found {len(pages)}")
    return pages


def render_document():
    missing = [str(item["path"]) for item in SCREENSHOTS if not item["path"].exists()]
    if missing:
        raise FileNotFoundError("Missing screenshot files:\n" + "\n".join(missing))

    doc = Document()
    configure_document(doc)
    pages = build_pages()

    for idx, spec in enumerate(pages, start=1):
        if spec.get("centered"):
            add_title(doc, spec["title"])
            for paragraph in spec.get("paragraphs", []):
                add_body(doc, paragraph, align=WD_ALIGN_PARAGRAPH.CENTER)
        elif "image" in spec:
            add_image_page(doc, spec["image"])
        elif "table" in spec and not spec.get("paragraphs") and not spec.get("bullets"):
            add_title(doc, spec["title"])
            add_table(doc, spec["table"], title=spec.get("table_title"), font_size=10)
        else:
            add_standard_page(
                doc,
                spec["title"],
                paragraphs=spec.get("paragraphs"),
                bullets=spec.get("bullets"),
                table=spec.get("table"),
                table_title=spec.get("table_title"),
            )
        page_break(doc, idx, len(pages))

    doc.save(OUTPUT)


if __name__ == "__main__":
    render_document()
    print(f"Generated report: {OUTPUT}")