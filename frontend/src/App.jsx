import React, { useState } from 'react';
import axios from 'axios';
import SearchBar from './components/SearchBar';
import ResultsTable from './components/ResultsTable';

const API_URL = 'https://shl-assessment-recommendation-system-bz51.onrender.com';
const API_URL = 'https://shl-assessment-recommendation-system-bz51.onrender.com';

const App = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async () => {
        if (!query.trim()) return;

        setLoading(true);
        setError(null);

        try {
            const response = await axios.post(`${API_URL}/recommend`, {
                query: query
            });

            setResults(response.data.recommended_assessments || []);
        } catch (err) {
            console.error('Search error:', err);
            setError(err.response?.data?.detail || 'Failed to fetch recommendations. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <div className="main-content">
                {/* Header */}
                <header className="header">
                    <h1 className="header-title">SHL Assessment Intelligence</h1>
                    <p className="header-subtitle">
                        AI-Powered Assessment Discovery • Semantic Search Engine
                    </p>
                </header>

                {/* Search Bar */}
                <SearchBar
                    query={query}
                    setQuery={setQuery}
                    onSearch={handleSearch}
                    loading={loading}
                />

                {/* Error Message */}
                {error && (
                    <div style={{
                        padding: '1rem',
                        marginBottom: '2rem',
                        background: 'linear-gradient(135deg, rgba(245, 87, 108, 0.15) 0%, rgba(240, 147, 251, 0.05) 100%)',
                        border: '1px solid rgba(245, 87, 108, 0.3)',
                        borderRadius: '12px',
                        color: '#ffb3c1'
                    }}>
                        ⚠️ {error}
                    </div>
                )}

                {/* Results */}
                <ResultsTable results={results} />

                {/* Footer Info */}
                {results.length > 0 && (
                    <div style={{
                        marginTop: '2rem',
                        padding: '1.5rem',
                        textAlign: 'center',
                        color: 'var(--text-muted)',
                        fontSize: '0.875rem',
                        borderTop: '1px solid var(--border-subtle)'
                    }}>
                        Showing {results.length} {results.length === 1 ? 'assessment' : 'assessments'} •
                        Powered by Gemini AI & Semantic Search
                    </div>
                )}
            </div>
        </div>
    );
};

export default App;