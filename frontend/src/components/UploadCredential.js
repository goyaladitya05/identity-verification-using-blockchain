import React, { useState } from 'react';
import { Container, Card, Form, Button, Alert, Spinner } from 'react-bootstrap';
import { credentialService } from '../services/authService';

const UploadCredential = () => {
  const [credentialType, setCredentialType] = useState('passport');
  const [credentialData, setCredentialData] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(null);

    if (!credentialData) {
      setError('Please enter credential data (JSON)');
      return;
    }

    let parsedData;
    try {
      parsedData = JSON.parse(credentialData);
    } catch (err) {
      setError('Credential data must be valid JSON');
      return;
    }

    setLoading(true);
    try {
      const res = await credentialService.createCredential(credentialType, parsedData);
      setSuccess(res.data);
      setCredentialData('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create credential');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="my-5">
      <Card>
        <Card.Header><h5>Upload Credential</h5></Card.Header>
        <Card.Body>
          {error && <Alert variant="danger">{error}</Alert>}
          {success && (
            <Alert variant="success">
              <h6>✓ Credential Created Successfully</h6>
              <p className="mb-2"><strong>Credential Hash:</strong> <code>{success.credential_hash}</code></p>
              {success.blockchain_tx && (
                <div className="mt-3 p-2 bg-light rounded">
                  <h6>Blockchain Transaction:</h6>
                  <p className="mb-1"><strong>TX Hash:</strong> <code style={{fontSize: '0.8rem'}}>{success.blockchain_tx.tx_hash}</code></p>
                  <p className="mb-1"><strong>Block Number:</strong> {success.blockchain_tx.block_number}</p>
                  <p className="mb-1"><strong>Gas Used:</strong> {success.blockchain_tx.gas_used}</p>
                  <p className="mb-1"><strong>Status:</strong> {success.blockchain_tx.status === 1 ? '✓ Success' : '✗ Failed'}</p>
                  {success.blockchain_tx.simulated && (
                    <p className="mt-2 text-muted"><em>Note: Simulated transaction for demo (stored in MongoDB with on-chain integration ready)</em></p>
                  )}
                </div>
              )}
            </Alert>
          )}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Credential Type</Form.Label>
              <Form.Control as="select" value={credentialType} onChange={(e) => setCredentialType(e.target.value)}>
                <option value="passport">Passport</option>
                <option value="aadhar">Aadhaar</option>
                <option value="drivers_license">Driver's License</option>
                <option value="degree">Degree</option>
                <option value="other">Other</option>
              </Form.Control>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Credential Data (JSON)</Form.Label>
              <Form.Control as="textarea" rows={8} value={credentialData} onChange={(e) => setCredentialData(e.target.value)} placeholder='{"name":"John","id":"..."}' />
            </Form.Group>

            <Button type="submit" disabled={loading}>{loading ? (<><Spinner animation="border" size="sm"/> Creating...</>) : 'Create Credential'}</Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default UploadCredential;
