import api from '../api/client'
import type {
  ScanResponse,
  AnalyzeRequest,
  AnalyzeResponse,
  AIAnalyzeRequest,
  AIAnalyzeResponse,
  HealthResponse,
} from '../types'

export async function fetchScan(region = 'us-east-1') {
  return api.get<ScanResponse>(`/scan`, { params: { region } })
}

export async function fetchHealth() {
  return api.get<HealthResponse>(`/health`)
}

export async function postAnalyze(request: AnalyzeRequest) {
  return api.post<AnalyzeResponse>(`/analyze`, request)
}

export async function postAIAnalyze(request: AIAnalyzeRequest) {
  return api.post<AIAnalyzeResponse>(`/ai-analyze`, request)
}
