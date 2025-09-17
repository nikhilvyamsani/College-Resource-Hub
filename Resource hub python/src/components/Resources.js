import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8001';

function Resources() {
  const [resources, setResources] = useState([]);
  const [filters, setFilters] = useState({
    subject: '',
    semester: '',
    search: ''
  });
  const [showRating, setShowRating] = useState(null);
  const [rating, setRating] = useState({ rating: 5, feedback: '' });

  useEffect(() => {
    fetchResources();
  }, [filters]);

  const fetchResources = async () => {
    try {
      const params = new URLSearchParams();
      Object.keys(filters).forEach(key => {
        if (filters[key]) params.append(key, filters[key]);
      });
      
      const response = await axios.get(`${API_BASE}/resources?${params}`);
      setResources(response.data);
    } catch (error) {
      console.error('Error fetching resources:', error);
    }
  };

  const handleDownload = async (resourceId, filename) => {
    try {
      const response = await axios.get(`${API_BASE}/download/${resourceId}`);
      window.open(`${API_BASE}${response.data.download_url}`, '_blank');
    } catch (error) {
      alert('Download failed');
    }
  };

  const handleRating = async (resourceId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API_BASE}/rate/${resourceId}`, rating, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      alert('Rating submitted successfully!');
      setShowRating(null);
      setRating({ rating: 5, feedback: '' });
      fetchResources();
    } catch (error) {
      alert('Rating failed');
    }
  };

  return (
    <div>
      <h1>Resources</h1>
      
      <div className="filters">
        <div className="form-group">
          <label>Subject</label>
          <input
            type="text"
            value={filters.subject}
            onChange={(e) => setFilters({...filters, subject: e.target.value})}
            placeholder="Filter by subject"
          />
        </div>

        <div className="form-group">
          <label>Semester</label>
          <select
            value={filters.semester}
            onChange={(e) => setFilters({...filters, semester: e.target.value})}
          >
            <option value="">All Semesters</option>
            {[1,2,3,4,5,6,7,8].map(sem => (
              <option key={sem} value={`Semester ${sem}`}>Semester {sem}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Search</label>
          <input
            type="text"
            value={filters.search}
            onChange={(e) => setFilters({...filters, search: e.target.value})}
            placeholder="Search resources"
          />
        </div>
      </div>

      <div className="resource-grid">
        {resources.map(resource => (
          <div key={resource.id} className="resource-card">
            <div className="resource-info">
              <h3>{resource.title}</h3>
              <p>{resource.description}</p>
              <div className="resource-meta">
                {resource.subject} • Semester {resource.semester} • By {resource.uploader}
                <br />
                ★ {resource.average_rating} • {resource.download_count} downloads
                <br />
                Tags: {resource.tags.join(', ')}
              </div>
            </div>
            
            <div className="resource-actions">
              <button 
                className="btn btn-small"
                onClick={() => handleDownload(resource.id, resource.filename)}
              >
                Download
              </button>
              <button 
                className="btn btn-small btn-secondary"
                onClick={() => setShowRating(resource.id)}
              >
                Rate
              </button>
            </div>

            {showRating === resource.id && (
              <div style={{ marginTop: '1rem', padding: '1rem', background: '#f8f9fa', borderRadius: '4px' }}>
                <div className="form-group">
                  <label>Rating (1-5)</label>
                  <select
                    value={rating.rating}
                    onChange={(e) => setRating({...rating, rating: parseInt(e.target.value)})}
                  >
                    {[1,2,3,4,5].map(r => (
                      <option key={r} value={r}>{r} Star{r > 1 ? 's' : ''}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Feedback (optional)</label>
                  <textarea
                    value={rating.feedback}
                    onChange={(e) => setRating({...rating, feedback: e.target.value})}
                    rows="2"
                  />
                </div>
                <button 
                  className="btn btn-small"
                  onClick={() => handleRating(resource.id)}
                >
                  Submit Rating
                </button>
                <button 
                  className="btn btn-small btn-secondary"
                  onClick={() => setShowRating(null)}
                  style={{ marginLeft: '0.5rem' }}
                >
                  Cancel
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Resources;