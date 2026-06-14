import React, { useEffect, useState } from 'react'
import { fetchScan, postAIAnalyze, postAnalyze } from '../services/apiService'
import type { AIAnalyzeResponse, AIAnalyzeRequest, AnalyzeResponse } from '../types'
import Loading from '../components/Loading'
import Expander from '../components/Expander'
import Empty from '../components/Empty'

export default function AIRecommendations(){
  const [analysis, setAnalysis] = useState<AIAnalyzeResponse | null>(null)
  const [fallback, setFallback] = useState<AnalyzeResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string|null>(null)
  const [aiUnavailable, setAiUnavailable] = useState(false)

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{
        const scanRes = await fetchScan()
        if(!mounted) return
        // backend requires at least one resource; skip if empty
        const resourceCount = scanRes.data.resources.ec2_instances.length + scanRes.data.resources.ebs_volumes.length + scanRes.data.resources.elastic_ips.length
        if(resourceCount === 0){ setLoading(false); return }

        // Try AI analysis first
        try{
          const req: AIAnalyzeRequest = { account_id: scanRes.data.account_id, region: scanRes.data.region, resources: scanRes.data.resources }
          const ai = await postAIAnalyze(req)
          if(!mounted) return
          setAnalysis(ai.data)
        }catch(aiErr:any){
          // If AI is unavailable (503), fall back to rule-based recommendations
          if(aiErr?.response?.status === 503 || aiErr?.response?.status === 502){
            setAiUnavailable(true)
            // Fall back to rule-based cost analysis
            const payload = mapScanToAnalyzeRequest(scanRes.data)
            if(payload.resources.length > 0){
              const analyzeRes = await postAnalyze(payload)
              if(!mounted) return
              setFallback(analyzeRes.data)
            }
          }else{
            throw aiErr
          }
        }
      }catch(e:any){
        setError(String(e?.message || e))
      }finally{ setLoading(false) }
    }
    load()
    return ()=>{ mounted = false }
  },[])

  if(loading) return <Loading />
  if(error) return <div className="card">Error: {error}</div>

  // If AI is unavailable, show fallback rule-based recommendations
  if(aiUnavailable && fallback){
    return (
      <div>
        <h1>AI Recommendations</h1>
        <div className="card" style={{background:'rgba(239,68,68,0.08)', borderLeft:'3px solid #ef4444', padding:12}}>
          <div style={{fontWeight:600, color:'#f87171'}}>AI Analysis Unavailable</div>
          <div style={{color:'var(--muted)', marginTop:8}}>
            AI-powered recommendations are currently unavailable. Configure OPENAI_API_KEY on your backend to enable AI analysis.
            Showing rule-based cost recommendations instead.
          </div>
        </div>

        <div style={{marginTop:16}}>
          <h2>Rule-Based Recommendations</h2>
          <div className="card">
            <div>Total savings opportunity: ${fallback.summary.total_potential_savings_usd.toFixed(2)}/month</div>
            <div style={{color:'var(--muted)'}}>Findings: {fallback.summary.findings_count}</div>
          </div>

          <div style={{display:'grid', gap:12, marginTop:12}}>
            {fallback.findings.map((f,idx)=> (
              <div key={idx} className="card">
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'start'}}>
                  <div style={{flex:1}}>
                    <div style={{fontWeight:700}}>{f.title}</div>
                    <div style={{color:'var(--muted)', fontSize:12, marginTop:4}}>Resource: {f.resource_id}</div>
                  </div>
                  <div style={{textAlign:'right', marginLeft:12}}>
                    <div style={{fontSize:16, fontWeight:700}}>${f.estimated_monthly_savings_usd.toFixed(2)}</div>
                    <div style={{fontSize:11, color:'var(--muted)'}}>Severity: {f.severity}</div>
                  </div>
                </div>
                <div style={{marginTop:8, color:'var(--muted)'}}>{f.description}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if(!analysis) return <Empty title="No AI analysis" subtitle="No recommendations were returned." />

  return (
    <div>
      <h1>AI Recommendations</h1>
      <div className="card">
        <h3>Summary</h3>
        <div style={{color:'var(--muted)'}}>{analysis.summary}</div>
        <div style={{marginTop:8}}>Estimated savings: ${analysis.total_estimated_monthly_savings_usd.toFixed(2)}/month</div>
        <div style={{color:'var(--muted)', fontSize:12, marginTop:4}}>Model: {analysis.model}</div>
      </div>

      <div style={{display:'grid', gap:12, marginTop:12}}>
        {analysis.recommendations.map((r,idx)=> (
          <Expander key={idx} title={`${r.title} — $${r.estimated_monthly_savings_usd.toFixed(2)}`}>
            <div style={{marginBottom:8}}>{r.recommendation}</div>
            <div style={{color:'var(--muted)'}}>Resource: {r.resource_id} ({r.resource_type})</div>
            <div style={{marginTop:8}}>
              <strong>Remediation commands</strong>
              <pre style={{marginTop:8, background:'rgba(255,255,255,0.02)', padding:8, borderRadius:6, overflow:'auto'}}>{r.remediation_commands.join('\n')}</pre>
            </div>
          </Expander>
        ))}
      </div>
    </div>
  )
}

function mapScanToAnalyzeRequest(scan: any){
  const resources: any[] = []
  for(const i of scan.resources.ec2_instances){
    resources.push({
      resource_id: i.instance_id,
      resource_type: 'ec2',
      region: i.region,
      tags: i.tags || {},
      metadata: { 
        instance_type: i.instance_type, 
        state: i.state,
        availability_zone: i.availability_zone,
        launch_time: i.launch_time,
        private_ip_address: i.private_ip_address,
        public_ip_address: i.public_ip_address,
      }
    })
  }
  for(const v of scan.resources.ebs_volumes){
    resources.push({
      resource_id: v.volume_id,
      resource_type: 'ebs',
      region: v.region,
      tags: v.tags || {},
      metadata: { 
        size_gb: v.size_gb, 
        volume_type: v.volume_type, 
        state: v.state,
        attached_instance_id: v.attached_instance_id,
        encrypted: v.encrypted,
      }
    })
  }
  for(const e of scan.resources.elastic_ips){
    resources.push({
      resource_id: e.allocation_id || e.public_ip,
      resource_type: 'elastic_ip',
      region: e.region,
      tags: e.tags || {},
      metadata: { 
        public_ip: e.public_ip, 
        association_id: e.association_id, 
        instance_id: e.instance_id,
        network_interface_id: e.network_interface_id,
      }
    })
  }
  return { account_id: scan.account_id, resources }
}
