import React from 'react'

export default function Empty({ title, subtitle }: { title: string, subtitle?: string }){
  return (
    <div style={{padding:24, textAlign:'center', color:'var(--muted)'}}>
      <h3 style={{margin:0, color:'var(--text)'}}>{title}</h3>
      {subtitle && <div style={{marginTop:8}}>{subtitle}</div>}
    </div>
  )
}
