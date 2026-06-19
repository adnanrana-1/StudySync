# 📚 StudySync

> **Smart Study Group Finder & Session Manager**
> 
> **An Open-Source Collaborative Academic Networking and Peer Matchmaking Platform**
> 
> *Final Semester Project | Department of Computer Science / Information Technology* > *Course: SE-494 Open Source Software Development (Section Y9)* > *Institution: University of Management and Technology (UMT)* StudySync is an advanced web intelligence platform designed to bridge the gap between university students looking for study partners, shared resources, and group execution environments. Built with an asynchronous decoupled architecture, it combines a responsive client-side interface with a secure, highly concurrent distributed backend API engine.

---

## 🚀 Key Features

* **Smart Partner Discovery:** Automated peer profile filtering and matchmaking workflows relying on intersection matrices across academic subject arrays.
* **Session Lifecycle Manager:** Full CRUD implementation allowing automated creation, synchronization, user joining, and deletion of structured study groups.
* **Peer Accountability Matrix:** An end-to-end review pipeline for users to submit programmatic score telemetry and qualitative remarks on group interactions.
* **Stateless Guard Isolation:** Secure token-based access controls using JSON Web Tokens (JWT) to secure state mutations across user profile actions.

---

## 🛠️ Tech Stack & Architecture

### Frontend Application
* **Structure & UI Logic:** HTML5 semantic layouts backed by responsive CSS3 layout overrides.
* **Network & State Handlers:** Vanilla JavaScript (ES6+) asynchronous `fetch()` API execution layers equipped with stateful local storage token handling.

### Backend Infrastructure
* **Core Microservice Engine:** FastAPI (Python compatible, native high-performance asynchronous concurrency ecosystem).
* **Asynchronous Driver Object:** Motor (Non-blocking, event-driven MongoDB engine interface).
* **Security & Cipher Systems:** PyJWT (JSON Web Tokens) coupled with Passlib and Bcrypt cryptographic salted password-hashing layers.

### Database Layer
* **Database Management System:** MongoDB (NoSQL Document Store initialized locally/via cloud clusters).

---

## 📦 Directory Structure

```text
StudySync - Smart Study Group Finder/
├── README.md                # Central project system architecture manual
├── backend/
│   ├── app/                 # Application routes, controllers, and core logic
│   ├── .env                 # Environment application variable secrets configuration
│   ├── main.py              # Main ASGI gateway entry point file
│   └── requirements.txt     # Python ecosystem backend dependencies
└── frontend/
    ├── css/                 # Global UI presentation override configuration sheets
    ├── js/                  # App network script interaction handlers (Fetch API)
    ├── index.html           # System landing portal entry point
    ├── login.html           # Authentication and entry layout boundary
    ├── dashboard.html       # Authorized core operations layout overview
    ├── browse.html          # Peer matchmaking discovery user interface
    └── sessions.html        # Group scheduling management framework panel

🗄️ Database Document Schema Design
 application maps entities using JSON-modeled collections inside MongoDB:

users Collection
JSON
{
  "_id": "ObjectId",
  "name": "Adnan Rana",
  "email": "adnan@umt.edu.pk",
  "hashed_password": "$bcrypt$v=2$r=12$...",
  "subjects": ["Data Structures", "Web Development", "Database Systems"],
  "bio": "Preparing for final semester examinations. Looking for back-end study groups.",
  "created_at": "ISODate"
}
 
study_sessions Collection
JSON
{
  "_id": "ObjectId",
  "title": "FastAPI Masterclass Prep",
  "subject": "Web Development",
  "description": "Deep-dive into async routers, middleware hooks, and cloud-native DB seeding.",
  "date_time": "2026-06-19T14:00:00Z",
  "location": "UMT Central Library / Teams",
  "creator_id": "ObjectId",
  "max_participants": 5,
  "participants": ["ObjectId_User_1", "ObjectId_User_2"]
}

ratings Collection
JSON
{
  "_id": "ObjectId",
  "session_id": "ObjectId",
  "reviewer_id": "ObjectId",
  "reviewee_id": "ObjectId",
  "rating": 5,
  "comment": "Exemplary collaborative preparation, well versed in database schema structure."
}