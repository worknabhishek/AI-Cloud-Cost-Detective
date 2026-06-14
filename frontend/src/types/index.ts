// Scan schemas
export type EC2Instance = {
  instance_id: string
  instance_type: string
  state: string
  region: string
  availability_zone: string
  launch_time?: string | null
  private_ip_address?: string | null
  public_ip_address?: string | null
  tags: Record<string, string>
}

export type EBSVolume = {
  volume_id: string
  size_gb: number
  volume_type: string
  state: string
  region: string
  availability_zone: string
  encrypted: boolean
  attached_instance_id?: string | null
  tags: Record<string, string>
}

export type ElasticIP = {
  allocation_id?: string | null
  public_ip: string
  domain: string
  association_id?: string | null
  instance_id?: string | null
  network_interface_id?: string | null
  region: string
  tags: Record<string, string>
}

export type ScanResources = {
  ec2_instances: EC2Instance[]
  ebs_volumes: EBSVolume[]
  elastic_ips: ElasticIP[]
}

export type ScanSummary = {
  ec2_instance_count: number
  ebs_volume_count: number
  elastic_ip_count: number
  total_resources: number
}

export type ScanResponse = {
  account_id: string
  region: string
  summary: ScanSummary
  resources: ScanResources
  scanned_at: string
}

// Health
export type HealthResponse = {
  status: string
  service: string
}

// Analyze schemas
export type AWSResource = {
  resource_id: string
  resource_type: string
  region: string
  tags: Record<string, string>
  metadata: Record<string, any>
}

export type AnalyzeRequest = {
  account_id: string
  resources: AWSResource[]
}

export type CostFinding = {
  resource_id: string
  category: string
  severity: 'low' | 'medium' | 'high' | string
  title: string
  description: string
  estimated_monthly_savings_usd: number
}

export type CostSummary = {
  total_estimated_monthly_cost_usd: number
  total_potential_savings_usd: number
  resources_analyzed: number
  findings_count: number
}

export type AnalyzeResponse = {
  account_id: string
  summary: CostSummary
  findings: CostFinding[]
  report_generated_at: string
}

// AI analyze schemas
export type OptimizationRecommendation = {
  resource_id: string
  resource_type: string
  title: string
  recommendation: string
  estimated_monthly_savings_usd: number
  remediation_commands: string[]
}

export type AIAnalyzeRequest = {
  account_id: string
  region: string
  resources: ScanResources
}

export type AIAnalyzeResponse = {
  account_id: string
  region: string
  summary: string
  total_estimated_monthly_savings_usd: number
  recommendations: OptimizationRecommendation[]
  analyzed_at: string
  model: string
}
