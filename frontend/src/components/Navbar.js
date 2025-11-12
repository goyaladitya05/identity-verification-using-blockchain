import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';
import './Navbar.css';

const AppNavbar = () => {
  const navigate = useNavigate();
  const isAuthenticated = localStorage.getItem('authToken') !== null;
  const user = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null;

  const handleLogout = () => {
    authService.logout();
    navigate('/');
  };

  const handleHome = () => {
    navigate('/');
  };

  const handleDashboard = () => {
    navigate('/dashboard');
  };

  return (
    <Navbar bg="light" expand="lg" sticky="top" className="navbar-custom">
      <Container>
        <Navbar.Brand onClick={handleHome} style={{ cursor: 'pointer', fontWeight: 'bold', fontSize: '1.3rem' }}>
          🔐 Identity Verification
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto align-items-center">
            {isAuthenticated ? (
              <>
                <Nav.Link onClick={handleDashboard}>Dashboard</Nav.Link>
                <Nav.Link onClick={() => navigate('/upload-credential')}>Upload</Nav.Link>
                <Nav.Link onClick={() => navigate('/verify-credential')}>Verify</Nav.Link>
                <Nav.Link onClick={() => navigate('/profile')}>Profile</Nav.Link>
                <div className="navbar-user me-3">
                  {user?.full_name || user?.email}
                </div>
                <Button variant="outline-primary" size="sm" onClick={handleLogout}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Nav.Link onClick={() => navigate('/login')}>Login</Nav.Link>
                <Nav.Link onClick={() => navigate('/register')}>Register</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
