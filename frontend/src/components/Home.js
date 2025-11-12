import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home">
      <section className="hero">
        <Container>
          <Row className="align-items-center">
            <Col md={6}>
              <h1 className="hero-title">Decentralized Identity Verification</h1>
              <p className="hero-subtitle">
                Secure, transparent, and user-controlled identity management powered by blockchain
              </p>
              <Button 
                variant="primary" 
                size="lg" 
                onClick={() => navigate('/register')}
                className="me-2"
              >
                Get Started
              </Button>
              <Button 
                variant="outline-light" 
                size="lg"
                onClick={() => navigate('/login')}
              >
                Login
              </Button>
            </Col>
            <Col md={6}>
              <div className="hero-image">
                <i className="fas fa-shield-alt fa-10x text-primary"></i>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      <section className="features my-5">
        <Container>
          <h2 className="text-center mb-5">Why Choose Our Platform?</h2>
          <Row>
            <Col md={4} className="mb-4">
              <Card className="feature-card h-100">
                <Card.Body className="text-center">
                  <h5 className="mb-3">🔒 Secure</h5>
                  <p>
                    Encrypted storage with advanced cryptography ensures your data remains secure.
                  </p>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4">
              <Card className="feature-card h-100">
                <Card.Body className="text-center">
                  <h5 className="mb-3">⛓️ Blockchain</h5>
                  <p>
                    Immutable ledger ensures data integrity and tamper-proof verification.
                  </p>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4">
              <Card className="feature-card h-100">
                <Card.Body className="text-center">
                  <h5 className="mb-3">👤 User Control</h5>
                  <p>
                    You have complete control over your data and who can access it.
                  </p>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  );
};

export default Home;
