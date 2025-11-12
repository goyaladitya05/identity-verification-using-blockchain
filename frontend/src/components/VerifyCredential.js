import React, { useState } from 'react';
import { Container, Card, Form, Button, Alert, Spinner } from 'react-bootstrap';
import { credentialService } from '../services/authService';

const VerifyCredential = () => {
  const [hash, setHash] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [blockchainProof, setBlockchainProof] = useState(null);
  const [error, setError] = useState('');

  const handleVerify = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setBlockchainProof(null);

    if (!hash) {
      setError('Please enter a credential hash');
      return;
    }

    setLoading(true);
    try {
      const res = await credentialService.verifyCredential(hash.trim());
      setResult(res.data);
      
      // Also fetch blockchain proof
      try {
        const proofRes = await credentialService.getBlockchainProof(hash.trim());
        setBlockchainProof(proofRes.data.blockchain_proof);
      } catch (proofErr) {
        console.log('Blockchain proof not available');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="my-5">
      <Card>
        <Card.Header><h5>Verify Credential</h5></Card.Header>
        <Card.Body>
          {error && <Alert variant="danger">{error}</Alert>}
          {result && (
            <>
              <Alert variant={result.valid ? 'success' : 'warning'}>
                <h6>Verification Result</h6>
                <p className="mb-2"><strong>Valid:</strong> {result.valid ? '✓ Yes' : '✗ No'}</p>
                <p className="mb-2"><strong>Type:</strong> {result.credential_type}</p>
                <p className="mb-2"><strong>Hash:</strong> <code style={{fontSize: '0.85rem'}}>{result.blockchain_hash}</code></p>
                <p className="mb-2"><strong>Created:</strong> {new Date(result.created_at).toLocaleString()}</p>
                
                {result.blockchain_verification && (
                  <div className="mt-3 p-2 bg-light rounded">
                    <h6>Blockchain Verification:</h6>
                    <p className="mb-0"><strong>Verified On Network:</strong> {result.blockchain_verification.valid ? '✓ Yes' : '✗ No'}</p>
                    <p className="text-muted mb-0"><em>Source: {result.blockchain_verification.source}</em></p>
                  </div>
                )}
              </Alert>

              {blockchainProof && (
                <Alert variant="info">
                  <h6>🔗 Blockchain Proof</h6>
                  <p className="mb-2"><strong>Owner Address:</strong> <code style={{fontSize: '0.8rem'}}>{blockchainProof.owner_address}</code></p>
                  <p className="mb-2"><strong>Contract Address:</strong> <code style={{fontSize: '0.8rem'}}>{blockchainProof.contract_address}</code></p>
                  <p className="mb-2"><strong>Network:</strong> {blockchainProof.network}</p>
                  <p className="mb-0"><strong>Status:</strong> {blockchainProof.verified_on_chain ? '✓ Verified On-Chain' : '✗ Not Found On-Chain'}</p>
                </Alert>
              )}
            </>
          )}

          <Form onSubmit={handleVerify}>
            <Form.Group className="mb-3">
              <Form.Label>Credential Hash</Form.Label>
              <Form.Control 
                value={hash} 
                onChange={(e) => setHash(e.target.value)} 
                placeholder="0x1234567890abcdef..." 
              />
            </Form.Group>
            <Button type="submit" disabled={loading}>
              {loading ? (<><Spinner animation="border" size="sm"/> Verifying...</>) : 'Verify'}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default VerifyCredential;
