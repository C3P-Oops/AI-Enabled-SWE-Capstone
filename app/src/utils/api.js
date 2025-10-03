// API utility functions for the recruitment app

const API_BASE_URL = 'http://localhost:8081';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API Error ${response.status}: ${errorText}`);
  }
  return response.json();
};

// API functions
export const api = {
  // Test connection
  async testConnection() {
    try {
      const response = await fetch(`${API_BASE_URL}/`);
      return await handleResponse(response);
    } catch (error) {
      console.error('API connection test failed:', error);
      throw error;
    }
  },

  // Jobs
  async getJobs() {
    const response = await fetch(`${API_BASE_URL}/jobs/`);
    return await handleResponse(response);
  },

  async getJob(jobId) {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
    return await handleResponse(response);
  },

  async createJob(jobData) {
    const response = await fetch(`${API_BASE_URL}/jobs/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jobData),
    });
    return await handleResponse(response);
  },

  // Candidates
  async getCandidates() {
    const response = await fetch(`${API_BASE_URL}/candidates/`);
    return await handleResponse(response);
  },

  async getCandidate(candidateId) {
    const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}`);
    return await handleResponse(response);
  },

  async createCandidate(candidateData) {
    const response = await fetch(`${API_BASE_URL}/candidates/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(candidateData),
    });
    return await handleResponse(response);
  },

  // Applications
  async getApplications() {
    const response = await fetch(`${API_BASE_URL}/applications/`);
    return await handleResponse(response);
  },

  async getApplication(applicationId) {
    const response = await fetch(`${API_BASE_URL}/applications/${applicationId}`);
    return await handleResponse(response);
  },

  async createApplication(applicationData) {
    const response = await fetch(`${API_BASE_URL}/applications/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(applicationData),
    });
    return await handleResponse(response);
  },

  async updateApplication(applicationId, updateData) {
    const response = await fetch(`${API_BASE_URL}/applications/${applicationId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateData),
    });
    return await handleResponse(response);
  },

  // Users
  async getUsers() {
    const response = await fetch(`${API_BASE_URL}/users/`);
    return await handleResponse(response);
  },

  async createUser(userData) {
    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    return await handleResponse(response);
  },
};

export default api;