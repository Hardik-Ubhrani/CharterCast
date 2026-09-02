import React, { useState } from 'react';
import SearchableSelect from '../components/SearchableSelect';
import FreightResult from '../components/FreightResult';
import RouteResult from '../components/RouteResult';
import { PORT_OPTIONS, COMMODITIES, VESSEL_TYPES } from '../services/portData';
import { forecastFreight } from '../services/freightApi';
import { recommendTradeRoute } from '../services/tradeRouteApi';
import { TrendingUp, Scale, Package, Compass, Anchor, Ship, AlertCircle, Sparkles, Activity, DollarSign, Navigation } from 'lucide-react';

export default function FreightRouteIntelligence({ onFreightStateChange, onRouteStateChange }) {
  const [cargoQuantity, setCargoQuantity] = useState('70000');
  const [commodity, setCommodity] = useState('Coal');
  const [originPort, setOriginPort] = useState('Australia');
  const [destinationPort, setDestinationPort] = useState('Paradip Port');
  const [vesselType, setVesselType] = useState('Panamax');

  // Freight Predict Parameters (Spot Model Inputs)
  const [bdi, setBdi] = useState('1772');
  const [dailyTimeCharter, setDailyTimeCharter] = useState('18957');
  const [newcastleCoalPrice, setNewcastleCoalPrice] = useState('158.44');
  const [voyageDistance, setVoyageDistance] = useState('5120');

  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState('');
  const [error, setError] = useState(null);

  const [freightState, setFreightState] = useState(null);
  const [routeState, setRouteState] = useState(null);

  const handleOptimizeRouteOnly = async () => {
    setError(null);

    if (!originPort) {
      setError('Please select an origin port.');
      return;
    }
    if (!destinationPort) {
      setError('Please select a destination port.');
      return;
    }

    setLoading(true);
    setLoadingText('Optimizing trade route...');
    setRouteState({ pending: true });

    try {
      const routeRes = await recommendTradeRoute({
        origin: originPort,
        destination: destinationPort,
        commodity: commodity,
        vesselClass: vesselType,
        cargoQuantity: cargoQuantity
      });
      setRouteState(routeRes);
      if (onRouteStateChange) onRouteStateChange(routeRes);
    } catch (err) {
      const errorState = { pending: false, error: err.message || 'Unable to connect to the Charter Cast AI backend.' };
      setRouteState(errorState);
      if (onRouteStateChange) onRouteStateChange(errorState);
      setError(err.message || 'Unable to connect to the Charter Cast AI backend.');
    } finally {
      setLoading(false);
      setLoadingText('');
    }
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
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
    setLoadingText('Generating freight intelligence...');

    try {
      // 1. Query Freight Forecast & Prediction
      const freightRes = await forecastFreight({
        origin: originPort,
        destination: destinationPort,
        vesselClass: vesselType,
        cargoQuantity,
        commodity,
        bdi: Number(bdi),
        dailyTimeCharter: Number(dailyTimeCharter),
        newcastleCoalPrice: Number(newcastleCoalPrice),
        voyageDistance: Number(voyageDistance)
      });
      setFreightState(freightRes);
      if (onFreightStateChange) onFreightStateChange(freightRes);

      setLoadingText('Optimizing trade route...');
      setRouteState({ pending: true });

      // 2. Query Trade Route
      const routeRes = await recommendTradeRoute({
        origin: originPort,
        destination: destinationPort,
        commodity: commodity,
        vesselClass: vesselType,
        cargoQuantity: cargoQuantity
      });
      setRouteState(routeRes);
      if (onRouteStateChange) onRouteStateChange(routeRes);

    } catch (err) {
      setError(err.message || 'Unable to connect to the Charter Cast AI backend.');
    } finally {
      setLoading(false);
      setLoadingText('');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      
      {/* Input Form Panel */}
      <div className="panel-primary" style={{ padding: '1.75rem 1.6rem' }}>
        <div style={{ marginBottom: '1.4rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.55rem' }}>
            <TrendingUp size={20} color="var(--accent-amber)" />
            FREIGHT & ROUTE INTELLIGENCE
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
            Forecast freight rates and optimize passage routing parameters.
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* Inputs Row 1: Cargo, Commodity, Vessel */}
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
                  placeholder="e.g. 70000"
                  value={cargoQuantity}
                  onChange={(e) => setCargoQuantity(e.target.value)}
                />
                <span className="unit-tag-mt">MT</span>
              </div>
            </div>

            {/* 2. Commodity Dropdown */}
            <SearchableSelect
              label="COMMODITY"
              icon={Package}
              placeholder="Select commodity..."
              options={COMMODITIES}
              value={commodity}
              onChange={setCommodity}
            />

            {/* 3. Vessel Type Dropdown */}
            <SearchableSelect
              label="VESSEL TYPE"
              icon={Ship}
              placeholder="Select vessel class..."
              options={VESSEL_TYPES}
              value={vesselType}
              onChange={setVesselType}
            />

          </div>

          {/* Inputs Row 2: Origin & Destination */}
          <div className="grid-2col">
            
            {/* 4. Origin Port Dropdown */}
            <SearchableSelect
              label="ORIGIN PORT"
              icon={Compass}
              placeholder="Select origin port..."
              options={PORT_OPTIONS}
              value={originPort}
              onChange={setOriginPort}
            />

            {/* 5. Destination Port Dropdown */}
            <SearchableSelect
              label="DESTINATION PORT"
              icon={Anchor}
              placeholder="Select destination port..."
              options={PORT_OPTIONS}
              value={destinationPort}
              onChange={setDestinationPort}
            />

          </div>

          {/* Inputs Row 3: Spot Freight Model Parameters */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <Activity size={13} color="var(--accent-amber)" />
                BALTIC DRY INDEX (BDI)
              </label>
              <input
                type="number"
                step="any"
                className="input-field"
                placeholder="1772"
                value={bdi}
                onChange={(e) => setBdi(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <DollarSign size={13} color="var(--accent-amber)" />
                DAILY TIME CHARTER ($/DAY)
              </label>
              <input
                type="number"
                step="any"
                className="input-field"
                placeholder="18957"
                value={dailyTimeCharter}
                onChange={(e) => setDailyTimeCharter(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <DollarSign size={13} color="var(--accent-amber)" />
                NEWCASTLE COAL PRICE ($/MT)
              </label>
              <input
                type="number"
                step="any"
                className="input-field"
                placeholder="158.44"
                value={newcastleCoalPrice}
                onChange={(e) => setNewcastleCoalPrice(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <Navigation size={13} color="var(--accent-amber)" />
                VOYAGE DISTANCE (NM)
              </label>
              <input
                type="number"
                step="any"
                className="input-field"
                placeholder="5120"
                value={voyageDistance}
                onChange={(e) => setVoyageDistance(e.target.value)}
              />
            </div>
          </div>

          {/* Error Alert */}
          {error && (
            <div
              style={{
                padding: '0.75rem 1rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255, 77, 109, 0.1)',
                border: '1px solid rgba(255, 77, 109, 0.25)',
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

          {/* Action Buttons Row */}
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
            <button
              type="button"
              onClick={handleOptimizeRouteOnly}
              className="btn-primary"
              style={{
                flex: '1',
                minWidth: '220px',
                background: 'linear-gradient(135deg, #4C8DAA 0%, #2B5B75 100%)',
                borderColor: 'rgba(76, 141, 170, 0.4)'
              }}
              disabled={loading}
            >
              {loading && loadingText.includes('route') ? (
                <>
                  <div className="spinner"></div>
                  <span>{loadingText}</span>
                </>
              ) : (
                <>
                  <Navigation size={16} />
                  <span>OPTIMIZE TRADE ROUTE</span>
                </>
              )}
            </button>

            <button type="submit" className="btn-primary" style={{ flex: '1', minWidth: '220px' }} disabled={loading}>
              {loading && !loadingText.includes('route') ? (
                <>
                  <div className="spinner"></div>
                  <span>{loadingText || 'Generating freight intelligence...'}</span>
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  <span>ANALYZE FREIGHT & ROUTE</span>
                </>
              )}
            </button>
          </div>

        </form>
      </div>

      {/* Results Presentation */}
      <FreightResult freightState={freightState} />
      <RouteResult routeState={routeState} />

    </div>
  );
}
