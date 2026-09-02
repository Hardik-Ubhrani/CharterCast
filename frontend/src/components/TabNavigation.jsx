import React from 'react';
import { Ship, TrendingUp } from 'lucide-react';

export default function TabNavigation({ activeTab, setActiveTab }) {
  return (
    <nav style={{ marginBottom: '1.5rem' }}>
      <div 
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '2rem',
          borderBottom: '1px solid var(--border-subtle)',
          padding: '0 0.25rem'
        }}
      >
        {/* Tab 1: Vessel Intelligence */}
        <button
          type="button"
          onClick={() => setActiveTab('vessel')}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.55rem',
            padding: '0.8rem 0.25rem',
            background: 'transparent',
            border: 'none',
            borderBottom: activeTab === 'vessel' 
              ? '2px solid var(--accent-amber)' 
              : '2px solid transparent',
            color: activeTab === 'vessel' ? 'var(--text-primary)' : 'var(--text-secondary)',
            fontFamily: 'var(--font-heading)',
            fontSize: '0.925rem',
            fontWeight: activeTab === 'vessel' ? 800 : 600,
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            position: 'relative'
          }}
        >
          <Ship size={17} color={activeTab === 'vessel' ? 'var(--accent-amber)' : 'var(--text-muted)'} />
          <span>VESSEL INTELLIGENCE</span>
        </button>

        {/* Tab 2: Freight & Route Intelligence */}
        <button
          type="button"
          onClick={() => setActiveTab('freight')}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.55rem',
            padding: '0.8rem 0.25rem',
            background: 'transparent',
            border: 'none',
            borderBottom: activeTab === 'freight' 
              ? '2px solid var(--accent-amber)' 
              : '2px solid transparent',
            color: activeTab === 'freight' ? 'var(--text-primary)' : 'var(--text-secondary)',
            fontFamily: 'var(--font-heading)',
            fontSize: '0.925rem',
            fontWeight: activeTab === 'freight' ? 800 : 600,
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            position: 'relative'
          }}
        >
          <TrendingUp size={17} color={activeTab === 'freight' ? 'var(--accent-amber)' : 'var(--text-muted)'} />
          <span>FREIGHT & ROUTE INTELLIGENCE</span>
        </button>
      </div>
    </nav>
  );
}



