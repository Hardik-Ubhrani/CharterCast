import React from 'react';
import { Compass, Activity } from 'lucide-react';

export default function HeroBanner() {
  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '2rem',
        alignItems: 'center',
        padding: '2rem 2.2rem',
        marginBottom: '1.75rem',
        background: 'var(--surface-primary)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-elevated)',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Subtle Background Glow behind left headline */}
      <div
        style={{
          position: 'absolute',
          top: '-20%',
          left: '-10%',
          width: '450px',
          height: '450px',
          background: 'radial-gradient(circle, rgba(245, 185, 66, 0.05) 0%, transparent 70%)',
          pointerEvents: 'none',
          zIndex: 0
        }}
      />

      {/* LEFT COLUMN: Messaging */}
      <div style={{ position: 'relative', zIndex: 1 }}>
        {/* Eyebrow */}
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.45rem',
            padding: '0.25rem 0.7rem',
            borderRadius: 'var(--radius-full)',
            background: 'rgba(245, 185, 66, 0.08)',
            border: '1px solid rgba(245, 185, 66, 0.2)',
            color: 'var(--accent-amber)',
            fontSize: '0.7rem',
            fontWeight: 800,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            marginBottom: '1rem'
          }}
        >
          <Compass size={13} />
          <span>MARITIME AI DECISION SUPPORT</span>
        </div>

        {/* Large Headline */}
        <h2
          style={{
            fontSize: '2.4rem',
            fontWeight: 900,
            color: 'var(--text-primary)',
            lineHeight: 1.15,
            letterSpacing: '-0.03em',
            marginBottom: '0.85rem'
          }}
        >
          Smarter Chartering.<br />
          <span style={{ color: 'var(--accent-amber)' }}>
            Powered by Intelligence.
          </span>
        </h2>

        {/* Supporting Text */}
        <p
          style={{
            fontSize: '0.925rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.55,
            maxWidth: '520px'
          }}
        >
          Forecast freight rates, identify suitable vessels and optimize trade decisions with AI-powered maritime intelligence.
        </p>
      </div>

      {/* RIGHT COLUMN: Sophisticated Maritime Intelligence Visualization */}
      <div
        style={{
          position: 'relative',
          height: '240px',
          background: 'var(--surface-secondary)',
          border: '1px solid var(--border-medium)',
          borderRadius: 'var(--radius-md)',
          overflow: 'hidden',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        {/* SVG Maritime Grid & Animated Route Canvas */}
        <svg
          width="100%"
          height="100%"
          viewBox="0 0 440 240"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          style={{ position: 'absolute', inset: 0 }}
        >
          <defs>
            {/* Gradient for route line: Amber -> Muted Ocean Blue */}
            <linearGradient id="routeGradient" x1="60" y1="180" x2="380" y2="70" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#F5B942" stopOpacity="0.9" />
              <stop offset="60%" stopColor="#D99A2B" stopOpacity="1" />
              <stop offset="100%" stopColor="#4C8DAA" stopOpacity="0.8" />
            </linearGradient>
            
            {/* Subtle Glow filter */}
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="2" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* Grid lines (Latitude / Longitude lines) */}
          <line x1="0" y1="60" x2="440" y2="60" stroke="rgba(255,255,255,0.025)" strokeWidth="1" />
          <line x1="0" y1="120" x2="440" y2="120" stroke="rgba(255,255,255,0.025)" strokeWidth="1" />
          <line x1="0" y1="180" x2="440" y2="180" stroke="rgba(255,255,255,0.025)" strokeWidth="1" />
          
          <line x1="110" y1="0" x2="110" y2="240" stroke="rgba(255,255,255,0.025)" strokeWidth="1" />
          <line x1="220" y1="0" x2="220" y2="240" stroke="rgba(255,255,255,0.025)" strokeWidth="1" />
          <line x1="330" y1="0" x2="330" y2="240" stroke="rgba(255,255,255,0.025)" strokeWidth="1" />

          {/* Radar Circles (Subtle Gray/Blue) */}
          <circle cx="220" cy="120" r="100" stroke="rgba(76, 141, 170, 0.12)" strokeWidth="1" strokeDasharray="4 4" />
          <circle cx="220" cy="120" r="60" stroke="rgba(76, 141, 170, 0.15)" strokeWidth="1" />
          <circle cx="220" cy="120" r="25" stroke="rgba(76, 141, 170, 0.2)" strokeWidth="1" />

          {/* Axis Coordinates Crosshairs */}
          <line x1="220" y1="15" x2="220" y2="225" stroke="rgba(76, 141, 170, 0.15)" strokeWidth="1" strokeDasharray="2 2" />
          <line x1="15" y1="120" x2="425" y2="120" stroke="rgba(76, 141, 170, 0.15)" strokeWidth="1" strokeDasharray="2 2" />

          {/* Background Route Track */}
          <path
            d="M 60 180 Q 150 70 240 130 T 380 70"
            stroke="rgba(76, 141, 170, 0.2)"
            strokeWidth="2.5"
            fill="none"
          />

          {/* Animated Trajectory */}
          <path
            d="M 60 180 Q 150 70 240 130 T 380 70"
            stroke="url(#routeGradient)"
            strokeWidth="2"
            strokeDasharray="10 6"
            fill="none"
            filter="url(#glow)"
          >
            <animate attributeName="stroke-dashoffset" from="32" to="0" dur="2.8s" repeatCount="indefinite" />
          </path>

          {/* Port Nodes (Amber) */}
          {/* Node 1: Origin Port */}
          <circle cx="60" cy="180" r="5" fill="#080B0F" stroke="#F5B942" strokeWidth="2" />
          <circle cx="60" cy="180" r="8" fill="none" stroke="rgba(245, 185, 66, 0.35)" strokeWidth="1">
            <animate attributeName="r" values="5;10;5" dur="2.2s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="1;0;1" dur="2.2s" repeatCount="indefinite" />
          </circle>
          <text x="60" y="202" fill="#9BA7B4" fontSize="9" fontFamily="JetBrains Mono" textAnchor="middle" fontWeight="600">PARADIP PORT</text>

          {/* Node 2: Intermediate Waypoint */}
          <circle cx="240" cy="130" r="4" fill="#080B0F" stroke="#4C8DAA" strokeWidth="2" />
          <text x="240" y="116" fill="#66727E" fontSize="8" fontFamily="JetBrains Mono" textAnchor="middle">WAYPOINT 01</text>

          {/* Node 3: Destination Port */}
          <circle cx="380" cy="70" r="5" fill="#080B0F" stroke="#F5B942" strokeWidth="2" />
          <circle cx="380" cy="70" r="8" fill="none" stroke="rgba(245, 185, 66, 0.35)" strokeWidth="1">
            <animate attributeName="r" values="5;10;5" dur="2.2s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="1;0;1" dur="2.2s" repeatCount="indefinite" />
          </circle>
          <text x="380" y="54" fill="#F5B942" fontSize="9" fontFamily="JetBrains Mono" textAnchor="middle" fontWeight="600">MAURER PORT</text>

          {/* Active Vessel Indicator Icon along Path */}
          <g transform="translate(190, 105)">
            <circle cx="0" cy="0" r="12" fill="rgba(245, 185, 66, 0.12)" stroke="rgba(245, 185, 66, 0.3)" strokeWidth="1" />
            <polygon points="-4,-5 7,0 -4,5 -1,0" fill="#F5B942" />
          </g>
        </svg>

        {/* Telemetry Overlay Card (Bottom-Left corner) */}
        <div
          style={{
            position: 'absolute',
            bottom: '10px',
            left: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.35rem 0.65rem',
            borderRadius: 'var(--radius-sm)',
            background: 'rgba(17, 22, 28, 0.9)',
            border: '1px solid var(--border-medium)',
            backdropFilter: 'blur(6px)',
            fontSize: '0.675rem',
            fontFamily: 'var(--font-mono)',
            color: 'var(--text-secondary)'
          }}
        >
          <Activity size={12} color="var(--accent-amber)" />
          <span>MARITIME RADAR: ACTIVE</span>
        </div>

        {/* Telemetry Overlay Card (Top-Right corner) */}
        <div
          style={{
            position: 'absolute',
            top: '10px',
            right: '12px',
            padding: '0.3rem 0.6rem',
            borderRadius: 'var(--radius-sm)',
            background: 'rgba(17, 22, 28, 0.9)',
            border: '1px solid var(--border-medium)',
            backdropFilter: 'blur(6px)',
            fontSize: '0.65rem',
            fontFamily: 'var(--font-mono)',
            color: 'var(--accent-amber)'
          }}
        >
          LANES ANALYZED: 100%
        </div>
      </div>
    </div>
  );
}



