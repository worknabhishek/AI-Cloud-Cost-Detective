import React, { useState } from 'react'

export default function Expander({ title, children }: { title: React.ReactNode, children: React.ReactNode }){
  const [open, setOpen] = useState(false)
  return (
    <div className="card" style={{padding:12}}>
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <div style={{fontWeight:600}}>{title}</div>
        <button onClick={()=>setOpen(v=>!v)} style={{background:'transparent', border:'none', color:'var(--muted)'}}>{open? 'Collapse' : 'Expand'}</button>
      </div>
      {open && <div style={{marginTop:12}}>{children}</div>}
    </div>
  )
}
