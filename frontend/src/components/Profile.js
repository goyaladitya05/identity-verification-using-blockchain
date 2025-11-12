import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Form, Alert } from 'react-bootstrap';
import { userService, authService } from '../services/authService';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [fullName, setFullName] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await userService.getProfile();
        setUser(res.data);
        setFullName(res.data.full_name || '');
      } catch (err) {
        setMessage('Failed to load profile');
      }
    };
    fetch();
  }, []);

  const handleSave = async () => {
    try {
      await userService.updateProfile(fullName);
      setMessage('Profile updated');
    } catch (err) {
      setMessage('Failed to update profile');
    }
  };

  // Password change
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [pwMessage, setPwMessage] = useState('');
  const [pwLoading, setPwLoading] = useState(false);

  const handleChangePassword = async () => {
    setPwMessage('');
    if (!oldPassword || !newPassword) {
      setPwMessage('Please enter old and new password');
      return;
    }

    setPwLoading(true);
    try {
      await authService.changePassword(oldPassword, newPassword);
      setPwMessage('Password changed successfully');
      setOldPassword('');
      setNewPassword('');
    } catch (err) {
      setPwMessage(err.response?.data?.error || 'Failed to change password');
    } finally {
      setPwLoading(false);
    }
  };

  return (
    <Container className="my-5">
      <Card>
        <Card.Header><h5>Profile Settings</h5></Card.Header>
        <Card.Body>
          {message && <Alert variant="info">{message}</Alert>}
          {user ? (
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control type="text" readOnly value={user.email} />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Full name</Form.Label>
                <Form.Control value={fullName} onChange={(e) => setFullName(e.target.value)} />
              </Form.Group>

              <Button onClick={handleSave}>Save</Button>
            </Form>
          ) : (
            <p>Loading...</p>
          )}
          <hr />
          <h6>Change Password</h6>
          {pwMessage && <Alert variant="info">{pwMessage}</Alert>}
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Old Password</Form.Label>
              <Form.Control type="password" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>New Password</Form.Label>
              <Form.Control type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
            </Form.Group>
            <Button onClick={handleChangePassword} disabled={pwLoading}>{pwLoading ? 'Saving...' : 'Change Password'}</Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Profile;
