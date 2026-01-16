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
