import React from 'react';
import { Ship, TrendingUp, Navigation } from 'lucide-react';

export default function DecisionSummaryBar({ vesselResult, freightState, routeState, activeTab, setActiveTab }) {
  // 1. Vessel Value
  const vesselValue = vesselResult?.recommended_vessel
    ? vesselResult.recommended_vessel.toUpperCase()
    : 'READY FOR INPUT';

  // 2. Freight Value
  let freightValue = 'READY FOR ANALYSIS';
  let isFreightCalculated = false;
  if (freightState && !freightState.pending && freightState.data?.forecast_rate) {
    freightValue = `$${freightState.data.forecast_rate.toFixed(2)} / MT`;
    isFreightCalculated = true;
  }

  // 3. Trade Route Value
  let routeValue = 'READY FOR OPTIMIZATION';
  let hasRouteData = false;
  if (routeState && !routeState.pending) {
    const routeArray = routeState.data?.recommended_route || routeState.data?.waypoints;
    if (routeArray && routeArray.length > 0) {
      routeValue = routeArray.join(' → ');
      hasRouteData = true;
    } else if (routeState.data && !routeState.data.route_feasible) {
      routeValue = 'ROUTE INFEASIBLE';
      hasRouteData = true;
    } else if (routeState.error) {
      routeValue = 'OPTIMIZATION ERROR';
    }
  }

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '1.25rem',
        marginBottom: '1.75rem'
      }}
    >
      {/* 01 VESSEL INTELLIGENCE */}
      <div
        onClick={() => setActiveTab && setActiveTab('vessel')}
        style={{
          background: 'var(--surface-primary)',
          border: activeTab === 'vessel' ? '1px solid var(--accent-amber)' : '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.2rem 1.35rem',
          boxShadow: activeTab === 'vessel' ? '0 0 0 1px var(--accent-amber)' : 'var(--shadow-flat)',
          position: 'relative',
          overflow: 'hidden',
          cursor: 'pointer',
          transition: 'all 0.2s ease'
        }}
      >
        {activeTab === 'vessel' && (
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              bottom: 0,
              width: '3px',
              background: 'var(--accent-amber)'
            }}
          />
        )}

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.6rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 900, fontFamily: 'var(--font-mono)', color: 'var(--accent-amber)' }}>01</span>
            <span style={{ fontSize: '0.725rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
              VESSEL INTELLIGENCE
            </span>
          </div>

          <span
            style={{
              fontSize: '0.65rem',
              fontWeight: 800,
              padding: '0.15rem 0.5rem',
              borderRadius: 'var(--radius-full)',
              background: 'rgba(245, 185, 66, 0.1)',
              border: '1px solid rgba(245, 185, 66, 0.25)',
              color: 'var(--accent-amber)',
              letterSpacing: '0.04em'
            }}
          >
            REAL MODEL
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.35rem' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              background: 'rgba(245, 185, 66, 0.1)',
              border: '1px solid rgba(245, 185, 66, 0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--accent-amber)'
            }}
          >
            <Ship size={18} />
          </div>
          <div>
            <div style={{ fontSize: '1.05rem', fontWeight: 900, color: vesselResult?.recommended_vessel ? 'var(--accent-amber)' : 'var(--text-primary)', letterSpacing: '-0.01em' }}>
              {vesselValue}
            </div>
          </div>
        </div>
      </div>

      {/* 02 FREIGHT INTELLIGENCE */}
      <div
        onClick={() => setActiveTab && setActiveTab('freight')}
        style={{
          background: 'var(--surface-primary)',
          border: activeTab === 'freight' ? '1px solid var(--accent-amber)' : '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.2rem 1.35rem',
          boxShadow: activeTab === 'freight' ? '0 0 0 1px var(--accent-amber)' : 'var(--shadow-flat)',
          position: 'relative',
          overflow: 'hidden',
          cursor: 'pointer',
          transition: 'all 0.2s ease'
        }}
      >
        {activeTab === 'freight' && (
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              bottom: 0,
              width: '3px',
              background: 'var(--accent-amber)'
            }}
          />
        )}

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.6rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 900, fontFamily: 'var(--font-mono)', color: 'var(--accent-amber)' }}>02</span>
            <span style={{ fontSize: '0.725rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
              FREIGHT INTELLIGENCE
            </span>
          </div>

          <span
            style={{
              fontSize: '0.65rem',
              fontWeight: 800,
              padding: '0.15rem 0.5rem',
              borderRadius: 'var(--radius-full)',
              background: 'rgba(245, 185, 66, 0.1)',
              border: '1px solid rgba(245, 185, 66, 0.25)',
              color: 'var(--accent-amber)',
              letterSpacing: '0.04em'
            }}
          >
            REAL MODEL
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.35rem' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              background: 'rgba(245, 185, 66, 0.1)',
              border: '1px solid rgba(245, 185, 66, 0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--accent-amber)'
            }}
          >
            <TrendingUp size={18} />
          </div>
          <div>
            <div style={{ fontSize: isFreightCalculated ? '1.05rem' : '0.85rem', fontWeight: 900, color: isFreightCalculated ? 'var(--accent-amber)' : 'var(--text-primary)', letterSpacing: isFreightCalculated ? '-0.01em' : 'normal' }}>
              {freightValue}
            </div>
          </div>
        </div>
      </div>

      {/* 03 TRADE ROUTE INTELLIGENCE */}
      <div
        onClick={() => setActiveTab && setActiveTab('freight')}
        style={{
          background: 'var(--surface-primary)',
          border: activeTab === 'freight' ? '1px solid var(--accent-amber)' : '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.2rem 1.35rem',
          boxShadow: activeTab === 'freight' ? '0 0 0 1px var(--accent-amber)' : 'var(--shadow-flat)',
          position: 'relative',
          overflow: 'hidden',
          cursor: 'pointer',
          transition: 'all 0.2s ease'
        }}
      >
        {activeTab === 'freight' && (
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              bottom: 0,
              width: '3px',
              background: 'var(--accent-amber)'
            }}
          />
        )}

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.6rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 900, fontFamily: 'var(--font-mono)', color: 'var(--accent-amber)' }}>03</span>
            <span style={{ fontSize: '0.725rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
              TRADE ROUTE INTELLIGENCE
            </span>
          </div>

          <span
            style={{
              fontSize: '0.65rem',
              fontWeight: 800,
              padding: '0.15rem 0.5rem',
              borderRadius: 'var(--radius-full)',
              background: 'rgba(245, 185, 66, 0.1)',
              border: '1px solid rgba(245, 185, 66, 0.25)',
              color: 'var(--accent-amber)',
              letterSpacing: '0.04em'
            }}
          >
            ROUTE ENGINE READY
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.35rem' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              background: 'rgba(245, 185, 66, 0.1)',
              border: '1px solid rgba(245, 185, 66, 0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--accent-amber)'
            }}
          >
            <Navigation size={18} />
          </div>
          <div>
            <div style={{ fontSize: hasRouteData ? '0.95rem' : '0.85rem', fontWeight: 900, color: hasRouteData ? 'var(--accent-amber)' : 'var(--text-primary)', letterSpacing: hasRouteData ? '-0.01em' : 'normal' }}>
              {routeValue}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}




