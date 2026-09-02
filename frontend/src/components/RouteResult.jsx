import React from 'react';
import { Navigation, ArrowRight, Anchor, MapPin, AlertCircle, CheckCircle, Compass, ShieldAlert, Cpu, Ship } from 'lucide-react';

export default function RouteResult({ routeState }) {
  if (!routeState) return null;

  // Case A: Model Connection Pending / Loading
  if (routeState.pending) {
    return (
      <div className="pending-card" style={{ marginTop: '1.5rem' }}>
        <div className="pending-icon-wrapper">
          <Navigation size={24} />
        </div>
        <span className="pending-badge">CONNECTING ROUTE ENGINE</span>
        <div className="pending-title">TRADE ROUTE OPTIMIZATION</div>
        <div className="pending-sub">
          {routeState.message || 'Optimizing passage routing using Constraint-Aware A* Route Engine...'}
        </div>
      </div>
    );
  }

  // Case B: Error Response
  if (routeState.error && !routeState.data) {
    return (
      <div className="panel-primary" style={{ padding: '1.75rem 1.6rem', marginTop: '1.5rem', border: '1px solid rgba(255, 77, 109, 0.3)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span className="tag-pill" style={{ background: 'rgba(255, 77, 109, 0.15)', color: 'var(--accent-danger)', border: '1px solid rgba(255, 77, 109, 0.3)' }}>
              <ShieldAlert size={12} />
              ROUTE ERROR
            </span>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              TRADE ROUTE ENGINE ERROR
            </h3>
          </div>
        </div>

        <div
          style={{
            padding: '1.25rem 1.4rem',
            background: 'rgba(255, 77, 109, 0.08)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid rgba(255, 77, 109, 0.2)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.85rem'
          }}
        >
          <AlertCircle size={20} color="var(--accent-danger)" style={{ flexShrink: 0 }} />
          <div>
            <div style={{ fontSize: '0.9rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              Unable to Optimize Route
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              {routeState.error}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Case C: Trade Route Result
  const { data } = routeState;
  if (!data) return null;

  const isFeasible = data.route_feasible;
  const engineName = data.engine_name || 'Constraint-Aware A* Route Engine';
  const vesselClass = data.vessel_class;
  const distance = data.distance_nm;
  const waypoints = data.recommended_route || data.waypoints || [data.origin, data.destination].filter(Boolean);

  // Infeasible Route Response
  if (!isFeasible) {
    return (
      <div className="panel-primary" style={{ padding: '1.75rem 1.6rem', marginTop: '1.5rem', border: '1px solid rgba(255, 77, 109, 0.3)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span className="tag-pill" style={{ background: 'rgba(255, 77, 109, 0.15)', color: 'var(--accent-danger)', border: '1px solid rgba(255, 77, 109, 0.3)' }}>
              <ShieldAlert size={12} />
              INFEASIBLE ROUTE
            </span>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              TRADE ROUTE CONSTRAINTS
            </h3>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <Cpu size={13} color="var(--accent-amber)" />
            {engineName}
          </span>
        </div>

        <div
          style={{
            padding: '1.25rem 1.4rem',
            background: 'rgba(255, 77, 109, 0.08)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid rgba(255, 77, 109, 0.2)',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.85rem'
          }}
        >
          <AlertCircle size={20} color="var(--accent-danger)" style={{ marginTop: '0.1rem', flexShrink: 0 }} />
          <div>
            <div style={{ fontSize: '0.9rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              Route Restriction Detected ({vesselClass || 'Selected Vessel'})
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.35rem', lineHeight: '1.45' }}>
              {data.reason || 'The requested route violates vessel draft capabilities or chokepoint navigation rules.'}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Feasible Route Response
  return (
    <div className="panel-primary" style={{ padding: '1.75rem 1.6rem', marginTop: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <span className="tag-pill tag-ai">
            <CheckCircle size={12} />
            ROUTE FEASIBLE
          </span>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            OPTIMIZED PASSAGE ROUTE
          </h3>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', flexWrap: 'wrap' }}>
          {distance != null && (
            <span style={{ fontSize: '0.825rem', fontWeight: 800, color: 'var(--accent-amber)', background: 'rgba(245, 185, 66, 0.1)', padding: '0.3rem 0.65rem', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(245, 185, 66, 0.25)' }}>
              <Compass size={13} style={{ display: 'inline', marginRight: '0.35rem' }} />
              {distance.toLocaleString()} NM
            </span>
          )}
          {vesselClass && (
            <span style={{ fontSize: '0.775rem', color: 'var(--text-primary)', fontWeight: 700, background: 'var(--surface-secondary)', padding: '0.3rem 0.65rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <Ship size={13} color="var(--accent-amber)" />
              {vesselClass}
            </span>
          )}
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <Cpu size={13} color="var(--accent-amber)" />
            {engineName}
          </span>
        </div>
      </div>

      {/* Dynamic Waypoint Path Flow */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem',
          background: 'var(--surface-secondary)',
          padding: '1.25rem 1.4rem',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)'
        }}
      >
        {waypoints.map((pt, idx) => (
          <React.Fragment key={idx}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
              <div
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: idx === 0 || idx === waypoints.length - 1 ? 'rgba(245, 185, 66, 0.15)' : 'rgba(76, 141, 170, 0.15)',
                  border: '1px solid rgba(245, 185, 66, 0.3)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--accent-amber)'
                }}
              >
                {idx === 0 ? <Anchor size={16} /> : idx === waypoints.length - 1 ? <MapPin size={16} /> : <Navigation size={16} />}
              </div>
              <div>
                <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 800, letterSpacing: '0.04em' }}>
                  {idx === 0 ? 'ORIGIN' : idx === waypoints.length - 1 ? 'DESTINATION' : `WAYPOINT ${idx}`}
                </div>
                <div style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '0.1rem' }}>
                  {pt}
                </div>
              </div>
            </div>

            {idx < waypoints.length - 1 && (
              <ArrowRight size={20} color="var(--accent-amber)" style={{ opacity: 0.7 }} />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}



