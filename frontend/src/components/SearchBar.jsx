import React from 'react';

const SearchBar = ({ query, setQuery, onSearch, loading }) => {
    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch();
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            handleSubmit(e);
        }
    };

    return (
        <div className="search-section">
            <form onSubmit={handleSubmit}>
                <div className="search-container">
                    <div className="search-input-wrapper">
                        <input
                            type="text"
                            className="search-input"
                            placeholder="Describe the role or requirement (e.g., 'Java developer with strong collaboration skills')..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyPress={handleKeyPress}
                            disabled={loading}
                        />
                    </div>
                    <button
                        type="submit"
                        className={`search-button ${loading ? 'loading' : ''}`}
                        disabled={loading || !query.trim()}
                    >
                        {loading ? 'Analyzing...' : 'Discover Assessments'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default SearchBar;
