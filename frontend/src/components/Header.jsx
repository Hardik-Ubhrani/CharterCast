import React from 'react';
import { Anchor, Server } from 'lucide-react';

export default function Header({ isBackendOnline }) {
  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0.85rem 1.4rem',
        marginBottom: '1.5rem',
        background: 'var(--surface-primary)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-flat)',
        flexWrap: 'wrap',
        gap: '1rem'
      }}
    >
      {/* Brand & Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
        <div 
          style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: 'rgba(245, 185, 66, 0.12)',
            border: '1px solid rgba(245, 185, 66, 0.3)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--accent-amber)'
          }}
        >
          <Anchor size={20} />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <h1 style={{ fontSize: '1.35rem', fontWeight: 900, color: 'var(--text-primary)', letterSpacing: '-0.02em', lineHeight: 1 }}>
              CHARTER CAST
            </h1>
          </div>
          <p style={{ fontSize: '0.675rem', color: 'var(--text-secondary)', fontWeight: 700, letterSpacing: '0.08em', marginTop: '0.2rem', textTransform: 'uppercase' }}>
            AI-POWERED FREIGHT & VESSEL INTELLIGENCE
          </p>
        </div>
      </div>

      {/* Subtle Status Indicators */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontSize: '0.725rem', fontWeight: 700, color: 'var(--text-secondary)', letterSpacing: '0.05em' }}>
          <span className="status-dot-green"></span>
          <span>AI SYSTEM ONLINE</span>
        </div>
        
        <div 
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            padding: '0.25rem 0.65rem',
            borderRadius: 'var(--radius-full)',
            background: isBackendOnline ? 'rgba(76, 141, 170, 0.1)' : 'rgba(224, 82, 82, 0.1)',
            border: `1px solid ${isBackendOnline ? 'rgba(76, 141, 170, 0.25)' : 'rgba(224, 82, 82, 0.25)'}`,
            color: isBackendOnline ? 'var(--accent-maritime-blue)' : 'var(--accent-danger)',
            fontSize: '0.7rem',
            fontWeight: 700,
            letterSpacing: '0.04em'
          }}
        >
          <Server size={12} />
          <span>{isBackendOnline ? 'BACKEND CONNECTED' : 'BACKEND DISCONNECTED'}</span>
        </div>
      </div>

    </header>
  );
}



