# Frontend for Cloud Cost Detective

A Vite + React + TypeScript frontend for AWS cloud cost optimization analysis.

## Features

- **Dashboard** — Account overview, total resources, findings count, backend health
- **Resource Inventory** — EC2 instances, EBS volumes, Elastic IPs with search and filtering
- **Cost Analysis** — Rule-based cost optimization findings grouped by category (Cost Optimization / Governance)
- **AI Recommendations** — AI-powered optimization recommendations with graceful fallback to rule-based analysis

## Real Cost Optimization Rules

Detects:
- **Unattached EBS Volumes** — Free volumes costing $0.10/GiB/month
- **Unassociated Elastic IPs** — Unused IPs costing $3.25/month
- **EC2 Rightsizing** — Oversized instances (t3.small/medium/large) with downsize recommendations
- **Missing Tags** — Governance findings for cost allocation compliance

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

The frontend connects to `http://localhost:8000` by default.

To use a different backend:

```bash
VITE_API_BASE=http://your-backend:8000 npm run dev
```

## API Integration

The frontend calls:
- `GET /health` — Backend health check
- `GET /scan?region=us-east-1` — Scan AWS resources
- `POST /analyze` — Rule-based cost analysis
- `POST /ai-analyze` — AI-powered recommendations (fallback to rules if unavailable)

## Error Handling

- Loading states for all async operations
- Empty states when no data is returned
- Graceful handling of API errors (e.g., 503 from missing OPENAI_API_KEY)
- Severity badges (low/medium/high) for findings
- Resource type and state indicators

## Pages

### Dashboard
- Account ID, region, total resource count
- Findings count and estimated monthly savings
- Backend health status

### Resource Inventory
- Searchable tables: EC2, EBS, Elastic IPs
- Status badges (running, in-use, available, attached, free)
- Availability zones, instance types, volume sizes

### Cost Analysis
- **Total Monthly Savings** — Sum of all optimization opportunities
- **Estimated Monthly Cost** — Baseline cost without optimizations
- **Cost Optimization Findings** — High-impact savings (unattached volumes, unassociated IPs, rightsizing)
- **Governance Findings** — Compliance recommendations (missing tags)
- Severity badges and per-finding savings

### AI Recommendations
- **When AI is available** — OpenAI-powered insights with remediation commands
- **When AI is unavailable** — Fallback to rule-based recommendations with user-friendly message
- Expandable cards for each recommendation
- AWS CLI commands for remediation

## Environment

Optional: Set `VITE_API_BASE` to override default backend URL.

```bash
VITE_API_BASE=https://api.example.com npm run dev
```

## Build

```bash
npm run build    # Production build
npm run preview  # Preview production build locally
```

Output: `dist/`

