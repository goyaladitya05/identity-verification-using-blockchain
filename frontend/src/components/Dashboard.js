import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Alert, Spinner, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { userService, credentialService } from '../services/authService';
import './Dashboard.css';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [credentials, setCredentials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchUserProfile();
    fetchCredentials();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await userService.getProfile();
      setUser(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch profile');
    }
  };

  const fetchCredentials = async () => {
    try {
      const response = await credentialService.listCredentials();
      setCredentials(response.data.credentials);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch credentials');
    } finally {
      setLoading(false);
    }
  };

  const [showModal, setShowModal] = useState(false);
  const [modalCredential, setModalCredential] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);

  const handleView = async (credentialId) => {
    setActionLoading(true);
    try {
      const resp = await credentialService.getCredential(credentialId);
      setModalCredential(resp.data.credential);
      setShowModal(true);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch credential');
    } finally {
      setActionLoading(false);
    }
  };

  const handleRevoke = async (credentialId) => {
    if (!window.confirm('Are you sure you want to revoke this credential?')) return;
    setActionLoading(true);
    try {
      await credentialService.revokeCredential(credentialId);
      // refresh credentials list
      await fetchCredentials();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to revoke credential');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
        <Spinner animation="border" />
      </Container>
    );
  }

  return (
    <Container className="dashboard-container">
      <Row className="my-5">
        <Col md={8}>
          <h1>Welcome, {user?.full_name}!</h1>
          {error && <Alert variant="danger">{error}</Alert>}

          <Card className="mb-4">
            <Card.Header className="bg-primary text-white">
              <h5>Profile Information</h5>
            </Card.Header>
            <Card.Body>
              <p><strong>Email:</strong> {user?.email}</p>
              <p><strong>Wallet Address:</strong> <code>{user?.wallet_address}</code></p>
              <p><strong>Credentials:</strong> {user?.credential_count}</p>
            </Card.Body>
          </Card>

          <Card>
            <Card.Header className="bg-success text-white">
              <h5>Your Credentials</h5>
            </Card.Header>
            <Card.Body>
              {credentials.length === 0 ? (
                <p>No credentials yet. Upload your first credential to get started!</p>
              ) : (
                <div className="credentials-list">
                  {credentials.map((cred) => (
                    <div key={cred.credential_id} className="credential-item mb-3 p-3 border rounded">
                      <h6>{cred.credential_type.toUpperCase()}</h6>
                      <p className="text-muted">
                        Hash: <code className="full-hash">{cred.blockchain_hash}</code>
                      </p>
                      <p className="text-muted">
                        Created: {new Date(cred.created_at).toLocaleDateString()}
                      </p>
                      <Button variant="warning" size="sm" className="me-2" onClick={() => handleView(cred.credential_id)} disabled={actionLoading}>
                        {actionLoading ? 'Loading...' : 'View'}
                      </Button>
                      <Button variant="danger" size="sm" onClick={() => handleRevoke(cred.credential_id)} disabled={actionLoading}>
                        {actionLoading ? 'Working...' : 'Revoke'}
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="quick-actions">
            <Card.Header className="bg-info text-white">
              <h5>Quick Actions</h5>
            </Card.Header>
            <Card.Body>
              {/* Use SPA navigation (no full page reload) */}
              <Button variant="primary" className="w-100 mb-2" onClick={() => navigate('/upload-credential')}>
                + Upload Credential
              </Button>
              <Button variant="secondary" className="w-100 mb-2" onClick={() => navigate('/verify-credential')}>
                Verify Credential
              </Button>
              <Button variant="outline-primary" className="w-100" onClick={() => navigate('/profile')}>
                Profile Settings
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      {/* Credential detail modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Credential Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {modalCredential ? (
            <div>
              <p><strong>Type:</strong> {modalCredential.credential_type}</p>
              <p><strong>Created:</strong> {new Date(modalCredential.created_at).toLocaleString()}</p>
              <p><strong>Blockchain Hash:</strong></p>
              <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', background: '#f6f6f6', padding: '10px' }}>{modalCredential.blockchain_hash}</pre>
              <p><strong>Credential Data (decrypted):</strong></p>
              <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', background: '#f6f6f6', padding: '10px' }}>{JSON.stringify(modalCredential.credential_data, null, 2)}</pre>
            </div>
          ) : (
            <p>Loading...</p>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Close</Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default Dashboard;

