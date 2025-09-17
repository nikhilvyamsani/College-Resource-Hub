import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8001';

function Upload() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    subject: '',
    semester: '',
    tags: ''
  });
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a file');
      return;
    }

    const uploadData = new FormData();
    Object.keys(formData).forEach(key => {
      uploadData.append(key, formData[key]);
    });
    uploadData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API_BASE}/upload`, uploadData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      alert('Resource uploaded successfully!');
      setFormData({ title: '', description: '', subject: '', semester: '', tags: '' });
      setFile(null);
    } catch (error) {
      alert(error.response?.data?.detail || 'Upload failed');
    }
  };

  return (
    <div>
      <h1>Upload Resource</h1>
      <form onSubmit={handleSubmit} style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <div className="form-group">
          <label>Title</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            required
          />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            rows="3"
            required
          />
        </div>

        <div className="form-group">
          <label>Subject</label>
          <input
            type="text"
            value={formData.subject}
            onChange={(e) => setFormData({...formData, subject: e.target.value})}
            required
          />
        </div>

        <div className="form-group">
          <label>Semester</label>
          <select
            value={formData.semester}
            onChange={(e) => setFormData({...formData, semester: e.target.value})}
            required
          >
            <option value="">Select Semester</option>
            {[1,2,3,4,5,6,7,8].map(sem => (
              <option key={sem} value={`Semester ${sem}`}>Semester {sem}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Tags (comma-separated)</label>
          <input
            type="text"
            value={formData.tags}
            onChange={(e) => setFormData({...formData, tags: e.target.value})}
            placeholder="notes, exam, important"
          />
        </div>

        <div className="form-group">
          <label>File</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
        </div>

        <button type="submit" className="btn">Upload Resource</button>
      </form>
    </div>
  );
}

export default Upload;