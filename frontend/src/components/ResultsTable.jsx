import React from 'react';

const ResultsTable = ({ results }) => {
    if (!results || results.length === 0) {
        return (
            <div className="empty-state">
                <div className="empty-state-icon">🔍</div>
                <h3 className="empty-state-title">No results yet</h3>
                <p className="empty-state-description">
                    Enter a job description or requirement to discover relevant SHL assessments
                </p>
            </div>
        );
    }

    const getBadgeClass = (type) => {
        const typeLower = type.toLowerCase();
        if (typeLower.includes('knowledge') || typeLower.includes('skill')) {
            return 'badge-knowledge';
        }
        if (typeLower.includes('personality') || typeLower.includes('behavior')) {
            return 'badge-personality';
        }
        if (typeLower.includes('ability') || typeLower.includes('aptitude')) {
            return 'badge-ability';
        }
        return '';
    };

    return (
        <div className="results-section">
            <div className="results-grid">
                {results.map((assessment, index) => (
                    <div key={index} className="assessment-card">
                        <div className="card-header">
                            <h3 className="card-title">{assessment.name}</h3>
                        </div>

                        <div className="card-badges">
                            {assessment.test_type && assessment.test_type.map((type, idx) => (
                                <span key={idx} className={`badge ${getBadgeClass(type)}`}>
                                    {type}
                                </span>
                            ))}
                        </div>

                        <p className="card-description">
                            {assessment.description || 'No description available.'}
                        </p>

                        <div className="card-meta">
                            {assessment.duration > 0 && (
                                <div className="meta-item">
                                    <span>⏱️</span>
                                    <span>{assessment.duration} mins</span>
                                </div>
                            )}
                            {assessment.adaptive_support && (
                                <div className="meta-item">
                                    <span>🎯</span>
                                    <span>Adaptive: {assessment.adaptive_support}</span>
                                </div>
                            )}
                            {assessment.remote_support && (
                                <div className="meta-item">
                                    <span>🌐</span>
                                    <span>Remote: {assessment.remote_support}</span>
                                </div>
                            )}
                        </div>

                        <div className="card-footer">
                            <a
                                href={assessment.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="card-link"
                            >
                                View Details →
                            </a>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ResultsTable;
