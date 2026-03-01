// src/pages/Dashboard.js
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import "./Dashboard.css";

function Dashboard() {
  const [deviceData, setDeviceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchDeviceData();
    
    // Optional: Set up polling for real-time updates
    const interval = setInterval(fetchDeviceData, 30000); // Update every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchDeviceData = async () => {
    try {
      const response = await API.get("/device-data"); // Adjust endpoint as needed
      setDeviceData(response.data);
      setError("");
    } catch (err) {
      console.error("Error fetching device data:", err);
      setError("Failed to fetch device data");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  if (loading) {
    return <div className="loading-screen">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h2>Smart Transformer Dashboard</h2>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </header>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="dashboard-content">
        {deviceData ? (
          <div className="data-grid">
            {/* Display your device data here */}
            <pre>{JSON.stringify(deviceData, null, 2)}</pre>
          </div>
        ) : (
          <p>No device data available</p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;