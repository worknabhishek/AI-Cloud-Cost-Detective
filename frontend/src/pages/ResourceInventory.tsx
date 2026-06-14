import React, { useEffect, useState } from 'react'
import { fetchScan } from '../services/apiService'
import type { ScanResponse, EC2Instance, EBSVolume, ElasticIP } from '../types'
import Loading from '../components/Loading'
import Empty from '../components/Empty'
import Badge from '../components/Badge'

export default function ResourceInventory(){
  const [scan, setScan] = useState<ScanResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')

  useEffect(()=>{
    let mounted = true
    fetchScan().then(r=>{ if(mounted) setScan(r.data) }).catch(()=>{ if(mounted) setScan(null) }).finally(()=>{ if(mounted) setLoading(false) })
    return ()=>{ mounted = false }
  },[])

  if(loading) return <Loading />

  if(!scan) return <Empty title="No resources" subtitle="Scan returned no data or the backend is unavailable." />

  const ec2 = scan.resources.ec2_instances as EC2Instance[]
  const ebs = scan.resources.ebs_volumes as EBSVolume[]
  const eips = scan.resources.elastic_ips as ElasticIP[]

  const filterFn = (s: string) => s.toLowerCase().includes(query.toLowerCase())

  const filteredEc2 = ec2.filter(i => filterFn(i.instance_id) || filterFn(i.instance_type) || filterFn(i.state) || filterFn(i.region))
  const filteredEbs = ebs.filter(v => filterFn(v.volume_id) || filterFn(String(v.size_gb)) || filterFn(v.state) || filterFn(v.region))
  const filteredEips = eips.filter(e => filterFn(e.public_ip) || filterFn(e.allocation_id ?? '') || filterFn(e.region))

  return (
    <div>
      <h1>Resource Inventory</h1>

      <div style={{display:'flex', gap:12, marginBottom:12}}>
        <input placeholder="Search resources..." value={query} onChange={e=>setQuery(e.target.value)} style={{flex:1, padding:8, borderRadius:8, border:'1px solid rgba(255,255,255,0.04)', background:'transparent', color:'var(--text)'}} />
      </div>

      <div className="card">
        <h3>EC2 Instances</h3>
        {filteredEc2.length===0 ? <Empty title="No EC2 instances"/> : (
          <table style={{width:'100%'}}>
            <thead><tr><th>Instance</th><th>Type</th><th>AZ</th><th>State</th></tr></thead>
            <tbody>
              {filteredEc2.map(i=> (
                <tr key={i.instance_id}>
                  <td>{i.instance_id}</td>
                  <td>{i.instance_type}</td>
                  <td>{i.availability_zone}</td>
                  <td><Badge tone={i.state==='running' ? 'success' : 'muted'}>{i.state}</Badge></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h3>EBS Volumes</h3>
        {filteredEbs.length===0 ? <Empty title="No EBS volumes"/> : (
          <table style={{width:'100%'}}>
            <thead><tr><th>Volume</th><th>Size (GiB)</th><th>Type</th><th>State</th></tr></thead>
            <tbody>
              {filteredEbs.map(v=> (
                <tr key={v.volume_id}>
                  <td>{v.volume_id}</td>
                  <td>{v.size_gb}</td>
                  <td>{v.volume_type}</td>
                  <td><Badge tone={v.state==='in-use' ? 'success' : 'muted'}>{v.state}</Badge></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h3>Elastic IPs</h3>
        {filteredEips.length===0 ? <Empty title="No Elastic IPs"/> : (
          <table style={{width:'100%'}}>
            <thead><tr><th>Public IP</th><th>Allocation</th><th>Associated</th><th>Domain</th></tr></thead>
            <tbody>
              {filteredEips.map(e=> (
                <tr key={(e.allocation_id||e.public_ip)}>
                  <td>{e.public_ip}</td>
                  <td>{e.allocation_id ?? '-'}</td>
                  <td>{e.instance_id ? <Badge tone="success">attached</Badge> : <Badge>free</Badge>}</td>
                  <td>{e.domain}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
