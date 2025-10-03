import React, { useState } from 'react';

// API base URL - adjust this to match your FastAPI server
const API_BASE_URL = 'http://localhost:8081';

export default function AddApplicantModal({ jobTitle = "Senior UX Designer", jobId, onClose }) {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (error) {
      setError('');
    }
  };

  const validateForm = () => {
    if (!formData.firstName.trim()) {
      setError('First name is required');
      return false;
    }
    if (!formData.lastName.trim()) {
      setError('Last name is required');
      return false;
    }
    if (!formData.email.trim()) {
      setError('Email is required');
      return false;
    }
    if (!formData.email.includes('@')) {
      setError('Please enter a valid email address');
      return false;
    }
    if (!jobId) {
      setError('Job ID is missing');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      // Step 1: Create the candidate
      const candidateData = {
        first_name: formData.firstName.trim(),
        last_name: formData.lastName.trim(),
        email: formData.email.trim(),
        phone: formData.phone.trim() || null
      };

      console.log('Creating candidate:', candidateData);
      const candidateResponse = await fetch(`${API_BASE_URL}/candidates/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(candidateData),
      });

      if (!candidateResponse.ok) {
        const errorData = await candidateResponse.json();
        throw new Error(errorData.detail || `Failed to create candidate: ${candidateResponse.status}`);
      }

      const candidate = await candidateResponse.json();
      console.log('Created candidate:', candidate);

      // Step 2: Create the application
      const applicationData = {
        job_id: jobId,
        candidate_id: candidate.candidate_id,
        status: 'applied' // Default status
      };

      console.log('Creating application:', applicationData);
      const applicationResponse = await fetch(`${API_BASE_URL}/applications/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(applicationData),
      });

      if (!applicationResponse.ok) {
        const errorData = await applicationResponse.json();
        throw new Error(errorData.detail || `Failed to create application: ${applicationResponse.status}`);
      }

      const application = await applicationResponse.json();
      console.log('Created application:', application);

      // Success! Close the modal
      onClose();

    } catch (err) {
      console.error('Error creating applicant:', err);
      setError(err.message || 'Failed to create applicant. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white p-8 rounded-xl shadow-lg max-w-lg w-full font-sans">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Add New Applicant for {jobTitle}
      </h2>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-700 text-sm">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="space-y-5">
          <div>
            <label htmlFor="firstName" className="sr-only">
              First Name
            </label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleInputChange}
              disabled={isSubmitting}
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>
          <div>
            <label htmlFor="lastName" className="sr-only">
              Last Name
            </label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleInputChange}
              disabled={isSubmitting}
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>
          <div>
            <label htmlFor="email" className="sr-only">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
              disabled={isSubmitting}
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>
          <div>
            <label htmlFor="phone" className="sr-only">
              Phone Number
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              placeholder="Phone Number (optional)"
              value={formData.phone}
              onChange={handleInputChange}
              disabled={isSubmitting}
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>

          <div>
            <label
              htmlFor="resume-upload"
              className="flex items-center justify-center w-full p-6 mt-2 bg-blue-50 border-2 border-blue-400 border-dashed rounded-lg cursor-pointer hover:bg-blue-100 transition-colors"
            >
              <div className="text-center">
                <div className="flex items-center justify-center">
                   <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    className="h-8 w-8 text-blue-500 mr-3" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor" 
                    strokeWidth="1.5"
                   >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" 
                    />
                  </svg>
                  <p className="text-gray-600">
                    Drag and drop resume or click to upload
                  </p>
                </div>
              </div>
              <input id="resume-upload" name="resume-upload" type="file" className="hidden" />
            </label>
          </div>
        </div>

        <div className="mt-8 flex justify-end gap-4">
          <button
            type="button"
            onClick={onClose}
            disabled={isSubmitting}
            className="px-6 py-2 border border-blue-500 text-blue-500 font-semibold rounded-md hover:bg-blue-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isSubmitting && (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            )}
            {isSubmitting ? 'Saving...' : 'Save Applicant'}
          </button>
        </div>
      </form>
    </div>
  );
};