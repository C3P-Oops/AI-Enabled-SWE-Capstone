import React from 'react';

export default function AddApplicantModal({ jobTitle = "Senior UX Designer", onClose }) {
  return (
    <div className="bg-white p-8 rounded-xl shadow-lg max-w-lg w-full font-sans">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Add New Applicant for {jobTitle}
      </h2>

      <form onSubmit={(e) => e.preventDefault()}>
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
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500"
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
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500"
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
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500"
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
              placeholder="Phone Number"
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500"
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
            className="px-6 py-2 border border-blue-500 text-blue-500 font-semibold rounded-md hover:bg-blue-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-6 py-2 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Save Applicant
          </button>
        </div>
      </form>
    </div>
  );
};