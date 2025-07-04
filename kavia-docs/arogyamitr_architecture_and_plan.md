# ArogyaMitr Architecture and Implementation Plan

## Introduction

ArogyaMitr is designed as a modular, full-stack health and wellness platform comprising a FastAPI-based backend and a React-based frontend. The system supports extensive health and wellness features, covering user profiles, tracking, dashboards, community and communication modules, AI-assisted chat, content, and more. This document summarizes the actionable architecture and step-by-step plan, with module breakdowns, API strategy, UI structure, integration flows, and container dependencies.

---

## 1. High-Level System Architecture

### 1.1 Containers Overview

- **Backend (arogyamitr_backend / FastAPI):**
  - Handles REST APIs, authentication, business logic, orchestration, third-party integrations, and data serving for all modules.
  - Depends on a future database service (`arogyamitr_database`).

- **Frontend (arogyamitr_frontend / React):**
  - User-facing, responsive web application.
  - Communicates via REST to backend, renders UI modules, charts, data forms, and provides rich client-side interactivity.

- **Inter-Container Dependency:**
  - Frontend strictly depends on backend for all dynamic data, authentication, and business logic.

### 1.2 Component Interaction (Mermaid Diagram)

```mermaid
graph TD
    subgraph Backend [FastAPI Backend]
      AMAPI(Main API)-->Auth
      AMAPI-->UserMgmt
      AMAPI-->Wellness
      AMAPI-->Charts
      AMAPI-->Community
      AMAPI-->Teleconsult
      AMAPI-->Profiles
      AMAPI-->AIEP(AI, Edu, Product)
      Auth -->|JWT/OAuth| UserMgmt
      Wellness --> Nutrition
      Wellness --> Fitness
      Wellness --> Mindfulness
      Wellness --> Sleep
      Community --> PeerSupport
    end
    subgraph DB [Database Service]
      DB[(Data Store)]
    end
    subgraph Frontend [React Frontend]
      WebUI --> APICalls
      WebUI --> UICharts
      WebUI --> UIChat
      WebUI --> Forms
      WebUI --> UINav
    end
    APICalls -- REST --> AMAPI
    AMAPI -- SQL/ORM --> DB
    WebUI -.-> User
```

---

## 2. Backend: FastAPI Container (arogyamitr_backend)

### 2.1 Structure

- **Entry Point:** `src/api/main.py`
  - Registers FastAPI app and CORS middleware, allowing all origins.
  - Provides health check endpoint (`GET /`).
- **Dependencies:** Listed in `requirements.txt`; includes `fastapi`, `pydantic`, `uvicorn`, `httpx`, etc.

### 2.2 Step-by-Step Module Expansion Plan

1. **Project Setup**
   - Expand folder structure: Create module folders (user, auth, wellness, charts, etc.) within `src/`.
   - Adopt a modular service/repository pattern for each domain (e.g., user, fitness, nutrition).

2. **User Management & Authentication**
   - Implement JWT and OAuth (Google, Apple) authentication.
   - CRUD APIs for user registration, login, profile, password reset, and social login.
   - Typical files: `src/api/routes/users.py`, `src/api/routes/auth.py`, `src/services/auth_service.py`

3. **Wellness Modules**
   - Diet & Nutrition, Fitness, Mindfulness, Sleep (recommend separate routers/services).
   - CRUD endpoints for user meals, activity, mindfulness logs, sleep data.
   - Endpoints for preset content (e.g., food items, workouts).

4. **Charts & Analytics APIs**
   - Expose endpoints to serve summarized analytics (progress rings, bars, line charts, disease anomaly alerts).
   - Eg: `/analytics/progress`, `/analytics/disease-alerts`

5. **Product Scanner & Directory**
   - API endpoint to submit product scan, return ethical score/details.
   - APIs for ethical business/resource directory.

6. **Community and Communication**
   - Peer support, forums, and health event endpoints.
   - Tele-consultation APIs for managing appointments, video call tokens, etc.

7. **Education & AI Chatbot**
   - Article endpoints, video content endpoints, integration with AI chat service.

8. **Third-Party Integrations**
   - Authentication (Google, Apple), payments (Stripe).
   - Reflected as external service modules.

9. **Profile & Settings**
   - Device management, notification settings, user preferences.

10. **Admin, Security and Middleware**
    - RBAC, admin routes, rate limiting, audit trails, centralized error handling.

### 2.3 Implementation Notes

- **Directory Example:**
  ```
  src/
    api/
      main.py
      routes/
        users.py
        auth.py
        nutrition.py
        fitness.py
        ...
    services/
      user_service.py
      nutrition_service.py
      ...
    models/
      user.py
      nutrition.py
    ...
  ```
- **Testing:** Use pytest for route/service tests.
- **Data Layer:** Future support for DB via `arogyamitr_database`; initial stubs return dummy/static data.

---

## 3. Frontend: React Container (arogyamitr_frontend)

### 3.1 Structure

- **Entry Point:** `src/index.js` – mounts React to DOM.
- **Core Component:** `src/App.js`
  - Manages app-wide effects (e.g., theme toggling).
  - Shows a simple structure with a header, theme switch, and content area.

- **Styling:** `src/App.css` declares light/dark theme variables, responsive CSS, and UI elements.

### 3.2 UI and Component Organization Plan

1. **Project Setup**
   - Use modern React (functional components, hooks).
   - Organize modules in `src/` with folders per feature: `/dashboard`, `/wellness`, `/chat`, `/profile`, etc.

2. **Navigation & Routing**
   - Implement sidebar + header navigation consistent with planned layout (`dashboard navigation sidebar, header bar, modals, tabbed views`).
   - Use `react-router` for modular page routing.

3. **Landing & Dashboard**
   - Personalized dashboard with user greetings, metrics, charts.
   - Top-level cards/sections for health modules.

4. **Module-Specific Components**
   - Wellness tracking modules: Forms & visualizations for diet, fitness, sleep, mindfulness.
   - Chart rendering: Integrate chart library (e.g., Chart.js or Recharts) for progress rings, etc.

5. **Community, Tele-Consultation, Resources**
   - Event calendars, chat/forum UIs, tele-consultation booking dialogs.
   - Integration with backend via fetch/XHR.

6. **Educational Content & AI Chat**
   - Media player, article list/detail.
   - Chatbot UI component; suggestive prompt buttons.

7. **Profile, Device, and Settings**
   - User info forms, notification/device manager modules.

8. **Theming and Branding**
   - Maintain style via CSS variables in `src/App.css`.
   - Allow theme switching with single source of truth (as in App.js).

### 3.3 Integration and Data Flow

- All data interactions use async calls to backend REST APIs.
- Use context/hooks for global state (logged-in user, dark/light theme, active metrics).
- Use modular, re-usable components for charts, cards, forms, dialogs.

---

## 4. Integration Flows and Considerations

- **API Security:** Use JWT bearer tokens for all API calls; handle OAuth for login/registration.
- **CORS:** Enabled to allow frontend to access backend APIs (see backend main.py middleware).
- **State Management:** Client-side state held in hooks/context; persists minimal state to local storage (auth tokens etc).
- **Consistent Typing and Validation:** Use Pydantic backend models and frontend JS validation.
- **Testing:** Frontend with Jest/React Testing Library; backend with pytest.

---

## 5. Implementation Steps Summary

1. **Bootstrap folders & core entrypoints**
2. **Stub out all planned backend and frontend modules as separate files/components**
3. **Implement authentication and user flow end-to-end**
4. **Build dashboard and first wellness module (diet/nutrition) with full API/UI interaction**
5. **Iteratively add all health, community, AI, and auxiliary modules**
6. **Integrate third-party logins, payments, and chart libraries**
7. **Add testing, admin, and hardening layers**

---

## 6. Major Considerations

- Plan for modular growth; strictly separate backend and frontend concerns.
- Make all business logic reside in the backend; frontend orchestrates UI and user flows.
- Encapsulate third-party service integrations.
- Provide graceful error handling, loading states, and skeleton UIs.
- Document code and APIs as modules are added for maintainability.

---

### Appendix: Tech Stack Summary

- **Backend:** Python, FastAPI, Pydantic, Uvicorn, Pytest
- **Frontend:** React, Vanilla CSS, (planned) Chart.js/Recharts, Jest, React Testing Library

---

_End of document_
