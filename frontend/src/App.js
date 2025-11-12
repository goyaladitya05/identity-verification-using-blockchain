import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import AppNavbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import UploadCredential from './components/UploadCredential';
import VerifyCredential from './components/VerifyCredential';
import Profile from './components/Profile';
import './App.css';

function App() {
  const isAuthenticated = () => {
    return localStorage.getItem('authToken') !== null;
  };

  const PrivateRoute = ({ element }) => {
    return isAuthenticated() ? element : <Navigate to="/login" />;
  };

  return (
    <Router>
      <AppNavbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
  <Route path="/dashboard" element={<PrivateRoute element={<Dashboard />} />} />
  <Route path="/upload-credential" element={<PrivateRoute element={<UploadCredential />} />} />
  <Route path="/verify-credential" element={<PrivateRoute element={<VerifyCredential />} />} />
  <Route path="/profile" element={<PrivateRoute element={<Profile />} />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
