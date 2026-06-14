import React, { useEffect, useState } from 'react'
import Loading from '../components/Loading'
import Empty from '../components/Empty'
import Badge from '../components/Badge'
import { fetchScan, postAnalyze } from '../services/apiService'
import type { ScanResponse, AnalyzeResponse, CostFinding } from '../types'

export default function CostAnalysis(){
  const [scan, setScan] = useState<ScanResponse | null>(null)
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{
        const scanRes = await fetchScan()
        if(!mounted) return
        setScan(scanRes.data)

        const payload = mapScanToAnalyzeRequest(scanRes.data)
        // backend requires min_length=1 for resources array
        if(payload.resources.length > 0){
          const analyzeRes = await postAnalyze(payload)
          setAnalysis(analyzeRes.data)
        }
      }catch(e:any){
        setError(String(e?.message || e))
      }finally{
        setLoading(false)
      }
    }
    load()
    return ()=>{ mounted = false }
  },[])

  if(loading) return <Loading />
  if(error) return <div className="card">Error: {error}</div>
  if(!analysis) return <Empty title="No analysis" subtitle="No findings were returned." />

  // Group findings by category
  const costOptimizationFindings = analysis.findings.filter(f => f.category === 'cost_optimization')
  const governanceFindings = analysis.findings.filter(f => f.category === 'governance')
  const otherFindings = analysis.findings.filter(f => f.category !== 'cost_optimization' && f.category !== 'governance')

  const severityToTone = (sev: string) => {
    const s = sev?.toLowerCase() || 'low'
    return s === 'high' ? 'danger' : s === 'medium' ? 'accent' : 'muted'
  }

  return (
    <div>
      <h1>Cost Analysis</h1>

      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:12, marginBottom:16}}>
        <div className="card">
          <h3>Total Monthly Savings</h3>
          <div style={{fontSize:32, fontWeight:700, color:'var(--accent)'}}>
            ${analysis.summary.total_potential_savings_usd.toFixed(2)}
          </div>
          <div style={{color:'var(--muted)', fontSize:12, marginTop:4}}>
            {analysis.summary.findings_count} findings across {analysis.summary.resources_analyzed} resources
          </div>
        </div>
        <div className="card">
          <h3>Estimated Monthly Cost</h3>
          <div style={{fontSize:32, fontWeight:700}}>
            ${analysis.summary.total_estimated_monthly_cost_usd.toFixed(2)}
          </div>
          <div style={{color:'var(--muted)', fontSize:12, marginTop:4}}>
            Cost without optimizations
          </div>
        </div>
      </div>

      {costOptimizationFindings.length > 0 && (
        <div>
          <h2 style={{fontSize:18, marginTop:20, marginBottom:12}}>Cost Optimization Opportunities</h2>
          <div style={{display:'grid', gap:12}}>
            {costOptimizationFindings.map((f: CostFinding, idx)=> (
              <div key={idx} className="card">
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'start', gap:12}}>
                  <div style={{flex:1}}>
                    <div style={{display:'flex', gap:8, alignItems:'center', marginBottom:8}}>
                      <span style={{fontWeight:700}}>{f.title}</span>
                      <Badge tone={severityToTone(f.severity)}>{f.severity}</Badge>
                    </div>
                    <div style={{color:'var(--muted)', fontSize:12}}>Resource: {f.resource_id}</div>
                    <div style={{marginTop:8, color:'var(--muted)'}}>{f.description}</div>
                  </div>
                  <div style={{textAlign:'right', whiteSpace:'nowrap'}}>
                    <div style={{fontSize:20, fontWeight:700, color:'#22c55e'}}>
                      ${f.estimated_monthly_savings_usd.toFixed(2)}
                    </div>
                    <div style={{fontSize:11, color:'var(--muted)'}}>monthly savings</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {governanceFindings.length > 0 && (
        <div>
          <h2 style={{fontSize:18, marginTop:20, marginBottom:12}}>Governance & Compliance</h2>
          <div style={{display:'grid', gap:12}}>
            {governanceFindings.map((f: CostFinding, idx)=> (
              <div key={idx} className="card">
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'start', gap:12}}>
                  <div style={{flex:1}}>
                    <div style={{display:'flex', gap:8, alignItems:'center', marginBottom:8}}>
                      <span style={{fontWeight:700}}>{f.title}</span>
                      <Badge tone={severityToTone(f.severity)}>{f.severity}</Badge>
                    </div>
                    <div style={{color:'var(--muted)', fontSize:12}}>Resource: {f.resource_id}</div>
                    <div style={{marginTop:8, color:'var(--muted)'}}>{f.description}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {otherFindings.length > 0 && (
        <div>
          <h2 style={{fontSize:18, marginTop:20, marginBottom:12}}>Other Findings</h2>
          <div style={{display:'grid', gap:12}}>
            {otherFindings.map((f: CostFinding, idx)=> (
              <div key={idx} className="card">
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'start', gap:12}}>
                  <div style={{flex:1}}>
                    <div style={{display:'flex', gap:8, alignItems:'center', marginBottom:8}}>
                      <span style={{fontWeight:700}}>{f.title}</span>
                      <Badge tone={severityToTone(f.severity)}>{f.severity}</Badge>
                    </div>
                    <div style={{color:'var(--muted)', fontSize:12}}>Resource: {f.resource_id}</div>
                    <div style={{marginTop:8, color:'var(--muted)'}}>{f.description}</div>
                  </div>
                  {f.estimated_monthly_savings_usd > 0 && (
                    <div style={{textAlign:'right', whiteSpace:'nowrap'}}>
                      <div style={{fontSize:16, fontWeight:700, color:'#22c55e'}}>
                        ${f.estimated_monthly_savings_usd.toFixed(2)}
                      </div>
                      <div style={{fontSize:11, color:'var(--muted)'}}>savings</div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function mapScanToAnalyzeRequest(scan: ScanResponse){
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
