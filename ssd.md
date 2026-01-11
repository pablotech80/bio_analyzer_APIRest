# System Specification Document (SSD) - Bio•Analyze API

## 1. Project Overview
Bio•Analyze is a Flask-based API designed for biometric analysis and nutritional recommendations. It targets fitness professionals and health practitioners.

## 2. Current Beta Architecture
- **Language**: Python 3.11+
- **Framework**: Flask
- **Structure**: Modular using Blueprints (e.g., `body_analysis`, `auth`).
- **Logic**: Mathematical formulas for IMC, TMB, FFMI, etc., encapsulated in `app/utils` and `app/services`.
- **Infrastructure**: Hosted on Railway.
- **Media**: Integrated with AWS S3 for photo storage.
- **AI Integration**: OpenAI for generating intelligent interpretations of biometric data.

## 3. Production Roadmap (Beta ➡️ Professional)

### 📊 Phase 1: Data Persistence & Management
- **ORM Integration**: Complete migration to SQLAlchemy with PostgreSQL.
- **Migrations**: Use Alembic (Flask-Migrate) for consistent schema evolution.
- **Audit Logs**: Track all calculations and report generations.

### 🔐 Phase 2: Professional Security
- **Authentication**: implementation of JWT-based auth for secure API access.
- **Rate Limiting**: Protect endpoints from abuse using Flask-Limiter.
- **HTTPS/SSL**: Ensure 100% encrypted traffic (Railway managed).

### 📄 Phase 3: Reporting & Features
- **PDF Generation**: Professional report generation for user downloads.
- **History**: Allow users to track their progress over time.
- **Advanced Metrics**: Inclusion of more specialized health markers.

### 🛠️ Phase 4: Reliability & DevOps
- **Testing**: 80%+ code coverage with automated unit/integration tests.
- **Logging**: Structured logging (JSON) for better observability.
- **Monitoring**: Integration with Prometheus or similar for performance tracking.

## 4. Technical Stack (Target)
| Component | Technology |
| :--- | :--- |
| **Backend** | Flask (Python) |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Auth** | JWT / Passport |
| **Storage** | AWS S3 |
| **AI** | OpenAI GPT-4o |
| **CI/CD** | GitHub Actions |
| **Deployment** | Railway |
