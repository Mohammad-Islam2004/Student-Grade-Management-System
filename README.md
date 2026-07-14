# 🎓 Helix Academics | Student Grade Management System

A sleek, glassmorphic dark-themed **Student Grade Management System** built with Python, Streamlit, and Plotly. This platform provides an intuitive administrative dashboard to register students, update biographical details, record module marks, generate dynamic transcripts, and view advanced subject-level analytics.

🔗 **[Live Production Deployment App](https://student-grade-management-system.streamlit.app/)**

---

## ⚡ Key Features

* **📊 Interactive Analytics Hub:** Beautifully visualizes class performance, grade distributions, success ratios (Pass vs. Fail), and subject-by-subject average curves using high-performance Plotly charts.
* **🔍 Privacy-First Directory:** Stripped of clunky "show-all" rosters. Roster search displays records *strictly* upon entering matching name or roll-number queries.
* **🛡️ Secure Operational Verification:** Enforces a rigid roll-number check before letting users modify student demographics, delete records, or append/remove grades.
* **📄 Live Transcript Generator:** Builds clean, dynamic academic transcripts featuring real-time grade calculations, overall percentages, and color-coded **PASS** / **FAIL** status markers.
* **💾 Modular JSON Database:** Keeps the backend business logic completely independent in a separate lightweight data access layer.

---

## 📁 Repository Blueprint

```bash
├── app.py              # Front-end Streamlit UI, views, charts, & custom CSS styles
├── student.py          # Back-end Database engine, computation formulas & metrics calculations
├── data.json           # Active student database records
└── requirements.txt    # Production library requirements for cloud hosting
