# AI Cloud Cost Detective

An AI-powered cloud cost optimization platform that scans AWS resources, identifies potential cost inefficiencies, and generates actionable optimization recommendations.

This project combines AWS infrastructure analysis with AI-driven insights to help engineers detect over-provisioned resources, unused assets, and cloud cost optimization opportunities.

---

## Overview

Cloud environments often accumulate unnecessary costs due to:

- Over-provisioned EC2 instances
- Unused EBS volumes
- Idle Elastic IP addresses
- Misconfigured infrastructure resources

AI Cloud Cost Detective acts as a cloud financial investigator by:

1. Discovering AWS resources
2. Analyzing infrastructure usage patterns
3. Identifying optimization opportunities
4. Generating AI-powered recommendations
5. Estimating potential monthly savings

---

## Features

### AWS Resource Discovery

- Scan EC2 instances
- Scan EBS volumes
- Scan Elastic IP addresses
- Retrieve AWS account metadata
- Region-based resource analysis

### Cost Analysis Engine

- Detect potential cost inefficiencies
- Identify unused resources
- Surface optimization opportunities
- Generate estimated savings reports

### AI Recommendation Layer

- AI-generated optimization recommendations
- Human-readable infrastructure insights
- Suggested remediation actions
- Cost reduction guidance

### API Documentation

- Interactive Swagger UI
- OpenAPI 3.1 support
- Structured request/response schemas

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Cloud

- AWS CLI
- EC2
- EBS
- Elastic IP

### AI

- OpenAI API

### Development

- Git
- GitHub

---

## Architecture

```text
                    ┌───────────────┐
                    │    AWS CLI    │
                    └───────┬───────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Resource Scanner │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Cost Analyzer    │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ OpenAI Analyzer  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ FastAPI Backend  │
                  └────────┬─────────┘
                           │
                           ▼
                     Swagger UI
```

---

## Project Structure

```text
cloud-cost-detective/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── scanners/
│   │   ├── services/
│   │   └── main.py
│   │
│   └── requirements.txt
│
└── README.md
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Verify application status.

---

### Resource Scan

```http
GET /scan
```

Discover AWS resources within a specified region.

---

### Cost Analysis

```http
POST /analyze
```

Analyze scanned resources for optimization opportunities.

---

### AI Analysis

```http
POST /ai-analyze
```

Generate AI-powered recommendations.

---

### End-to-End AI Scan

```http
POST /ai-analyze/scan
```

Scan AWS resources and generate recommendations in a single workflow.

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/worknabhishek/AI-Cloud-Cost-Detective.git
cd AI-Cloud-Cost-Detective
```

### Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Configure AWS Credentials

```bash
aws configure
```

Verify:

```bash
aws sts get-caller-identity
```

### Configure OpenAI API Key

```bash
export OPENAI_API_KEY="your-api-key"
```

### Run Application

```bash
python3 -m uvicorn app.main:app --reload
```

---

## API Documentation

Once the application is running:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides interactive testing for all available endpoints.

---

## Current Status

### Completed

- [x] FastAPI backend
- [x] AWS resource discovery
- [x] EC2 scanning
- [x] EBS scanning
- [x] Elastic IP scanning
- [x] Cost analysis engine
- [x] OpenAPI documentation
- [x] GitHub integration

### In Progress

- [ ] React frontend dashboard
- [ ] PostgreSQL persistence layer
- [ ] Investigation history tracking
- [ ] Docker deployment
- [ ] Cloud deployment

---

## Screenshots

Coming Soon

---

## Future Enhancements

- Kubernetes cost analysis
- RDS optimization recommendations
- S3 storage analysis
- Multi-cloud support
- Historical cost tracking
- Interactive dashboard
- Automated remediation workflows

---

## Learning Outcomes

This project explores:

- FastAPI application development
- AWS resource discovery
- Infrastructure cost optimization
- API design and schema modeling
- AI-assisted infrastructure analysis
- Cloud FinOps concepts

---

## Author

**Abhishek Rathore**

Building practical DevOps and Cloud Engineering projects focused on automation, infrastructure, and AI-powered operations.
