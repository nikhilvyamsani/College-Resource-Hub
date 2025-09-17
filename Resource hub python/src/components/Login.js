import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8001';

function Login({ setToken }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const response = await axios.post(`${API_BASE}/login`, {
          username: formData.username,
          password: formData.password
        });
        localStorage.setItem('token', response.data.access_token);
        setToken(response.data.access_token);
      } else {
        await axios.post(`${API_BASE}/register`, formData);
        alert('Registration successful! Please login.');
        setIsLogin(true);
      }
    } catch (error) {
      alert(error.response?.data?.detail || 'An error occurred');
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>{isLogin ? 'Login' : 'Register'}</h2>
        
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={formData.username}
            onChange={(e) => setFormData({...formData, username: e.target.value})}
            required
          />
        </div>

        {!isLogin && (
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>
        )}

        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            required
          />
        </div>

        <button type="submit" className="btn">
          {isLogin ? 'Login' : 'Register'}
        </button>

        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? 'Need an account? Register' : 'Have an account? Login'}
        </button>
      </form>
    </div>
  );
}

export default Login;