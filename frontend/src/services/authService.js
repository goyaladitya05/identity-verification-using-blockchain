import api from './api';

export const authService = {
  register: (email, password, walletAddress, fullName) => {
    return api.post('/auth/register', {
      email,
      password,
      wallet_address: walletAddress,
      full_name: fullName,
    });
  },

  login: (email, password) => {
    return api.post('/auth/login', {
      email,
      password,
    });
  },

  verifyToken: (token) => {
    return api.post('/auth/verify-token', {}, {
      headers: { Authorization: `Bearer ${token}` },
    });
  },

  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  },
  changePassword: (oldPassword, newPassword) => {
    return api.post('/users/change-password', {
      old_password: oldPassword,
      new_password: newPassword,
    });
  },
};

export const userService = {
  getProfile: () => {
    return api.get('/users/profile');
  },

  updateProfile: (fullName) => {
    return api.put('/users/profile', {
      full_name: fullName,
    });
  },

  verifyUser: (userId) => {
    return api.post(`/users/verify/${userId}`);
  },
};

export const credentialService = {
  createCredential: (credentialType, credentialData) => {
    return api.post('/credentials/create', {
      credential_type: credentialType,
      credential_data: credentialData,
    });
  },

  listCredentials: () => {
    return api.get('/credentials/list');
  },

  getCredential: (credentialId) => {
    return api.get(`/credentials/${credentialId}`);
  },

  revokeCredential: (credentialId) => {
    return api.post(`/credentials/${credentialId}/revoke`);
  },

  verifyCredential: (credentialHash) => {
    return api.get(`/credentials/verify/${credentialHash}`);
  },

  getBlockchainProof: (credentialHash) => {
    return api.get(`/credentials/${credentialHash}/blockchain-proof`);
  },
};
