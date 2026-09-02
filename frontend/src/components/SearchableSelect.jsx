import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Search, X, MapPin } from 'lucide-react';

export default function SearchableSelect({ options = [], value, onChange, placeholder = 'Select port...', label, icon: Icon = MapPin }) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const wrapperRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const selectedOption = options.find(opt => opt.value === value || opt.label === value);

  const filteredOptions = options.filter(opt =>
    opt.label.toLowerCase().includes(search.toLowerCase()) ||
    opt.value.toLowerCase().includes(search.toLowerCase())
  );

  const handleSelect = (val) => {
    onChange(val);
    setIsOpen(false);
    setSearch('');
  };

  const handleClear = (e) => {
    e.stopPropagation();
    onChange('');
    setSearch('');
  };

  return (
    <div className="form-group" ref={wrapperRef} style={{ position: 'relative' }}>
      {label && (
        <label className="form-label">
          {Icon && <Icon size={13} color="var(--accent-maritime-blue)" />}
          {label}
        </label>
      )}

      {/* Main Select Field Box */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        className="input-field"
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          cursor: 'pointer',
          userSelect: 'none',
          borderColor: isOpen ? 'var(--accent-amber)' : undefined,
          boxShadow: isOpen ? '0 0 0 2px var(--amber-glow)' : undefined
        }}
      >
        <span style={{ color: selectedOption ? 'var(--text-primary)' : 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontWeight: selectedOption ? 600 : 400 }}>
          {selectedOption ? selectedOption.label : placeholder}
        </span>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          {selectedOption && (
            <div onClick={handleClear} style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', padding: '2px' }}>
              <X size={14} />
            </div>
          )}
          <ChevronDown size={16} color="var(--text-muted)" style={{ transform: isOpen ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s ease' }} />
        </div>
      </div>

      {/* Popover Dropdown Menu */}
      {isOpen && (
        <div
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            right: 0,
            marginTop: '0.35rem',
            background: 'var(--surface-elevated)',
            border: '1px solid var(--border-medium)',
            borderRadius: 'var(--radius-md)',
            boxShadow: 'var(--shadow-elevated)',
            zIndex: 100,
            overflow: 'hidden'
          }}
        >
          {/* Search Filter Input inside Menu */}
          <div style={{ padding: '0.55rem 0.75rem', borderBottom: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'var(--surface-secondary)' }}>
            <Search size={14} color="var(--accent-maritime-blue)" />
            <input
              type="text"
              autoFocus
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter..."
              style={{
                width: '100%',
                background: 'transparent',
                border: 'none',
                color: 'var(--text-primary)',
                outline: 'none',
                fontSize: '0.85rem',
                fontFamily: 'var(--font-body)'
              }}
            />
          </div>

          {/* Options Scroll List */}
          <div style={{ maxHeight: '200px', overflowY: 'auto', padding: '0.25rem 0' }}>
            {filteredOptions.length > 0 ? (
              filteredOptions.map((opt) => (
                <div
                  key={opt.value}
                  onClick={() => handleSelect(opt.value)}
                  style={{
                    padding: '0.6rem 0.9rem',
                    fontSize: '0.85rem',
                    color: value === opt.value ? 'var(--accent-amber)' : 'var(--text-primary)',
                    fontWeight: value === opt.value ? 700 : 400,
                    background: value === opt.value ? 'rgba(245, 185, 66, 0.1)' : 'transparent',
                    cursor: 'pointer',
                    transition: 'background 0.15s ease'
                  }}
                  onMouseEnter={(e) => {
                    if (value !== opt.value) e.currentTarget.style.background = 'rgba(255, 255, 255, 0.04)';
                  }}
                  onMouseLeave={(e) => {
                    if (value !== opt.value) e.currentTarget.style.background = 'transparent';
                  }}
                >
                  {opt.label}
                </div>
              ))
            ) : (
              <div style={{ padding: '0.85rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.825rem' }}>
                No matching option
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}



