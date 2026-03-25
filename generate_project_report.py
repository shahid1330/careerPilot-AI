from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


ROOT = Path(r"e:\Christ University\Trimester 6\Project")
ASSETS = ROOT / "report_assets"
OUTPUT = ROOT / "CareerPilot_AI_Project_Report_30_Pages_No_Images.docx"


def set_margins(section):
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)


def remove_header_footer(section):
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False
    for p in section.header.paragraphs:
        p.text = ""
    for p in section.footer.paragraphs:
        p.text = ""


def clear_header_footer_content(section):
    hdr = section.header._element
    ftr = section.footer._element
    for child in list(hdr):
        hdr.remove(child)
    for child in list(ftr):
        ftr.remove(child)


def apply_default_style(doc):
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    style.font.size = Pt(12)


def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    if level == 1:
        run.font.size = Pt(16)
        run.bold = True
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        run.font.size = Pt(12)
        run.bold = True
    run.font.name = "Times New Roman"
    return p


def add_body(doc, text):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.line_spacing = 1.5


def create_assets():
    ASSETS.mkdir(exist_ok=True)

    plt.style.use("default")

    # Figure 1: System architecture diagram
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    blocks = [
        (0.8, 6.5, 2.4, 2.0, "Users", "#F4A261"),
        (3.8, 6.5, 2.4, 2.0, "Next.js Frontend", "#2A9D8F"),
        (6.8, 6.5, 2.4, 2.0, "FastAPI Backend", "#E76F51"),
        (6.8, 3.6, 2.4, 2.0, "PostgreSQL", "#457B9D"),
        (3.8, 3.6, 2.4, 2.0, "Groq LLM API", "#A8DADC"),
    ]
    for x, y, w, h, label, color in blocks:
        rect = plt.Rectangle((x, y), w, h, color=color, alpha=0.9, ec="black", lw=1.5)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=11, weight="bold")
    arrows = [((3.2, 7.5), (3.8, 7.5)), ((6.2, 7.5), (6.8, 7.5)), ((8.0, 6.5), (8.0, 5.6)), ((6.2, 4.6), (6.8, 4.6))]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", color="black", lw=2))
    ax.set_title("CareerPilot AI Architecture", fontsize=16, weight="bold", color="#1D3557")
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_1_architecture.png", dpi=220)
    plt.close(fig)

    # Figure 2: Data flow diagram
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")
    entities = [
        (0.8, 5.5, "Student"),
        (3.8, 6.2, "Auth Service"),
        (6.5, 6.2, "AI Service"),
        (9.2, 6.2, "Roadmap Engine"),
        (6.5, 3.2, "Mock Test Engine"),
        (9.2, 3.2, "Career Intelligence"),
    ]
    colors = ["#FFB703", "#219EBC", "#8ECAE6", "#023047", "#FB8500", "#8338EC"]
    for (x, y, label), c in zip(entities, colors):
        ax.add_patch(plt.Circle((x, y), 0.9, color=c, alpha=0.85))
        ax.text(x, y, label, ha="center", va="center", fontsize=9, color="white", weight="bold")
    flows = [
        ((1.7, 5.8), (3.0, 6.0), "Login/Register"),
        ((4.7, 6.2), (5.6, 6.2), "JWT"),
        ((7.4, 6.2), (8.3, 6.2), "Roadmap JSON"),
        ((7.4, 5.4), (6.8, 4.1), "Topics"),
        ((7.4, 3.2), (8.3, 3.2), "Scores"),
    ]
    for s, e, t in flows:
        ax.annotate("", xy=e, xytext=s, arrowprops=dict(arrowstyle="->", lw=2, color="#222"))
        ax.text((s[0] + e[0]) / 2, (s[1] + e[1]) / 2 + 0.25, t, fontsize=8, ha="center")
    ax.set_title("High-Level Data Flow", fontsize=16, weight="bold", color="#1D3557")
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_2_dataflow.png", dpi=220)
    plt.close(fig)

    # Figure 3: ER overview
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)

    def table_box(x, y, title, rows, color):
        w, h = 3.2, 0.6 * (len(rows) + 1)
        ax.add_patch(plt.Rectangle((x, y), w, h, ec="black", fc=color, alpha=0.85))
        ax.text(x + 1.6, y + h - 0.35, title, ha="center", va="center", fontsize=10, weight="bold")
        for i, r in enumerate(rows):
            ax.text(x + 0.2, y + h - 0.85 - i * 0.55, r, fontsize=8)

    table_box(0.7, 5.5, "USERS", ["id (PK)", "email", "username"], "#E63946")
    table_box(4.4, 5.5, "USER_ROLES", ["id (PK)", "user_id (FK)", "role_name"], "#457B9D")
    table_box(8.1, 5.5, "ROADMAPS", ["id (PK)", "user_role_id (FK)", "roadmap_text"], "#2A9D8F")
    table_box(0.7, 1.4, "DAILY_PLANS", ["id (PK)", "user_role_id (FK)", "day_number"], "#FFB703")
    table_box(4.4, 1.4, "MOCK_TESTS_V2", ["id (PK)", "user_role_id (FK)", "mcq_count"], "#8338EC")
    table_box(8.1, 1.4, "CAREER_DNA", ["id (PK)", "user_role_id (FK)", "overall_score"], "#06D6A0")

    for sx, sy, ex, ey in [(3.9, 6.7, 4.4, 6.7), (7.6, 6.7, 8.1, 6.7), (6.0, 5.5, 6.0, 3.5), (2.3, 5.5, 2.3, 3.5), (9.7, 5.5, 9.7, 3.5)]:
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy), arrowprops=dict(arrowstyle="->", lw=1.8))

    ax.set_title("Core Database Entities and Relationships", fontsize=16, weight="bold", color="#1D3557")
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_3_er.png", dpi=220)
    plt.close(fig)

    # Figure 4: Mock-test sequence
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    lanes = ["User", "Frontend", "Backend", "AI Service", "DB"]
    xs = [0.8, 2.8, 4.8, 6.8, 8.8]
    for x, name in zip(xs, lanes):
        ax.plot([x, x], [0.8, 5.5], linestyle="--", color="#666")
        ax.text(x, 5.8, name, ha="center", fontsize=10, weight="bold")
    steps = [
        (0, 1, 5.0, "Select MCQ/Coding"),
        (1, 2, 4.5, "POST /mock-tests/generate"),
        (2, 4, 4.0, "Fetch completed topics"),
        (2, 3, 3.5, "Generate fresh questions"),
        (3, 2, 3.0, "Return MCQ + Coding"),
        (2, 4, 2.5, "Persist test and questions"),
        (2, 1, 2.0, "Respond test_id"),
        (1, 0, 1.5, "Launch test page"),
    ]
    for s, e, y, text in steps:
        ax.annotate("", xy=(xs[e], y), xytext=(xs[s], y), arrowprops=dict(arrowstyle="->", lw=2, color="#264653"))
        ax.text((xs[s] + xs[e]) / 2, y + 0.08, text, fontsize=8, ha="center")
    ax.set_title("Mock Test Generation Sequence", fontsize=16, weight="bold", color="#1D3557")
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_4_sequence.png", dpi=220)
    plt.close(fig)

    # Figure 5: Score trend sample
    fig, ax = plt.subplots(figsize=(10, 5.5))
    tests = np.arange(1, 11)
    scores = np.array([52, 58, 61, 63, 67, 70, 72, 75, 78, 82])
    ax.plot(tests, scores, marker="o", color="#2A9D8F", linewidth=3)
    ax.fill_between(tests, scores, 40, color="#2A9D8F", alpha=0.18)
    ax.set_facecolor("#F1FAEE")
    ax.grid(alpha=0.3)
    ax.set_xlabel("Mock Test Number")
    ax.set_ylabel("Total Score (%)")
    ax.set_title("Performance Trend Across Tests", fontsize=16, weight="bold", color="#1D3557")
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_5_trend.png", dpi=220)
    plt.close(fig)

    # Figure 6: Radar chart
    labels = np.array(["Logic", "Problem Solving", "Speed", "Consistency", "Learning Efficiency"])
    values = np.array([0.76, 0.72, 0.64, 0.81, 0.74])
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    values = np.append(values, values[0])
    angles = np.append(angles, angles[0])

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, color="#E76F51", linewidth=3)
    ax.fill(angles, values, color="#E76F51", alpha=0.3)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_ylim(0, 1)
    ax.set_title("Career DNA Sample Profile", fontsize=15, weight="bold", pad=20)
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_6_radar.png", dpi=220)
    plt.close(fig)

    # Figure 7: Deployment pipeline
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axis("off")
    nodes = [
        (0.8, 2.5, "Developer Push", "#264653"),
        (2.8, 2.5, "GitHub Repo", "#2A9D8F"),
        (4.8, 3.3, "Render (Backend)", "#E9C46A"),
        (4.8, 1.7, "Vercel (Frontend)", "#F4A261"),
        (7.2, 2.5, "Live Application", "#E76F51"),
    ]
    for x, y, txt, c in nodes:
        ax.add_patch(FancyBboxPatch((x, y), 1.6, 0.8, boxstyle="round,pad=0.1", fc=c, ec="black", alpha=0.95))
        ax.text(x + 0.8, y + 0.4, txt, ha="center", va="center", fontsize=9, weight="bold", color="white")
    edges = [((2.4, 2.9), (2.8, 2.9)), ((4.4, 2.9), (4.8, 3.5)), ((4.4, 2.9), (4.8, 2.1)), ((6.4, 3.5), (7.2, 2.9)), ((6.4, 2.1), (7.2, 2.9))]
    for s, e in edges:
        ax.annotate("", xy=e, xytext=s, arrowprops=dict(arrowstyle="->", lw=2))
    ax.set_title("Cloud Deployment Pipeline", fontsize=16, weight="bold", color="#1D3557")
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_7_deployment.png", dpi=220)
    plt.close(fig)

    # Figure 8: Gantt chart
    fig, ax = plt.subplots(figsize=(10, 5.5))
    tasks = ["Phase 2 Backend", "Phase 3 AI", "Phase 4 Frontend", "Phase 6A Testing", "Phase 6B Intelligence"]
    starts = [1, 5, 9, 13, 17]
    durations = [4, 4, 4, 4, 4]
    colors = ["#457B9D", "#1D3557", "#2A9D8F", "#E9C46A", "#E76F51"]
    for i, (task, start, duration, color) in enumerate(zip(tasks, starts, durations, colors)):
        ax.barh(task, duration, left=start, color=color, alpha=0.85)
    ax.set_xlabel("Project Weeks")
    ax.set_title("Implementation Timeline (Illustrative)", fontsize=16, weight="bold", color="#1D3557")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_8_gantt.png", dpi=220)
    plt.close(fig)

    # Figure 9: Testing status chart
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    categories = ["Auth APIs", "Roadmap APIs", "Mock Test APIs", "Code Execution", "UI Flows"]
    passed = np.array([9, 8, 10, 7, 8])
    total = np.array([10, 10, 12, 9, 10])
    ax.bar(categories, total, color="#D9D9D9", label="Total")
    ax.bar(categories, passed, color="#2A9D8F", label="Passed")
    ax.set_ylabel("Test Cases")
    ax.set_title("Representative Test Coverage Snapshot", fontsize=16, weight="bold", color="#1D3557")
    ax.legend()
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(ASSETS / "fig_9_testing.png", dpi=220)
    plt.close(fig)



def add_figure(doc, filename, caption):
    # Images intentionally disabled as per latest report request.
    return


def add_table_caption(doc, caption):
    p = doc.add_paragraph(caption)
    p.runs[0].font.size = Pt(10)
    p.runs[0].bold = True


def write_page(doc, title, paragraphs=None, bullets=None, figure=None, table_data=None, table_caption=None):
    add_heading(doc, title, level=1)
    if paragraphs:
        for para in paragraphs:
            add_body(doc, para)
    if bullets:
        for b in bullets:
            add_bullet(doc, b)
    if table_data is not None:
        if table_caption:
            add_table_caption(doc, table_caption)
        rows = len(table_data)
        cols = len(table_data[0]) if rows > 0 else 0
        table = doc.add_table(rows=rows, cols=cols)
        table.style = "Table Grid"
        for r in range(rows):
            for c in range(cols):
                table.cell(r, c).text = str(table_data[r][c])
                for run in table.cell(r, c).paragraphs[0].runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(11)
    if figure:
        add_figure(doc, figure[0], figure[1])


def add_page_break_if_needed(doc, current_page, total_pages):
    if current_page < total_pages:
        doc.add_page_break()


def build_report():
    create_assets()

    doc = Document()
    apply_default_style(doc)

    for sec in doc.sections:
        set_margins(sec)
        remove_header_footer(sec)
        clear_header_footer_content(sec)

    pages = []

    pages.append((
        "CAREERPILOT AI: AN AI-POWERED CAREER ROADMAP, LEARNING, AND EVALUATION PLATFORM",
        [
            "Project Report submitted in partial fulfillment of the requirements for the final year project.",
            "Department of Computer Science, CHRIST (Deemed to be University)",
            "Academic Year: 2025-2026",
            "Submitted by: Shahid and Team",
            "Guide: ____________________",
            "Date: March 2026"
        ],
        None,
        None,
        None,
        None
    ))

    pages.append((
        "CERTIFICATE",
        [
            "This is to certify that the project titled CareerPilot AI has been carried out by the undersigned students under the supervision of the project guide and submitted to the Department of Computer Science, CHRIST (Deemed to be University), in partial fulfillment of the requirements for award of degree.",
            "The work embodied in this report is original and has not been submitted to any other University or Institution for the award of any degree or diploma."
        ],
        ["Guide Signature: ____________________", "Head of Department Signature: ____________________", "Date: ____________________"],
        None,
        None,
        None
    ))

    pages.append((
        "ACKNOWLEDGMENTS",
        [
            "The development of CareerPilot AI has been a collaborative effort made possible by constant support from faculty, peers, and family. We thank our project guide for continuous mentorship in requirements clarification, architecture refinement, and implementation review. We also acknowledge the Department of Computer Science for providing the academic environment, infrastructure, and process discipline required to complete a full-stack AI product.",
            "Special thanks are due to classmates and testers who participated in iterative review sessions and helped validate user journeys such as roadmap generation, daily plan tracking, mock-test workflows, and performance analytics. Their feedback was crucial for improving usability, reliability, and consistency of system behavior.",
            "Finally, we thank our family members for encouragement and support throughout the project timeline."
        ],
        None,
        None,
        None,
        None
    ))

    pages.append((
        "ABSTRACT",
        [
            "CareerPilot AI is a full-stack intelligent learning platform that transforms career aspirations into structured plans, measurable practice, and feedback-driven improvement. The system combines a FastAPI backend, PostgreSQL database, and Next.js frontend to deliver secure authentication, AI-generated career roadmaps, daily learning plans, smart mock tests, coding evaluation, and career intelligence analytics. A JWT-based authorization workflow protects all user-specific operations, while modular API design allows independent scaling of roadmap, testing, and analytics services.",
            "The platform addresses limitations of static learning portals by making preparation adaptive and evidence-based. Users define a target role, obtain role-specific learning pathways, complete daily milestones, and then receive assessments generated only from completed topics. The evaluation engine supports MCQ and coding sections, tracks section-level performance, and computes historical trends. Additional intelligence modules estimate readiness for internships and placements through profile dimensions such as logical ability, consistency, and learning velocity.",
            "The implemented system demonstrates an end-to-end educational technology workflow with practical deployment readiness and extensibility for future mentoring and recommendation features."
        ],
        None,
        None,
        None,
        None
    ))

    # Page 5: TOC
    toc_paras = [
        "1. Introduction .......................................................................................... 9",
        "2. System Analysis and Requirements ......................................................... 12",
        "3. System Design ..................................................................................... 16",
        "4. Implementation .................................................................................... 21",
        "5. Testing ............................................................................................... 26",
        "6. Conclusion ........................................................................................... 29",
        "Appendices ............................................................................................ 30",
        "References ............................................................................................ 30"
    ]
    pages.append(("TABLE OF CONTENTS", toc_paras, None, None, None, None))

    # Page 6: List of Tables
    list_tables = [
        ["Table No.", "Title", "Page No."],
        ["Table 1.1", "Software and Hardware Requirements", "14"],
        ["Table 2.1", "Module-Wise Functional Mapping", "17"],
        ["Table 3.1", "Database Table Summary", "19"],
        ["Table 4.1", "Implementation Standards", "22"],
        ["Table 5.1", "Representative Test Cases", "26"],
        ["Table 6.1", "Advantages and Limitations", "29"],
    ]
    pages.append(("LIST OF TABLES", ["The following tables are used in this report."], None, None, list_tables, None))

    # Page 7: List of Figures
    list_figs = [
        ["Fig. No.", "Figure Name", "Page No."],
        ["Fig 1.1", "CareerPilot AI Architecture", "10"],
        ["Fig 2.1", "High-Level Data Flow", "13"],
        ["Fig 3.1", "Core Database ER Overview", "18"],
        ["Fig 4.1", "Mock Test Generation Sequence", "23"],
        ["Fig 5.1", "Performance Trend Across Tests", "27"],
        ["Fig 6.1", "Career DNA Sample Profile", "28"],
        ["Fig 7.1", "Cloud Deployment Pipeline", "25"],
    ]
    pages.append(("LIST OF FIGURES", ["The following figures are used in this report."], None, None, list_figs, None))

    # Page 8: Abbreviations
    pages.append((
        "LIST OF ABBREVIATIONS",
        [
            "AI  : Artificial Intelligence",
            "API : Application Programming Interface",
            "JWT : JSON Web Token",
            "ORM : Object Relational Mapper",
            "LLM : Large Language Model",
            "UI  : User Interface",
            "ER  : Entity Relationship",
            "DFD : Data Flow Diagram",
            "SQL : Structured Query Language",
            "KPI : Key Performance Indicator",
        ],
        None,
        None,
        None,
        None
    ))

    # Page 9-11 Chapter 1
    pages.append((
        "CHAPTER 1: INTRODUCTION",
        [
            "This chapter introduces the problem context, goals, and scope of CareerPilot AI.",
            "Digital learners often face fragmented resources, unclear progression plans, and weak feedback loops. Existing portals typically provide content but do not continuously align learning activity with career outcomes. CareerPilot AI addresses this challenge by combining planning, guided execution, assessment, and analytics in one platform.",
            "The project is positioned as a practical career preparation assistant for students targeting software roles. It integrates roadmap generation, daily plans, and adaptive assessment while maintaining secure account-level personalization."
        ],
        [
            "Project Description: AI-assisted career planning with structured execution and test-driven progress measurement.",
            "Existing System Limitation: Static courses lack personalization and closed-loop evaluation.",
            "Objective: Improve user readiness for internships and placements through measurable learning cycles.",
            "Purpose: Provide a single platform for planning, learning, testing, and performance insight.",
            "Scope: Role-based roadmap generation, topic-level completion tracking, mock tests, and intelligence dashboards.",
            "Applicability: Useful for students, self-learners, placement training groups, and mentors."
        ],
        ("fig_1_architecture.png", "Fig 1.1 CareerPilot AI Architecture"),
        None,
        None
    ))

    pages.append((
        "CHAPTER 1: OVERVIEW OF THE REPORT",
        [
            "The report is organized to mirror the software engineering lifecycle adopted for CareerPilot AI. Chapter 2 captures system analysis and requirements, including user characteristics, constraints, and conceptual models. Chapter 3 describes architecture, module decomposition, interface design, and database mapping. Chapter 4 summarizes implementation approaches and coding standards, followed by chapter 5 that documents testing strategies and sample test reports. Chapter 6 provides conclusion, limitations, and future scope.",
            "Appendices contain additional planning artifacts and supportive content, while references follow the required citation style."
        ],
        None,
        None,
        None,
        None
    ))

    pages.append((
        "CHAPTER 1: EXISTING SYSTEM AND OBJECTIVES",
        [
            "Existing systems relevant to career preparation include static MOOC catalogs, video-based learning channels, standalone coding platforms, and unintegrated test portals. These systems solve isolated subproblems but rarely offer continuity from aspiration to outcome.",
            "CareerPilot AI objective statement: Build an end-to-end, secure, AI-enabled system that converts a user-selected role into daily learning tasks, evaluates progress using personalized assessments, and provides actionable readiness insights within a single workflow.",
            "The expected contribution is improvement in engagement, consistency, and measurable performance progression."
        ],
        None,
        None,
        None,
        None
    ))

    # Chapter 2 pages 12-15
    pages.append((
        "CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENTS",
        [
            "This chapter formalizes problem definition, requirements specification, and constraints.",
            "Problem Definition: learners need a guided and measurable path to move from beginner to role-ready candidate. The core gap is absence of unified planning and feedback mechanisms.",
            "Requirements are identified as functional, non-functional, and operational. Functional requirements include registration, authentication, roadmap generation, daily plan generation, test creation, submission evaluation, and analytics retrieval. Non-functional requirements include data integrity, secure access control, acceptable response time, and maintainable code organization."
        ],
        None,
        None,
        None,
        None
    ))

    pages.append((
        "CHAPTER 2: BLOCK DIAGRAM AND DATA FLOW",
        [
            "The system receives user input from frontend interfaces, validates identity through JWT, generates AI-assisted artifacts, persists data into PostgreSQL, and returns structured responses. Generated outputs include roadmaps, plans, mock tests, and coaching insights.",
            "The data flow model captures interactions among frontend, backend router layer, service layer, AI gateway, and persistence layer."
        ],
        None,
        ("fig_2_dataflow.png", "Fig 2.1 High-Level Data Flow"),
        None,
        None
    ))

    req_table = [
        ["Category", "Specification"],
        ["OS", "Windows 10/11 or Linux"],
        ["Backend Runtime", "Python 3.11, FastAPI, Uvicorn"],
        ["Frontend Runtime", "Node.js 18+, Next.js 16"],
        ["Database", "PostgreSQL with SQLAlchemy ORM"],
        ["Security", "JWT authentication, bcrypt hashing"],
        ["AI Integration", "Groq LLM API through service layer"],
        ["Hardware (Recommended)", "8 GB RAM, modern multi-core CPU"],
    ]
    pages.append((
        "CHAPTER 2: SYSTEM REQUIREMENTS",
        [
            "User Characteristics include students preparing for interviews, beginners seeking structured learning, and users requiring analytics feedback after assessments.",
            "The requirements matrix below summarizes software and hardware baseline assumptions for deployment and development."
        ],
        None,
        None,
        req_table,
        "Table 1.1 Software and Hardware Requirements"
    ))

    pages.append((
        "CHAPTER 2: CONSTRAINTS AND CONCEPTUAL MODELS",
        [
            "Primary constraints include dependency on external LLM API availability, internet access for hosted deployment, and role-topic quality sensitivity in generated outputs. Additional constraints arise from time-bound student project schedules and evolving frontend requirements.",
            "Conceptual modeling in this project combines ER relationships for storage design and sequence/data-flow models for runtime interaction analysis."
        ],
        [
            "Constraint 1: LLM response variability requires schema validation and fallback handling.",
            "Constraint 2: User progress tracking depends on reliable client state synchronization.",
            "Constraint 3: Execution sandboxing for code evaluation must control runtime and errors."
        ],
        None,
        None,
        None
    ))

    # Chapter 3 pages 16-20
    pages.append((
        "CHAPTER 3: SYSTEM DESIGN",
        [
            "This chapter presents architecture, module design, database strategy, and interface planning.",
            "Architecture follows a client-server pattern where Next.js handles presentation and interaction, FastAPI provides business logic, and PostgreSQL supports transactional data storage. API routers are segmented by domain: auth, AI, mock tests, performance, and career intelligence.",
            "The design emphasizes modularity to permit independent evolution of testing and analytics services."
        ],
        None,
        None,
        None,
        None
    ))

    module_table = [
        ["Module", "Core Responsibility", "Key Files"],
        ["Authentication", "Register, login, token validation", "app/routers/auth.py"],
        ["AI Roadmap", "Roadmap and daily plan generation", "app/routers/ai.py"],
        ["Mock Tests", "Question generation and attempts", "app/routers/mock_tests.py"],
        ["Code Execution", "Run coding answers against test cases", "app/routers/code_execution.py"],
        ["Performance", "Score trends and quote service", "app/routers/performance.py"],
        ["Career Intelligence", "DNA, forecasts, coaching", "app/routers/career_intelligence.py"],
    ]
    pages.append((
        "CHAPTER 3: MODULE DESIGN",
        [
            "The platform decomposes into cohesive modules with clearly defined interfaces. This supports easier testing, maintainability, and progressive enhancement.",
            "The module mapping table shows responsibilities and implementation anchors."
        ],
        None,
        None,
        module_table,
        "Table 2.1 Module-Wise Functional Mapping"
    ))

    pages.append((
        "CHAPTER 3: DATABASE DESIGN",
        [
            "Database design includes core user-role mapping, planning entities, test entities, and intelligence entities. The user_roles table acts as a central role context key referenced by roadmaps, plans, and performance modules.",
            "JSON columns are intentionally used for dynamic fields such as topics_used, score_trend, and recommendations to support rapid prototyping while preserving relational integrity for primary entities."
        ],
        None,
        ("fig_3_er.png", "Fig 3.1 Core Database ER Overview"),
        None,
        None
    ))

    db_table = [
        ["Table", "Purpose", "Key Relationship"],
        ["users", "Identity records", "1-to-many with user_roles"],
        ["user_roles", "Career role context", "Parent for roadmaps and tests"],
        ["roadmaps", "Generated role roadmaps", "FK to user_roles"],
        ["daily_plans", "Day-wise learning tasks", "FK to user_roles"],
        ["mock_tests_v2", "Test instances", "FK to user_roles"],
        ["mock_test_questions", "MCQ/coding question bank", "FK to mock_tests_v2"],
        ["career_dna_profiles", "Career intelligence profile", "FK to user_roles"],
    ]
    pages.append((
        "CHAPTER 3: TABLES, RELATIONSHIPS, AND CONSTRAINTS",
        [
            "Relational constraints use cascading deletes for role-scoped artifacts, ensuring consistency when parent contexts are removed. Unique constraints are applied where profile entities map one-to-one with a role context.",
            "The summary below captures the principal persistence entities."
        ],
        None,
        None,
        db_table,
        "Table 3.1 Database Table Summary"
    ))

    pages.append((
        "CHAPTER 3: INTERFACE AND PROCEDURAL DESIGN",
        [
            "Interface design in frontend pages focuses on clear visual hierarchy, action-oriented cards, progress badges, and route-centric task flows. The dashboard acts as a control center linking roadmap creation, daily plans, tests, and analytics.",
            "Procedural design for mock tests follows a strict path: verify user role, gather completed topics, generate non-repetitive questions, persist test entities, and launch timed test UI. This sequence reduces randomization errors and preserves relevance to learned content."
        ],
        None,
        ("fig_4_sequence.png", "Fig 4.1 Mock Test Generation Sequence"),
        None,
        None
    ))

    # Chapter 4 pages 21-25
    pages.append((
        "CHAPTER 4: IMPLEMENTATION",
        [
            "Implementation was carried out incrementally using phase-wise milestones. Backend foundation established API contracts and database migration capability. AI endpoints and frontend pages were then integrated, followed by advanced assessment and analytics modules.",
            "Source organization follows domain-driven separation: models, schemas, routers, services, and utilities. Frontend follows Next.js App Router conventions with route folders and reusable UI components."
        ],
        None,
        None,
        None,
        None
    ))

    coding_table = [
        ["Standard", "Applied Practice"],
        ["Naming", "Descriptive snake_case in Python, camelCase in TypeScript"],
        ["Validation", "Pydantic schema validation for request and response models"],
        ["Security", "Hashed passwords, JWT bearer token checks"],
        ["Error Handling", "HTTPException with status-specific feedback"],
        ["Structure", "Router-service-model separation of concerns"],
    ]
    pages.append((
        "CHAPTER 4: IMPLEMENTATION APPROACHES AND CODING STANDARDS",
        [
            "Implementation approach combines top-down module planning with iterative integration testing. Critical user journeys were prioritized: authentication, roadmap generation, and mock test lifecycle.",
            "Coding standards adopted in this project are summarized below."
        ],
        None,
        None,
        coding_table,
        "Table 4.1 Implementation Standards"
    ))

    pages.append((
        "CHAPTER 4: API IMPLEMENTATION DETAILS",
        [
            "Backend entry point includes routers for auth, AI, mock tests, performance, career intelligence, and code execution. Each router encapsulates endpoint definitions and delegates logic to services where appropriate.",
            "Authentication uses OAuth2 password flow and JWT issuance. AI router supports roadmap generation, daily-plan generation, and topic teaching. Mock-test router enforces completed-topic-only test generation. Performance router computes score trends. Career intelligence router computes DNA, skills, forecast, coaching, and velocity responses."
        ],
        [
            "Key backend files: main.py, app/routers/auth.py, app/routers/ai.py",
            "Assessment files: app/routers/mock_tests.py, app/routers/code_execution.py",
            "Analytics files: app/routers/performance.py, app/routers/career_intelligence.py"
        ],
        None,
        None,
        None
    ))

    pages.append((
        "CHAPTER 4: FRONTEND IMPLEMENTATION DETAILS",
        [
            "The frontend uses Next.js with TypeScript for type-safe page development. Route-driven pages include register, login, dashboard, roadmap, daily-plan, mock-test, performance, and career-intelligence.",
            "AuthContext manages session state and redirects. API client wrapper centralizes base URL and authorization interceptors. UI employs cards, gradients, badges, and chart components to present metrics and actionable insights.",
            "Mock-test page includes configurable MCQ/coding counts and dynamic duration logic. Performance page displays trend charts and strong/weak area summaries."
        ],
        None,
        None,
        None,
        None
    ))

    pages.append((
        "CHAPTER 4: DEPLOYMENT DESIGN",
        [
            "Deployment design separates backend and frontend services for independent build and release pipelines. Backend is configured for Render using uvicorn start command, while frontend is configured for Vercel builds.",
            "Environment-driven configuration controls database URL, CORS origins, JWT settings, and AI API keys. This model supports both local development and cloud deployment with minimal code changes."
        ],
        None,
        ("fig_7_deployment.png", "Fig 7.1 Cloud Deployment Pipeline"),
        None,
        None
    ))

    # Chapter 5 pages 26-28
    test_table = [
        ["Test Scenario", "Input", "Expected Output", "Observed"],
        ["Register user", "Valid email/username/password", "201 Created user", "Pass"],
        ["Login user", "Correct credentials", "JWT token + user details", "Pass"],
        ["Generate roadmap", "role_name + duration", "Roadmap JSON stored", "Pass"],
        ["Generate test", "completed_day_numbers", "Personalized questions", "Pass"],
        ["Execute code", "question_id + code", "Case-wise result list", "Pass"],
        ["Performance summary", "user_role_id", "Trend and strengths", "Pass"],
    ]
    pages.append((
        "CHAPTER 5: TESTING",
        [
            "Testing strategy includes unit-level validation of endpoint behaviors and integration-level validation of full user flows. Manual exploratory tests were also performed for frontend interactions and error handling.",
            "Representative test scenarios are listed below."
        ],
        None,
        None,
        test_table,
        "Table 5.1 Representative Test Cases"
    ))

    pages.append((
        "CHAPTER 5: TESTING APPROACHES AND REPORTS",
        [
            "Unit testing validates discrete operations such as token generation, role ownership checks, and schema conversions. Integration testing validates chained operations including registration to dashboard progression and roadmap to test lifecycle.",
            "Test report evidence from scripts indicates successful health checks, auth workflows, and protected endpoint access under correct token contexts."
        ],
        [
            "Approach 1: Unit testing for utility and schema-level checks.",
            "Approach 2: Integration testing for API-to-database behavior.",
            "Approach 3: End-to-end manual flow validation from frontend routes."
        ],
        ("fig_9_testing.png", "Fig 5.1 Representative Test Coverage Snapshot"),
        None,
        None
    ))

    pages.append((
        "CHAPTER 5: PERFORMANCE ANALYSIS SNAPSHOT",
        [
            "Performance monitoring includes total tests, average score, best/worst score, and trend movement across attempts. Section-level diagnostics identify strong and weak topics, enabling targeted improvement plans.",
            "The sample charts below illustrate trend progression and multidimensional intelligence profiling used by the system."
        ],
        None,
        ("fig_5_trend.png", "Fig 5.2 Performance Trend Across Tests"),
        None,
        None
    ))

    # Chapter 6 pages 29
    adv_lim_table = [
        ["Advantages", "Limitations"],
        ["Unified planning-learning-testing workflow", "Dependent on external AI service quality"],
        ["Secure JWT-based personalization", "Requires stable internet for hosted mode"],
        ["Topic-based adaptive mock tests", "Advanced proctoring not fully implemented"],
        ["Rich analytics and career forecasting", "Some outputs remain heuristic in student version"],
    ]
    pages.append((
        "CHAPTER 6: CONCLUSION",
        [
            "CareerPilot AI fulfills its objective of delivering a structured and measurable career preparation platform. The project demonstrates complete full-stack integration from authentication and roadmap generation to testing, code execution, and intelligence analytics.",
            "Design and implementation issues addressed include modular decomposition, schema consistency, and integration sequencing across rapidly evolving requirements. The final platform is practical for student use and capable of incremental enhancement.",
            "Future scope includes richer recommendation explainability, stronger anti-cheat instrumentation, mentor collaboration modules, and longitudinal readiness prediction using larger historical datasets."
        ],
        None,
        ("fig_6_radar.png", "Fig 6.1 Career DNA Sample Profile"),
        adv_lim_table,
        "Table 6.1 Advantages and Limitations"
    ))

    # Page 30 appendices + references
    pages.append((
        "APPENDICES AND REFERENCES",
        [
            "Appendix A: Implementation Timeline and Milestones",
            "Appendix B: Additional Diagrams",
            "Appendix C: User Guidance Notes",
            "",
            "References",
            "[1] Pressman, Roger S. Software Engineering: A Practitioner’s Approach. McGraw-Hill, 2010.",
            "[2] FastAPI Documentation. https://fastapi.tiangolo.com/.",
            "[3] Next.js Documentation. https://nextjs.org/docs.",
            "[4] SQLAlchemy Documentation. https://docs.sqlalchemy.org/.",
            "[5] PostgreSQL Documentation. https://www.postgresql.org/docs/.",
            "[6] Vercel Platform Docs. https://vercel.com/docs.",
            "[7] Render Deployment Docs. https://render.com/docs.",
            "[8] Groq API Documentation. https://console.groq.com/docs.",
            "[9] IEEE Citation Guidance. https://ieeeauthorcenter.ieee.org/.",
        ],
        None,
        ("fig_8_gantt.png", "Fig A.1 Implementation Timeline (Illustrative)"),
        None,
        None
    ))

    total_pages = len(pages)
    assert total_pages == 30, f"Expected 30 pages, found {total_pages}"

    for idx, page in enumerate(pages, start=1):
        title, paras, bullets, fig, tbl, tbl_caption = page
        write_page(doc, title, paras, bullets, fig, tbl, tbl_caption)
        add_page_break_if_needed(doc, idx, total_pages)

    # Ensure all sections keep required margins and no header/footer.
    for sec in doc.sections:
        set_margins(sec)
        remove_header_footer(sec)
        clear_header_footer_content(sec)

    doc.save(OUTPUT)


if __name__ == "__main__":
    build_report()
    print(f"Report created: {OUTPUT}")
    print(f"Assets folder: {ASSETS}")