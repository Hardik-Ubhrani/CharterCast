import React, { useState } from 'react';
import SearchableSelect from '../components/SearchableSelect';
import VesselResult from '../components/VesselResult';
import { PORT_OPTIONS } from '../services/portData';
import { recommendVessel } from '../services/vesselApi';
import { Ship, Scale, Compass, Anchor, AlertCircle, Sparkles, ArrowRight } from 'lucide-react';

export default function VesselIntelligence({ onVesselResultChange }) {
  const [cargoQuantity, setCargoQuantity] = useState('');
  const [originPort, setOriginPort] = useState('');
  const [destinationPort, setDestinationPort] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!cargoQuantity || Number(cargoQuantity) <= 0) {
      setError('Please enter a valid cargo quantity.');
      return;
    }
    if (!originPort) {
      setError('Please select an origin port.');
      return;
    }
    if (!destinationPort) {
      setError('Please select a destination port.');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const res = await recommendVessel({
        cargoQuantityMt: cargoQuantity,
        originPort,
        destinationPort
      });
      setResult(res);
      if (onVesselResultChange) {
        onVesselResultChange(res);
      }
    } catch (err) {
      setError(err.message || 'Unable to connect to the Charter Cast AI backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      
      {/* Input Workspace Panel */}
      <div className="panel-primary" style={{ padding: '1.75rem 1.6rem' }}>
        <div style={{ marginBottom: '1.4rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.55rem' }}>
            <Ship size={20} color="var(--accent-amber)" />
            VESSEL SELECTION INTELLIGENCE
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
            Identify optimal vessel class by analyzing cargo tonnage and draft constraints across trade lanes.
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* 3-Column Input Workspace */}
          <div className="grid-3col">
            
            {/* 1. Cargo Quantity Input */}
            <div className="form-group">
              <label className="form-label">
                <Scale size={13} color="var(--accent-maritime-blue)" />
                CARGO QUANTITY
              </label>
              <div className="input-container-mt">
                <input
                  type="number"
                  min="1"
                  step="any"
                  className="input-field"
                  placeholder="e.g. 50000"
                  value={cargoQuantity}
                  onChange={(e) => setCargoQuantity(e.target.value)}
                />
                <span className="unit-tag-mt">MT</span>
              </div>
            </div>

            {/* 2. Origin Port Dropdown */}
            <SearchableSelect
              label="ORIGIN PORT"
              icon={Compass}
              placeholder="Select origin port..."
              options={PORT_OPTIONS}
              value={originPort}
              onChange={setOriginPort}
            />

            {/* 3. Destination Port Dropdown */}
            <SearchableSelect
              label="DESTINATION PORT"
              icon={Anchor}
              placeholder="Select destination port..."
              options={PORT_OPTIONS}
              value={destinationPort}
              onChange={setDestinationPort}
            />

          </div>

          {/* Error Alert Box */}
          {error && (
            <div
              style={{
                padding: '0.75rem 1rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(224, 82, 82, 0.1)',
                border: '1px solid rgba(224, 82, 82, 0.25)',
                color: 'var(--accent-danger)',
                fontSize: '0.825rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '0.55rem'
              }}
            >
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          {/* Primary Action Button — Strongest Amber CTA */}
          <div style={{ marginTop: '0.25rem' }}>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? (
                <>
                  <div className="spinner"></div>
                  <span>Evaluating Vessel Suitability...</span>
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  <span>ANALYZE VESSEL</span>
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </div>

        </form>
      </div>

      {/* Result Presentation Component */}
      <VesselResult result={result} />

    </div>
  );
}



