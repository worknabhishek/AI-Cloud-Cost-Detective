import React, { useEffect, useState } from 'react'
import { fetchScan, fetchHealth, postAnalyze } from '../services/apiService'
import type { ScanResponse, AnalyzeResponse, HealthResponse } from '../types'
import Loading from '../components/Loading'

export default function Dashboard(){
  const [scan, setScan] = useState<ScanResponse | null>(null)
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{
        const scanRes = await fetchScan()
        if(!mounted) return
        setScan(scanRes.data)

        const healthRes = await fetchHealth()
        setHealth(healthRes.data)

        // prepare analyze request by mapping scanned resources
        // backend requires min_length=1, so only POST if we have resources
        const payload = mapScanToAnalyzeRequest(scanRes.data)
        if(payload.resources.length > 0){
          const analyzeRes = await postAnalyze(payload)
          setAnalysis(analyzeRes.data)
        }
      }catch(e){
        // ignore here; pages show empty states
      }finally{
        setLoading(false)
      }
    }
    load()
    return ()=>{ mounted = false }
  },[])

  if(loading) return <Loading />

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="card" style={{display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:12}}>
        <div>
          <h4>Account</h4>
          <div>{scan?.account_id ?? '—'}</div>
        </div>
        <div>
          <h4>Region</h4>
          <div>{scan?.region ?? '—'}</div>
        </div>
        <div>
          <h4>Backend Health</h4>
          <div>{health?.status ?? 'unknown'}</div>
        </div>
      </div>

      <div style={{marginTop:16, display:'grid', gridTemplateColumns:'1fr 1fr', gap:12}}>
        <div className="card">
          <h3>Total Resources</h3>
          <div style={{fontSize:28, marginTop:8}}>{scan?.summary.total_resources ?? 0}</div>
        </div>
        <div className="card">
          <h3>Findings</h3>
          <div style={{fontSize:28, marginTop:8}}>{analysis ? analysis.summary.findings_count : '—'}</div>
          <div style={{marginTop:8}}>Estimated savings: {analysis ? `$${analysis.summary.total_potential_savings_usd.toFixed(2)}` : '—'}</div>
        </div>
      </div>
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
      }
    })
  }
  return { account_id: scan.account_id, resources }
}
