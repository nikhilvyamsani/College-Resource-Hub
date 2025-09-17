import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8001';

function Dashboard() {
  const [dashboardData, setDashboardData] = useState({ top_rated: [], most_downloaded: [] });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get(`${API_BASE}/dashboard`);
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Top Rated Resources</h3>
          {dashboardData.top_rated.map(resource => (
            <div key={resource.id} style={{ padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
              <div>{resource.title}</div>
              <div className="rating">★ {resource.rating}</div>
            </div>
          ))}
        </div>

        <div className="dashboard-card">
          <h3>Most Downloaded</h3>
          {dashboardData.most_downloaded.map(resource => (
            <div key={resource.id} style={{ padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
              <div>{resource.title}</div>
              <div className="resource-meta">{resource.downloads} downloads</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;