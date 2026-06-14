import React from 'react'
import { NavLink } from 'react-router-dom'

export default function Layout({ children }: { children: React.ReactNode }){
  return (
    <div style={{display:'flex', minHeight:'100vh'}}>
      <aside className="sidebar">
        <h3>Cloud Cost Detective</h3>
        <nav style={{marginTop:16}}>
          <NavLink to="/" className={({isActive}) => "link" + (isActive?" active":"")}>Dashboard</NavLink>
          <NavLink to="/inventory" className={({isActive}) => "link" + (isActive?" active":"")}>Resource Inventory</NavLink>
          <NavLink to="/costs" className={({isActive}) => "link" + (isActive?" active":"")}>Cost Analysis</NavLink>
          <NavLink to="/recommendations" className={({isActive}) => "link" + (isActive?" active":"")}>AI Recommendations</NavLink>
        </nav>
      </aside>
      <main className="main">
        <div className="header">
          <div className="nav">
            <h2>Workspace</h2>
          </div>
        </div>
        <div className="container">
          {children}
        </div>
      </main>
    </div>
  )
}
