import React from 'react'

export default function Loading({ text = 'Loading...' }: { text?: string }){
  return (
    <div style={{padding:20, textAlign:'center', color:'var(--muted)'}}>
      <div style={{height:36, display:'flex', alignItems:'center', justifyContent:'center'}}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="10" stroke="rgba(255,255,255,0.06)" strokeWidth="4" />
          <path d="M22 12a10 10 0 00-10-10" stroke="var(--accent)" strokeWidth="4" strokeLinecap="round"/>
        </svg>
      </div>
      <div style={{marginTop:8}}>{text}</div>
    </div>
  )
}
