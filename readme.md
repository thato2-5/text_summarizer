# Text Summarizer API

## Overview
A RESTful API for text summarization built with Flask that provides intelligent text summarization, user management, and analytics capabilities. The API supports multiple NLP algorithms for generating concise summaries while maintaining the original meaning of the text.

# Features

### Core Functionality
- Text Summarization: Generate summaries using LSA, TextRank, Luhn, and LexRank algorithms
- User Management: Secure authentication and profile management
- History Tracking: Store and retrieve summarization history
- Analytics Dashboard: Track usage statistics and performance metrics
- Multi-language Support: Process text in various languages

#### Security Features
- Password hashing with bcrypt
- JWT-based authentication
- CSRF protection
- SQL injection prevention
- Input sanitization and validation

# API Documentation

### Base URL
```text
https://your-domain.com/api/v1
```

# Authentication Endpoints

- POST /auth/login
- Authenticate user and return JWT token.

### Request:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "user@example.com"
  }
}
```

POST /auth/register

Create a new user account.

### Request:
```json
{
  "username": "john_doe",
  "email": "user@example.com",
  "password": "securepassword123",
  "confirm_password": "securepassword123"
}
```

### Response:
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "user@example.com"
  }
}
```

POST /auth/logout

Invalidate user session token.

### Headers:
```text
Authorization: Bearer <token>
```

### Response:
```json
{
  "message": "Successfully logged out"
}
```

Summary Endpoints
POST /summarize

Generate a summary from input text.

### Headers:
```text
Authorization: Bearer <token>
Content-Type: application/json    
```

### Request:
```json
{
  "text": "Full text content goes here...",
  "algorithm": "lsa",  // Options: lsa, textrank, luhn, lexrank
  "summary_percent": 30,  // Percentage of original text
  "title": "Optional title for the summary"
}
```

### Response:
```json
{
  "id": 123,
  "title": "Generated Summary Title",
  "original_text": "Full text content goes here...",
  "summary_text": "Condensed summary text here...",
  "original_length": 1200,
  "summary_length": 360,
  "compression_ratio": 30.0,
  "algorithm": "lsa",
  "processing_time": 2.45,
  "created_at": "2024-01-15T10:30:00Z"
}
```

GET /docs

Interactive API documentation (Swagger UI).
Error Handling
Error Response Format

# Error Handling

## Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}  // Optional additional details
  }
}
```

### Common Error Codes
- AUTH_001: Invalid credentials
- AUTH_002: Token expired
- AUTH_003: Insufficient permissions
- VALID_001: Invalid input data
- VALID_002: Missing required field
- DB_001: Database error
- DB_001: Database error
- NLP_001: Text processing error
- RATE_001: Rate limit exceeded

### HTTP Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity
- 429: Too Many Requests
- 500: Internal Server Error

### Rate Limiting
- Authenticated users: 100 requests/minute
- Unauthenticated users: 20 requests/minute
- Summarization endpoint: 10 requests/minute per user

## Installation

### Prerequisites
- Python 3.8+
- pip package manager
- SQLite (development) or PostgreSQL (production)

## Setup
```bash
# Clone repository
git clone https://github.com/yourusername/text-summarizer-api.git
cd text-summarizer-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
flask db upgrade

# Start development server
flask run
```

## Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

# Configuration
## Environment Variables
```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///app.db  # Development
# DATABASE_URL=postgresql://user:password@localhost/dbname  # Production

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour

# Rate Limiting
RATELIMIT_STORAGE_URL=redis://localhost:6379/0

# External Services
SENTRY_DSN=your-sentry-dsn  # Optional
```

# Development
## Running Tests
```bash
# Run all tests
pytest

# Run specific test category
pytest tests/test_auth.py
pytest tests/test_summarization.py
pytest tests/test_api.py

# Run with coverage
pytest --cov=app tests/
```

## Support
- Issues: https://github.com/thato2-5/text_summarizer/issues
- Email: support@monyatech.org.za

## Performance
- Average response time: < 500ms
- Maximum text length: 10,000 words
- Concurrent users: Up to 1000
- Uptime SLA: 99.9%

## Monitoring

### The API includes built-in monitoring endpoints:
- /health - System health status
- /metrics - Prometheus metrics (if enabled)
- Error tracking with Sentry integration
- Performance monitoring with New Relic/DataDog integration

# Screenshot:
![alt text](https://github.com/thato2-5/text_summarizer/blob/main/home.png)

# Screenshot:
![alt text](https://github.com/thato2-5/text_summarizer/blob/main/home01.png)

# Screenshot:
![alt text](https://github.com/thato2-5/text_summarizer/blob/main/home02.png)

# Screenshot:
![alt text](https://github.com/thato2-5/text_summarizer/blob/main/home03.png)

# Screenshot:
![alt text](https://github.com/thato2-5/text_summarizer/blob/main/home04.png)

# Screenshot:
![alt text](https://github.com/thato2-5/text_summarizer/blob/main/home05.png)

# Screenshot:
![alt text](https://github.com/thato2-5/text_summarizer/blob/main/home06.png)

# Screenshot:
![alt text](https://github.com/thato2-5/text_summarizer/blob/main/home07.png)

# 1. System Architecture Diagram
```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Web Browser] --> B[Flask Templates]
        B --> C[Static Assets<br/>CSS/JS/Images]
    end

    subgraph "Application Layer"
        D[Flask Application] --> E[Authentication Module]
        D --> F[Summarization Engine]
        D --> G[Analytics Module]
        E --> H[User Management]
        F --> I[NLP Processing]
        G --> J[Data Visualization]
    end

    subgraph "Data Layer"
        K[SQLite Database] --> L[Users Table]
        K --> M[Summaries Table]
        N[External APIs] --> O[Wikipedia Content]
    end

    subgraph "NLP Layer"
        P[NLTK Library] --> Q[Text Processing]
        R[Sumy Library] --> S[Summarization Algorithms]
        T[TextBlob] --> U[Sentiment Analysis]
    end

    A --> D
    D --> K
    D --> P
    D --> R
    D --> T
    F --> N

    style A fill:#e1f5fe
    style D fill:#f3e5f5
    style K fill:#e8f5e8
    style P fill:#fff3e0
```

# 2. Database Schema Diagram
```mermaid
erDiagram
    USER {
        int id PK "Primary Key"
        string username UK "Unique"
        string email UK "Unique"
        string password_hash "Hashed"
        datetime created_at "Timestamp"
        boolean is_active "Status"
    }

    SUMMARY {
        int id PK "Primary Key"
        text original_text "Full text"
        text summary_text "Summarized text"
        int summary_length "Word count"
        int original_length "Word count"
        float compression_ratio "Ratio"
        datetime created_at "Timestamp"
        int user_id FK "Foreign Key"
        string title "Summary title"
        string language "Text language"
    }

    USER ||--o{ SUMMARY : creates
    SUMMARY }|--|| USER : belongs_to

    note left of USER
        User authentication and
        profile management
        - Password hashing
        - Session management
        - Account status
    end note

    note right of SUMMARY
        Text summarization records
        - Original and summary text
        - Length metrics
        - Compression statistics
        - Timestamp tracking
    end note
```

# 3. User Authentication Flowchart
```mermaid
flowchart TD
    Start([Start]) --> CheckAuth{User Authenticated?}
    
    CheckAuth -->|No| ShowLanding[Show Landing Page]
    CheckAuth -->|Yes| RedirectDashboard[Redirect to Dashboard]
    
    ShowLanding --> AuthChoice{Authentication Choice}
    AuthChoice -->|Login| ShowLogin[Show Login Form]
    AuthChoice -->|Register| ShowRegister[Show Registration Form]
    
    ShowLogin --> SubmitLogin[Submit Login Credentials]
    SubmitLogin --> ValidateLogin{Validate Credentials}
    
    ValidateLogin -->|Invalid| ShowError[Show Error Message]
    ValidateLogin -->|Valid| CreateSession[Create User Session]
    
    ShowRegister --> SubmitRegister[Submit Registration]
    SubmitRegister --> ValidateRegister{Validate Registration}
    
    ValidateRegister -->|Invalid| ShowRegError[Show Registration Error]
    ValidateRegister -->|Valid| CreateUser[Create New User]
    CreateUser --> AutoLogin[Auto-Login New User]
    
    ShowError --> ShowLogin
    ShowRegError --> ShowRegister
    CreateSession --> RedirectDashboard
    AutoLogin --> RedirectDashboard
    
    RedirectDashboard --> ShowDashboard[Show User Dashboard]
    ShowDashboard --> UserActions{User Actions}
    
    UserActions -->|Logout| DestroySession[Destroy Session]
    UserActions -->|Continue| MaintainSession[Maintain Session]
    
    DestroySession --> ShowLanding
    MaintainSession --> ShowDashboard

    style Start fill:#4caf50
    style RedirectDashboard fill:#2196f3
    style DestroySession fill:#ff9800
```

# 4. Text Summarization Workflow
```mermaid
sequenceDiagram
    participant U as User
    participant F as Flask App
    participant S as Summarization Engine
    participant DB as Database
    participant NLP as NLP Libraries

    U->>F: Submit Text for Summarization
    F->>F: Validate Input Text
    F->>F: Preprocess Text (clean, tokenize)
    F->>S: Request Summary Generation
    
    S->>NLP: Apply Selected Algorithm
    Note over S,NLP: LSA, TextRank,<br/>Luhn, or LexRank
    
    NLP->>S: Return Summary Sentences
    S->>S: Calculate Metrics
    Note over S: Word count,<br/>compression ratio,<br/>sentiment analysis
    
    S->>F: Return Summary + Metrics
    F->>DB: Save Summary Record
    DB->>F: Confirm Save Operation
    F->>U: Display Summary Results
    F->>U: Update Analytics Dashboard
    
    Note over U,F: Real-time feedback<br/>and progress indicators
```

# 5. Component Relationship Diagram
```mermaid
graph LR
    subgraph "Core Components"
        A[Flask Application]
        B[Authentication System]
        C[Summarization Engine]
        D[Analytics Dashboard]
        E[Database Models]
    end

    subgraph "Supporting Libraries"
        F[Flask-Login]
        G[Flask-SQLAlchemy]
        H[NLTK]
        I[Sumy]
        J[TextBlob]
    end

    subgraph "User Interface"
        K[Templates]
        L[Static Files]
        M[Forms]
        N[Charts]
    end

    subgraph "Data Storage"
        O[SQLite Database]
        P[User Sessions]
        Q[Summary Records]
    end

    A --> B
    A --> C
    A --> D
    A --> E
    
    B --> F
    E --> G
    C --> H
    C --> I
    C --> J
    
    A --> K
    A --> L
    B --> M
    D --> N
    
    E --> O
    B --> P
    E --> Q

    style A fill:#bbdefb
    style B fill:#c8e6c9
    style C fill:#fff9c4
    style D fill:#ffccbc
```

# 6. Data Flow Diagram
```mermaid
flowchart TD
    A[User Input Text] --> B{Input Validation}
    B -->|Valid| C[Text Preprocessing]
    B -->|Invalid| D[Error Message]
    
    C --> E[Algorithm Selection]
    E --> F{LSA Algorithm}
    E --> G{TextRank Algorithm}
    E --> H{Luhn Algorithm}
    E --> I{LexRank Algorithm}
    
    F --> J[Generate Summary]
    G --> J
    H --> J
    I --> J
    
    J --> K[Metrics Calculation]
    K --> L[Database Storage]
    L --> M[Results Display]
    M --> N[Analytics Update]
    N --> O[Dashboard Refresh]
    
    D --> P[User Feedback]
    P --> A
    
    style A fill:#e3f2fd
    style J fill:#c8e6c9
    style M fill:#fff3e0
    style O fill:#fce4ec
```

# 7. User Journey Map
```mermaid
journey
    title Text Summarizer User Journey
    section Registration
      Visit Website: 5: User
      Register Account: 4: User
      Verify Email: 3: System
    section Summarization
      Input Text: 5: User
      Select Parameters: 4: User
      Generate Summary: 5: System
      View Results: 5: User
    section Analytics
      View Dashboard: 4: User
      Filter History: 3: User
      Export Data: 2: User
    section Management
      Update Profile: 3: User
      Manage Summaries: 4: User
      Delete Account: 1: User
```

# 8. Deployment Architecture
```mermaid
graph TB
    subgraph "Production Environment"
        A[Load Balancer] --> B[Web Server 1]
        A --> C[Web Server 2]
        A --> D[Web Server N]
        
        B --> E[Application Server]
        C --> E
        D --> E
        
        E --> F[(Database Cluster)]
        E --> G[File Storage]
        E --> H[Cache Layer]
        
        I[Monitoring] --> E
        I --> F
        J[Backup System] --> F
        J --> G
    end

    subgraph "External Services"
        K[CDN] --> L[Static Assets]
        M[Email Service] --> N[Notifications]
        O[Analytics] --> P[Usage Tracking]
    end

    style A fill:#ff9800
    style E fill:#4caf50
    style F fill:#2196f3
    style I fill:#f44336
```

# 9. API Endpoints Diagram
```mermaid
graph TD
    subgraph "Authentication Flow"
        A1[POST /auth/login] --> A2{Authenticate User<br/>Return JWT Token}
        B1[POST /auth/register] --> B2{Create User Account<br/>Send Verification}
        C1[POST /auth/logout] --> C2{Invalidate Token<br/>Clear Session}
    end

    subgraph "Summary Management"
        D1[POST /api/summarize] --> D2{Process Text/URL<br/>Generate & Store Summary}
        E1[GET /api/history] --> E2{Retrieve User's<br/>Summary History}
        F1[GET /api/summary/:id] --> F2{Validate Ownership<br/>Return Summary}
        G1[DELETE /api/summary/:id] --> G2{Verify Permissions<br/>Remove Summary}
    end

    subgraph "Analytics & Dashboard"
        H1[GET /api/dashboard] --> H2{Aggregate User Data<br/>Return Statistics}
        I1[GET /api/analytics] --> I2{Process Metrics<br/>Return JSON Data}
    end

    subgraph "System Endpoints"
        J1[GET /] --> J2{Serve Frontend<br/>or API Info}
        K1[GET /health] --> K2{System Status<br/>& Metrics}
        L1[GET /docs] --> L2{API Documentation<br/>& Examples}
    end

    style A1 fill:#c8e6c9
    style D1 fill:#bbdefb
    style H1 fill:#fff9c4
    style J1 fill:#ffccbc
```

# 10. Security Architecture Diagram
```mermaid
graph TB
    subgraph "Security Layers"
        A[HTTPS Encryption] --> B[Firewall Protection]
        B --> C[User Authentication]
        C --> D[Session Management]
        D --> E[Data Validation]
        E --> F[Database Security]
    end

    subgraph "Authentication Flow"
        G[Password Hashing] --> H[bcrypt Algorithm]
        I[Session Tokens] --> J[Secure Cookies]
        K[CSRF Protection] --> L[Form Validation]
    end

    subgraph "Data Protection"
        M[Input Sanitization] --> N[XSS Prevention]
        O[SQL Injection Prevention] --> P[Parameterized Queries]
        Q[Data Encryption] --> R[At Rest & Transit]
    end

    C --> G
    C --> I
    D --> K
    E --> M
    E --> O
    F --> Q

    style A fill:#ffebee
    style C fill:#f3e5f5
    style F fill:#e8f5e8
```

# 11. Testing Strategy Diagram
```mermaid
graph TD
    subgraph "Testing Pyramid"
        A[Unit Tests] --> B[Component Tests]
        B --> C[Integration Tests]
        C --> D[End-to-End Tests]
    end

    subgraph "Test Categories"
        E[Authentication Tests] --> F[Login/Register]
        G[Summarization Tests] --> H[NLP Algorithms]
        I[API Tests] --> J[Endpoints Validation]
        K[UI Tests] --> L[User Interface]
    end

    subgraph "Test Data"
        M[Sample Users] --> N[Realistic Profiles]
        O[Sample Texts] --> P[Various Domains]
        Q[Performance Data] --> R[Load Testing]
    end

    A --> E
    A --> G
    B --> I
    C --> K
    D --> L
    
    E --> M
    G --> O
    K --> Q

    style A fill:#e1f5fe
    style D fill:#4caf50
    style M fill:#fff3e0
```

# 12. Monitoring and Analytics Diagram
```mermaid
graph TB
    subgraph "Data Sources"
        A[User Requests & Actions] --> B[Application Logs]
        C[System Resources] --> D[Performance Metrics]
        E[Application Errors] --> F[Error Traces]
        G[Business Events] --> H[Usage Analytics]
    end

    subgraph "Processing Pipeline"
        I[Log Aggregator<br/>e.g., Fluentd, Logstash] --> J[Message Queue<br/>e.g., Kafka, RabbitMQ]
        K[Metrics Collector<br/>e.g., Prometheus] --> L[Time-Series Database]
        M[Error Collector<br/>e.g., Sentry] --> N[Error Database]
        
        J --> O[Stream Processor]
        L --> P[Metric Analyzer]
        N --> Q[Error Analyzer]
    end

    subgraph "Storage & Analysis"
        O --> R[Processed Data Store]
        P --> S[Aggregated Metrics]
        Q --> T[Error Trends]
        
        R --> U[Analytics Engine]
        S --> U
        T --> U
    end

    subgraph "Visualization & Alerting"
        U --> V[Monitoring Dashboard<br/>e.g., Grafana]
        U --> W[Scheduled Reports<br/>PDF/Email]
        U --> X[Alert Manager<br/>Slack/Email/PagerDuty]
        
        V --> Y[Real-time Charts]
        W --> Z[Historical Insights]
        X --> AA[Incident Response]
    end

    style A fill:#f3e5f5
    style I fill:#c8e6c9
    style V fill:#bbdefb
    style X fill:#ffccbc
```
