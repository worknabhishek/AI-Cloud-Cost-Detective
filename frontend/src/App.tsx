import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import ResourceInventory from './pages/ResourceInventory'
import CostAnalysis from './pages/CostAnalysis'
import AIRecommendations from './pages/AIRecommendations'
import Layout from './components/Layout'

export default function App(){
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard/>} />
        <Route path="/inventory" element={<ResourceInventory/>} />
        <Route path="/costs" element={<CostAnalysis/>} />
        <Route path="/recommendations" element={<AIRecommendations/>} />
      </Routes>
    </Layout>
  )
}
