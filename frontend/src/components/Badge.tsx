import React from 'react'

export default function Badge({ children, tone = 'muted' }: { children: React.ReactNode, tone?: 'muted'|'success'|'danger'|'accent' }){
  const bg = tone === 'success' ? 'rgba(34,197,94,0.12)' : tone === 'danger' ? 'rgba(239,68,68,0.08)' : tone === 'accent' ? 'rgba(124,58,237,0.08)' : 'rgba(255,255,255,0.03)'
  const color = tone === 'danger' ? '#f87171' : tone === 'success' ? '#22c55e' : tone === 'accent' ? 'var(--accent)' : 'var(--muted)'
  return (
    <span style={{display:'inline-block', padding:'4px 8px', borderRadius:999, background:bg, color, fontSize:12}}>{children}</span>
  )
}
