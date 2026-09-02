import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HeroBanner from './components/HeroBanner';
import TabNavigation from './components/TabNavigation';
import DecisionSummaryBar from './components/DecisionSummaryBar';
import VesselIntelligence from './pages/VesselIntelligence';
import FreightRouteIntelligence from './pages/FreightRouteIntelligence';
import { checkBackendHealth } from './services/api';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('vessel');
  const [isBackendOnline, setIsBackendOnline] = useState(false);

  // Shared state for Decision Summary Bar
  const [vesselResult, setVesselResult] = useState(null);
  const [freightState, setFreightState] = useState(null);
  const [routeState, setRouteState] = useState(null);

  useEffect(() => {
    async function verifyHealth() {
      const health = await checkBackendHealth();
      setIsBackendOnline(health.online);
    }
    verifyHealth();
    
    // Periodically re-check health every 15 seconds
    const interval = setInterval(verifyHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-container">
      {/* Header Bar */}
      <Header isBackendOnline={isBackendOnline} />

      {/* Hero / Intro Banner */}
      <HeroBanner />

      {/* Decision Summary Strip */}
      <DecisionSummaryBar
        vesselResult={vesselResult}
        freightState={freightState}
        routeState={routeState}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {/* Primary Tab Navigation */}
      <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main View Area */}
      <main style={{ transition: 'opacity 0.25s ease-in-out' }}>
        {activeTab === 'vessel' && (
          <VesselIntelligence onVesselResultChange={setVesselResult} />
        )}
        {activeTab === 'freight' && (
          <FreightRouteIntelligence
            onFreightStateChange={setFreightState}
            onRouteStateChange={setRouteState}
          />
        )}
      </main>

      {/* Footer */}
      <footer
        style={{
          marginTop: '4rem',
          paddingTop: '1.75rem',
          borderTop: '1px solid rgba(255, 255, 255, 0.08)',
          textAlign: 'center',
          fontSize: '0.8rem',
          color: 'var(--text-muted)'
        }}
      >
        <p>CHARTER CAST &bull; AI-Powered Freight & Vessel Intelligence &bull; Decision Support System</p>
      </footer>
    </div>
  );
}
