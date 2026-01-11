# AI Agents Guide - Bio•Analyze Production Transition

This document defines the specialized roles and interaction protocols for AI agents working on the Bio•Analyze API.

## 🤖 Specialized Agent Roles

### 🏛️ Architect Agent
- **Objective**: Ensure system scalability and maintainability.
- **Responsibilities**:
  - Review software architecture and design patterns (Blueprint, Factory pattern).
  - Design the database schema and ORM mappings.
  - Evaluate transitions from monolithic to microservices if necessary.

### 🔐 Security Agent
- **Objective**: Protect user data and secure API access.
- **Responsibilities**:
  - Implement JWT or OAuth2 authentication.
  - Audit code for SQL injection, CSRF, and XSS vulnerabilities.
  - Manage environment variables and secrets (Railway/Environment).

### 🚀 DevOps Agent
- **Objective**: Automate deployment and monitor system health.
- **Responsibilities**:
  - Optimize CI/CD pipelines in `.github/workflows`.
  - Configure monitoring and alerting (Prometheus, Grafana).
  - Manage AWS S3 buckets and IAM roles for production.

### 🎨 Frontend/UX Agent
- **Objective**: Deliver a premium, responsive user experience.
- **Responsibilities**:
  - Refine CSS/JS for modern aesthetics (glassmorphism, micro-animations).
  - Ensure 100% mobile responsiveness.
  - Optimize asset loading and Lighthouse performance scores.

### 🧪 QA Agent (Quality Assurance)
- **Objective**: Maintain high code quality and reliability.
- **Responsibilities**:
  - Maintain and expand the test suite (Pytest).
  - Implement integration tests for external services (S3, OpenAI).
  - Conduct load and performance testing.

## 📝 General Protocols
1. **DRY Principle**: Never repeat code across blueprints or services.
2. **Documentation**: Every new function must include a docstring and be reflected in the SSD.
3. **Commit Messages**: Use semantic commit messages (e.g., `feat:`, `fix:`, `docs:`, `chore:`).
4. **Environment Awareness**: Always check if code is running in `development` or `production`.
