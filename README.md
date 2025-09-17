# CV Evaluation Engine

A RESTful API-based CV evaluation system that automatically scores and analyzes CVs for data professionals. The system provides dual evaluation modes: general market assessment and job-specific matching.

## Overview

The CV Evaluation Engine helps assess data professionals' CVs and matches them with relevant opportunities. It empowers data professionals to understand their market positioning while helping companies identify top talent efficiently.

### Key Features

- Dual-mode evaluation: general market assessment and job-specific matching
- Advanced NLP-based skill extraction and analysis
- Contextual experience and education evaluation
- AI-powered insights and career recommendations
- RESTful API with comprehensive documentation
- Docker containerization for easy deployment

## Business Value

**For Data Professionals:**
- Understand market positioning and career level
- Get personalized career guidance and skill gap analysis
- Receive targeted job application advice
- Access actionable improvement recommendations

**For Companies:**
- Automate initial CV screening process
- Quickly identify qualified candidates
- Make data-driven hiring decisions
- Reduce time-to-hire with intelligent matching

## Technology Stack

### Core Technologies
- **FastAPI** - Modern Python web framework for building APIs
- **UV** - Fast Python package installer and resolver
- **Docker** - Containerization platform
- **Pydantic** - Data validation using Python type annotations

### NLP & AI Stack
- **spaCy** - Advanced natural language processing
- **sentence-transformers** - Semantic similarity and embeddings
- **scikit-learn** - Machine learning algorithms
- **OpenAI/Local LLMs** - Large language model integration

### Development Tools
- **pytest** - Testing framework
- **Makefile** - Build automation
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
cv-evaluation-engine/
├── Makefile                    # Build automation
├── pyproject.toml             # UV package configuration
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-container orchestration
├── .env.example              # Environment variables template
│
├── app/                       # Main application directory
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Configuration management
│   │
│   ├── api/v1/endpoints/      # API route handlers
│   │   ├── upload.py         # CV upload endpoints
│   │   ├── evaluate.py       # Evaluation endpoints
│   │   ├── jobs.py           # Job-related endpoints
│   │   ├── results.py        # Results retrieval
│   │   └── health.py         # Health check endpoints
│   │
│   ├── core/                 # Core business logic
│   │   ├── cv_processor/     # Text extraction and parsing
│   │   ├── evaluator/        # Scoring algorithms
│   │   ├── job_analyzer/     # Job description analysis
│   │   ├── matchers/         # CV-job matching logic
│   │   └── ai_enhancements/  # LLM-powered features
│   │
│   ├── models/               # Pydantic data models
│   ├── services/             # Business logic services
│   └── resources/            # Static data and configurations
│       ├── market_standards/ # General evaluation benchmarks
│       ├── jobs/             # Job templates and postings
│       └── skills/           # Skills taxonomy and mappings
│
├── tests/                    # Comprehensive test suite
├── scripts/                  # Utility scripts
└── docs/                     # Documentation
```

## API Endpoints

### Core Endpoints

#### CV Upload
```
POST /api/v1/upload
Content-Type: multipart/form-data
```
Upload CV files (PDF, TXT, DOCX) and receive upload ID for processing.

#### General Market Evaluation
```
GET /api/v1/evaluate/general/{upload_id}
```
Evaluate CV against general market standards and industry benchmarks.

#### Job-Specific Matching
```
POST /api/v1/evaluate/job-match/{upload_id}
```
Compare CV against specific job requirements and calculate match percentage.

#### Comprehensive Analysis
```
POST /api/v1/evaluate/comprehensive/{upload_id}
```
Perform both general and job-specific evaluation with comparative insights.

#### Job Description Parsing
```
POST /api/v1/jobs/parse
```
Parse and structure job descriptions for matching analysis.

#### Results Retrieval
```
GET /api/v1/results/{evaluation_id}
```
Retrieve detailed evaluation results with recommendations and insights.

## Evaluation Methodology

### General Market Evaluation (0-100 Score)

**Skills Assessment (50 points)**
- Advanced NLP-based skill detection and categorization
- Market demand weighting and proficiency level analysis
- Semantic matching for skill variations and synonyms
- Skill combination and synergy evaluation

**Experience Analysis (30 points)**
- Contextual work history parsing and role classification
- Career progression and seniority level assessment
- Relevant vs total experience calculation
- Impact and achievement quantification

**Education Evaluation (20 points)**
- Degree level recognition and field relevance scoring
- Professional certification and continuous learning assessment
- Market expectation alignment and industry standards

### Job-Specific Matching

**Requirements Analysis**
- Must-have vs nice-to-have skill alignment scoring
- Experience level and seniority compatibility assessment
- Education requirement fulfillment verification
- Soft skills and cultural fit evaluation

**Gap Analysis**
- Critical missing skill identification and prioritization
- Learning path suggestions with timeline estimates
- Application readiness scoring and improvement recommendations
- Competitive advantage highlighting

## Data Sources and Comparisons

### General Evaluation References
- Curated market standards database for various data science roles
- Aggregated job market intelligence and skill demand trends
- Anonymized peer benchmark data and industry progression patterns
- Current salary ranges and career advancement metrics

### Job-Specific Matching References
- User-provided job descriptions with intelligent parsing
- Curated job templates covering common role patterns
- Active job posting analysis and requirement extraction
- Company profile and industry context integration

## Prerequisites

### System Requirements
- Python 3.11 or higher
- Docker and Docker Compose
- Make (GNU Make)
- Git version control

### Installing UV
```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Development Setup

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd cv-evaluation-engine

# Copy environment configuration
cp .env.example .env

# Install dependencies and start development server
make install
make dev
```

### Available Make Commands

#### Development Commands
- `make install` - Install dependencies with UV
- `make dev` - Start development server
- `make test` - Run comprehensive test suite
- `make lint` - Run code linting and formatting
- `make type-check` - Execute static type checking

#### Docker Commands
- `make docker-build` - Build Docker image
- `make docker-run` - Run containerized application
- `make docker-dev` - Development with Docker Compose

#### Data Management Commands
- `make init-db` - Initialize database
- `make populate-data` - Load initial market data and job templates
- `make populate-skills` - Load skills taxonomy database

#### Utility Commands
- `make clean` - Clean temporary files and caches
- `make logs` - View application logs
- `make benchmark` - Run performance benchmarks

## Implementation Phases

### Phase 1: Core Foundation (Week 1-2)
- Project setup with FastAPI, UV, and Docker configuration
- Basic file upload and text extraction functionality
- Simple skill detection and scoring algorithms
- General market evaluation API endpoint implementation
- Basic test coverage and documentation

### Phase 2: Job Integration (Week 2-3)
- Job description parser and requirements extraction
- CV-job matching algorithms and scoring logic
- Job-specific evaluation endpoint development
- Gap analysis and targeted recommendation engine
- Enhanced skill detection with semantic matching

### Phase 3: AI Enhancements (Week 3-4)
- Large language model integration for advanced insights
- Intelligent feedback generation and career guidance
- Market intelligence analysis and trend identification
- Personalized recommendation system development
- Advanced contextual analysis capabilities

### Phase 4: Production Readiness (Week 4)
- Comprehensive testing suite with edge case coverage
- Performance optimization and scalability improvements
- Robust error handling and input validation
- Complete documentation and deployment guides
- Monitoring, logging, and observability setup

## Performance Targets

### Technical Metrics
- CV processing time: Less than 10 seconds per document
- API response time: Less than 2 seconds for standard requests
- Skill extraction accuracy: Greater than 85% precision and recall
- System availability: Greater than 99% uptime

### Business Metrics
- Actionable insights provided in every evaluation report
- Clear improvement recommendations with specific action items
- Accurate market positioning and career level assessment
- Demonstrable value for both job seekers and recruiters

## Testing Strategy

### Test Coverage
- Unit tests for individual component functionality
- Integration tests for end-to-end API workflows
- Performance tests for scalability and load handling
- Edge case testing for robust error handling

### Test Data
- Curated collection of sample CVs across experience levels
- Diverse job descriptions covering various data science roles
- Edge cases including unusual formats and incomplete information
- Validation datasets for accuracy measurement

## Deployment

### Development Environment
```bash
make install
make dev
# API available at http://localhost:8000
```

### Docker Deployment
```bash
make docker-build
make docker-run
# API available at http://localhost:8000
```

### Production Deployment
- Container registry configuration and image management
- Environment variable management and security
- Load balancer setup and health check configuration
- Monitoring and alerting system integration

## Contributing

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Write comprehensive tests for new functionality
- Update documentation for API changes
- Use type hints for all function signatures

### Code Quality
- All code must pass linting and type checking
- Minimum 80% test coverage required
- Performance benchmarks must be maintained
- Security best practices must be followed

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For questions, issues, or contributions, please refer to the project documentation or contact the development team.