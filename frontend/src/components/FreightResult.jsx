import React from 'react';
import { TrendingUp, Clock, Calendar } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function FreightResult({ freightState }) {
  if (!freightState) return null;

  // Case A: Pending / Model Connection Pending State
  if (freightState.pending) {
    return (
      <div className="pending-card" style={{ marginTop: '1.5rem' }}>
        <div className="pending-icon-wrapper">
          <Clock size={24} />
        </div>
        <span className="pending-badge">MODEL INTEGRATION PENDING</span>
        <div className="pending-title">FREIGHT RATE FORECASTING</div>
        <div className="pending-sub">
          Awaiting ML temporal forecast model integration for dynamic freight rate trajectory predictions.
        </div>
      </div>
    );
  }

  // Case B: Real Backend Forecast Data Returned
  const { data } = freightState;
  if (!data) return null;

  const {
    current_rate,
    forecast_rate,
    lower_bound,
    upper_bound,
    trend,
    forecast_points,
    model_used
  } = data;

  const chartData = forecast_points?.map(pt => ({
    date: pt.date || `Day ${pt.day}`,
    rate: pt.rate,
    lower: pt.lower_bound,
    upper: pt.upper_bound
  })) || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '0.5rem' }}>
      
      {/* Hero Freight Rate Card */}
      <div className="hero-result-card panel-elevated" style={{ padding: '2rem 1.75rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1.25rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.65rem' }}>
              <span className="tag-pill tag-ai">
                <TrendingUp size={12} />
                AI FREIGHT MODEL
              </span>
              <span style={{ fontSize: '0.725rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>
                {model_used || 'Forecast Engine'}
              </span>
            </div>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-secondary)', fontWeight: 800 }}>
              PREDICTED FREIGHT RATE
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: 900, color: 'var(--accent-amber)', letterSpacing: '-0.02em', marginTop: '0.2rem' }}>
              ${forecast_rate?.toFixed(2)} <span style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>/ MT</span>
            </div>
          </div>

          {current_rate && (
            <div
              style={{
                padding: '0.9rem 1.4rem',
                borderRadius: 'var(--radius-md)',
                background: 'var(--surface-secondary)',
                border: '1px solid var(--border-medium)',
                textAlign: 'right'
              }}
            >
              <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                CURRENT SPOT RATE
              </div>
              <div style={{ fontSize: '1.25rem', fontWeight: 900, color: 'var(--text-primary)', marginTop: '0.15rem' }}>
                ${current_rate?.toFixed(2)} / MT
              </div>
              {trend && (
                <div style={{ fontSize: '0.775rem', color: trend === 'DOWN' ? 'var(--accent-success)' : 'var(--accent-danger)', fontWeight: 800, marginTop: '0.2rem' }}>
                  Trend: {trend}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Bounds & Horizon Grid */}
        {(lower_bound !== undefined || upper_bound !== undefined) && (
          <div className="grid-3col" style={{ marginTop: '1.5rem', paddingTop: '1.25rem', borderTop: '1px solid var(--border-subtle)' }}>
            <div style={{ background: 'var(--surface-secondary)', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>LOWER BOUND</div>
              <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--accent-success)', marginTop: '0.2rem' }}>${lower_bound?.toFixed(2)} / MT</div>
            </div>
            <div style={{ background: 'var(--surface-secondary)', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>UPPER BOUND</div>
              <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--accent-danger)', marginTop: '0.2rem' }}>${upper_bound?.toFixed(2)} / MT</div>
            </div>
            <div style={{ background: 'var(--surface-secondary)', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>FORECAST HORIZON</div>
              <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--accent-amber)', marginTop: '0.2rem' }}>30 Days</div>
            </div>
          </div>
        )}
      </div>

      {/* Recharts 30-Day Line Chart */}
      {chartData.length > 0 && (
        <div className="panel-primary" style={{ padding: '1.75rem 1.6rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.35rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Calendar size={18} color="var(--accent-amber)" />
              30-DAY FREIGHT RATE TRAJECTORY
            </h3>
          </div>

          <div style={{ width: '100%', height: 280 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
                <XAxis dataKey="date" stroke="var(--text-secondary)" tick={{ fontSize: 11 }} />
                <YAxis stroke="var(--text-secondary)" tick={{ fontSize: 11 }} domain={['dataMin - 1', 'dataMax + 1']} />
                <Tooltip
                  contentStyle={{ background: '#11161C', borderColor: 'var(--border-medium)', borderRadius: '8px', color: '#fff' }}
                  formatter={(val) => [`$${Number(val).toFixed(2)} / MT`, 'Rate']}
                />
                <Line type="monotone" dataKey="rate" stroke="var(--accent-amber)" strokeWidth={2.5} dot={false} activeDot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

    </div>
  );
}


