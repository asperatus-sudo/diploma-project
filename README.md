#  TryHackMe: Functional & Performance Testing Framework

**An automated infrastructure designed to validate API integrity, UI stability, and system performance.** This project demonstrates a modular testing approach and seamless integration of quality assurance processes into the CI/CD lifecycle.

---

##  Architecture & Engineering
The framework is built on the **Page Object Model (POM)** design pattern, ensuring a strict separation between test logic and UI locators for high maintainability.

- **Hybrid Strategy:** Integration of functional (API/UI) and non-functional (Load) testing within a unified environment.
- **Async Orchestration:** Powered by the **SENTINEL v2.0** engine—a custom async orchestrator for real-time process monitoring and artifact delivery.
- **CI/CD Infrastructure:** Fully automated pipelines via **GitHub Actions** with segmented reporting and secure secret management.

##  Tech Stack
- **Core:** `Python 3.12+` (AsyncIO, Requests).
- **Frameworks:** `Pytest`, `Selenium WebDriver`.
- **Performance:** `Locust` (User behavior modeling and metrics analytics).
- **Observability:** `Allure Reports` and `Telegram Bot API` integration for instant fail-fast alerts.

---

##  Test Strategy & Implementation

### 1. Functional API Testing (8 Core Suites)
- **Infrastructure Integrity:** Automated audit of **HTTP Security Headers** and comprehensive **data integrity verification** of server responses.
- **Session Lifecycle Management:** Automated verification of authentication states and session health monitoring to ensure CI/CD pipeline stability.
- **Data-Driven Testing (DDT):** Large-scale navigation auditing (50+ endpoints) and dynamic room-data validation via Query parameters.
- **Error Handling:** Analysis of redirect logic and response integrity for invalid endpoints.

### 2. Functional UI Testing (7 Modular Suites)
- **Component Audit:** Stability verification of Header, Footer, and Main Content areas to ensure visual and functional consistency.
- **Complex User Flows:** Multi-step "Search & Filter" scenarios using adaptive waits and **JS-injections** to handle dynamic React-based content.
- **Navigation UX:** Functional verification of return paths and interface behavior on 404 Not Found pages.

### 3. Performance Testing (Locust)
- **Smoke Load:** Scalable load simulations with task weighting to evaluate baseline system resilience under concurrent traffic.

### 4. SENTINEL Orchestrator
An asynchronous tool for remote testing control:
- **Artifact Management:** Automated delivery of failure screenshots and zipped Allure reports via Telegram.
- **Lifecycle Control:** Cross-platform management (Start/Stop) of testing sub-processes.

---

##  CI/CD & Security
- **Result Transparency:** Segmented execution paths for API and UI layers, ensuring precise defect localization.
- **Data Confidentiality:** Industry-standard management of sensitive credentials via **encrypted environment variables**.

##  Certification
Verification of professional training (IT STEP Computer Academy) is available here:
[View Certificate](./certificates/qa_certificate.png)

---
*Developed by **Alexander Talako** | QA Engineer*