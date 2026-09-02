import React from 'react';
import { Ship, Compass, Anchor, Cpu, CheckCircle2, XCircle, Info, Scale, Waves, ArrowRight } from 'lucide-react';

export default function VesselResult({ result }) {
  if (!result) return null;

  const {
    recommended_vessel,
    route,
    consignment_size,
    route_max_draft,
    explanation,
    options
  } = result;

  // Format SHAP feature contribution drivers for display
  const shapDrivers = explanation ? Object.entries(explanation).map(([key, val]) => {
    const absVal = Math.abs(val);
    let displayName = key;
    if (key === 'consignment_size') displayName = 'Consignment Size';
    else if (key === 'route_max_draft') displayName = 'Route Max Draft';
    else if (key === 'origin_port') displayName = 'Origin';
    else if (key === 'destination_port') displayName = 'Destination';
    else if (key === 'budget') displayName = 'Budget';

    return {
      key,
      name: displayName,
      rawVal: val,
      absVal,
    };
  }).sort((a, b) => b.absVal - a.absVal) : [];

  const maxShap = shapDrivers.length > 0 ? Math.max(...shapDrivers.map(d => d.absVal), 0.0001) : 1;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

      {/* Hero Result Card: Dominant Recommended Vessel */}
      <div className="hero-result-card panel-elevated" style={{ padding: '2rem 1.75rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1.25rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.65rem' }}>
              <span className="tag-pill tag-ai">
                <Cpu size={12} />
                AI RECOMMENDATION
              </span>
              <span style={{ fontSize: '0.725rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>
                XGBoost Intelligence Model
              </span>
            </div>
            
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-secondary)', fontWeight: 800 }}>
              RECOMMENDED VESSEL
            </div>
            
            <div style={{ fontSize: '2.5rem', fontWeight: 900, color: 'var(--text-primary)', letterSpacing: '-0.02em', marginTop: '0.2rem', textTransform: 'uppercase' }}>
              <span style={{ color: 'var(--text-primary)' }}>{recommended_vessel?.split('/')[0]}</span>
              {recommended_vessel?.includes('/') && (
                <span style={{ color: 'var(--accent-amber)' }}> / {recommended_vessel?.split('/')[1]}</span>
              )}
              {!recommended_vessel?.includes('/') && recommended_vessel}
            </div>
          </div>

          <div
            style={{
              padding: '1rem 1.4rem',
              borderRadius: 'var(--radius-md)',
              background: 'var(--surface-secondary)',
              border: '1px solid var(--border-medium)',
              display: 'flex',
              alignItems: 'center',
              gap: '1rem'
            }}
          >
            <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(245, 185, 66, 0.12)', border: '1px solid rgba(245, 185, 66, 0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-amber)' }}>
              <Ship size={24} />
            </div>
            <div>
              <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                SUITABILITY INDEX
              </div>
              <div style={{ fontSize: '1.05rem', fontWeight: 900, color: 'var(--accent-amber)', marginTop: '0.1rem' }}>
                OPTIMAL SELECTION
              </div>
            </div>
          </div>
        </div>

        {/* Maritime Route & Cargo Vector Banner */}
        <div style={{ marginTop: '1.75rem', paddingTop: '1.4rem', borderTop: '1px solid var(--border-subtle)' }}>
          
          <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.75rem' }}>
            TRADE ROUTE & CARGO MATRIX
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr auto 1fr auto 1fr',
              alignItems: 'center',
              gap: '1rem',
              background: 'var(--surface-secondary)',
              padding: '1.1rem 1.4rem',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)'
            }}
          >
            {/* Cargo Quantity */}
            <div>
              <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 800, letterSpacing: '0.05em' }}>
                CARGO SIZE
              </div>
              <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--accent-amber)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginTop: '0.2rem' }}>
                <Scale size={15} />
                {consignment_size ? `${Number(consignment_size).toLocaleString()} MT` : 'N/A'}
              </div>
            </div>

            {/* Separator */}
            <div style={{ color: 'var(--text-muted)', opacity: 0.4 }}>|</div>

            {/* Origin Port */}
            <div>
              <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 800, letterSpacing: '0.05em' }}>
                ORIGIN PORT
              </div>
              <div style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginTop: '0.2rem' }}>
                <Compass size={15} color="var(--accent-maritime-blue)" />
                {route?.origin_port || 'N/A'}
              </div>
            </div>

            {/* Direction Arrow */}
            <div style={{ display: 'flex', alignItems: 'center', color: 'var(--accent-amber)' }}>
              <ArrowRight size={20} />
            </div>

            {/* Destination Port */}
            <div>
              <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 800, letterSpacing: '0.05em' }}>
                DESTINATION PORT
              </div>
              <div style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginTop: '0.2rem' }}>
                <Anchor size={15} color="var(--accent-maritime-blue)" />
                {route?.destination_port || 'N/A'}
              </div>
            </div>

          </div>

          {route_max_draft && (
            <div style={{ marginTop: '0.75rem', fontSize: '0.775rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.4rem', fontFamily: 'var(--font-mono)' }}>
              <Info size={13} color="var(--accent-amber)" />
              <span>Route Bottleneck Max Permissible Draft: <strong style={{ color: 'var(--text-primary)' }}>{route_max_draft}m</strong></span>
            </div>
          )}

        </div>
      </div>

      {/* SHAP Decision Drivers Bar Visualization */}
      {shapDrivers.length > 0 && (
        <div className="panel-primary" style={{ padding: '1.75rem 1.6rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.35rem' }}>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Cpu size={18} color="var(--accent-amber)" />
                AI DECISION DRIVERS
              </h3>
              <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
                Feature contribution weights driving XGBoost classification selection
              </p>
            </div>
            <span style={{ fontSize: '0.7rem', color: 'var(--accent-amber)', background: 'rgba(245, 185, 66, 0.08)', border: '1px solid rgba(245, 185, 66, 0.2)', padding: '0.25rem 0.65rem', borderRadius: 'var(--radius-sm)', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
              SHAP Explainer Matrix
            </span>
          </div>

          <div className="shap-bar-container">
            {shapDrivers.map((driver) => {
              const widthPct = Math.min(Math.round((driver.absVal / maxShap) * 100), 100);
              const isPositive = driver.rawVal >= 0;
              return (
                <div key={driver.key} className="shap-bar-item">
                  <div className="shap-bar-header">
                    <span style={{ fontWeight: 600 }}>{driver.name}</span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: isPositive ? 'var(--accent-amber)' : 'var(--accent-danger)', fontWeight: 700 }}>
                      {isPositive ? `+${driver.rawVal.toFixed(3)}` : driver.rawVal.toFixed(3)}
                    </span>
                  </div>
                  <div className="shap-bar-track">
                    <div
                      className="shap-bar-fill"
                      style={{
                        width: `${Math.max(widthPct, 4)}%`,
                        background: isPositive
                          ? 'linear-gradient(90deg, var(--accent-gold) 0%, var(--accent-amber) 100%)'
                          : 'linear-gradient(90deg, #802A2A 0%, var(--accent-danger) 100%)'
                      }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>

          <div style={{ marginTop: '1.25rem', fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Info size={13} color="var(--text-muted)" />
            <span>Note: Warm Amber bars indicate positive contribution toward selection; muted red bars indicate draft or budget constraints.</span>
          </div>
        </div>
      )}

      {/* Alternative Vessel Feasibility Assessment Options */}
      {options && options.length > 0 && (
        <div className="panel-primary" style={{ padding: '1.75rem 1.6rem' }}>
          <div style={{ marginBottom: '1.35rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Waves size={18} color="var(--accent-amber)" />
              VESSEL CLASS FEASIBILITY MATRIX
            </h3>
            <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
              Operational constraints and draft compliance across commercial bulk classes
            </p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {options.map((opt, idx) => (
              <div key={idx} className="option-row">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                  {opt.feasible ? (
                    <CheckCircle2 size={20} color="var(--accent-success)" />
                  ) : (
                    <XCircle size={20} color="var(--accent-danger)" />
                  )}
                  <div>
                    <div style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                      {opt.vessel_class}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.1rem' }}>
                      {opt.reason}
                    </div>
                  </div>
                </div>

                <div style={{ textAlign: 'right', flexShrink: 0 }}>
                  <span className={opt.feasible ? 'badge-feasible' : 'badge-restricted'}>
                    {opt.feasible ? 'FEASIBLE' : 'RESTRICTED'}
                  </span>
                  {opt.feasible && opt.score > 0 && (
                    <div style={{ fontSize: '0.725rem', color: 'var(--text-secondary)', marginTop: '0.25rem', fontFamily: 'var(--font-mono)' }}>
                      Score: {opt.score}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}



