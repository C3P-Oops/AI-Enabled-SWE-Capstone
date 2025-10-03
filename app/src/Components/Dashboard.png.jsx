import React, { useState, useEffect, useRef } from 'react';

// API configuration
const API_BASE_URL = 'http://localhost:8081';

// Icon components (as they would be in a real app, but defined here for self-containment)
const UsersIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.653-.122-1.28-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.653.122-1.28.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
  </svg>
);

const DocumentTextIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
);

const BriefcaseIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>
);

const ClockIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const BellIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
  </svg>
);

const UserCircleIcon = (props) => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor" {...props}>
        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clipRule="evenodd" />
    </svg>
);

const SearchIcon = (props) => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} {...props}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
);

const PlusIcon = (props) => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" {...props}>
        <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
);


const StatusBadge = ({ status }) => {
  const baseClasses = "inline-flex items-center px-3 py-1 rounded-full text-xs font-medium capitalize";
  switch (status.toLowerCase()) {
    case 'open':
      return <span className={`${baseClasses} bg-green-100 text-green-800`}>{status}</span>;
    case 'draft':
      return <span className={`${baseClasses} bg-blue-100 text-blue-800`}>{status}</span>;
    case 'closed':
      return <span className={`${baseClasses} bg-red-100 text-red-800`}>{status}</span>;
    case 'interviewing':
      return <span className={`${baseClasses} bg-orange-100 text-orange-800`}>{status}</span>;
    case 'screening':
      return <span className={`${baseClasses} bg-yellow-100 text-yellow-800`}>{status}</span>;
    case 'pending':
      return <span className={`${baseClasses} bg-purple-100 text-purple-800`}>{status}</span>;
    case 'paused':
      return <span className={`${baseClasses} bg-gray-100 text-gray-800`}>{status}</span>;
    case 'filled':
      return <span className={`${baseClasses} bg-emerald-100 text-emerald-800`}>{status}</span>;
    default:
      return <span className={`${baseClasses} bg-slate-100 text-slate-800`}>{status}</span>;
  }
};

// API utility functions
const fetchJobs = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching jobs:', error);
    throw error;
  }
};

const fetchApplicationsForJob = async (jobId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/applications/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const applications = await response.json();
    return applications.filter(app => app.job_id === jobId);
  } catch (error) {
    console.error('Error fetching applications:', error);
    return [];
  }
};

// Transform backend data to match frontend expectations
const transformJobData = (jobs, applicationsData) => {
  return jobs.map(job => {
    const applications = applicationsData[job.job_id] || [];
    const applicantCount = applications.length;
    
    // Map job titles to departments based on common patterns
    let department = 'Not specified';
    const title = job.title.toLowerCase();
    
    if (title.includes('engineer') || title.includes('developer') || title.includes('devops') || title.includes('qa')) {
      department = 'Engineering';
    } else if (title.includes('product manager') || title.includes('product')) {
      department = 'Product';
    } else if (title.includes('designer') || title.includes('ux') || title.includes('ui')) {
      department = 'Design';
    } else if (title.includes('data scientist') || title.includes('data') || title.includes('analyst')) {
      department = 'Data & Analytics';
    } else if (title.includes('marketing') || title.includes('sales')) {
      department = 'Marketing & Sales';
    } else if (title.includes('hr') || title.includes('human resources')) {
      department = 'Human Resources';
    } else if (title.includes('security') || title.includes('cybersecurity')) {
      department = 'Security';
    } else if (title.includes('writer') || title.includes('technical writer')) {
      department = 'Documentation';
    } else if (title.includes('architect') || title.includes('cloud')) {
      department = 'Architecture';
    }
    
    // Determine status based on job data or default to 'Open'
    let status = 'Open';
    if (applicantCount === 0) {
      status = 'Open';
    } else if (applications.some(app => app.status === 'interviewing')) {
      status = 'Interviewing';
    }

    return {
      job_id: job.job_id,
      title: job.title,
      department: department,
      status: status,
      applicants: applicantCount,
      actions: applicantCount > 0 ? ['View', 'Edit'] : ['View']
    };
  });
};

// Helper function to highlight search terms
const highlightSearchTerm = (text, searchTerm) => {
  if (!searchTerm.trim()) return text;
  
  const regex = new RegExp(`(${searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  const parts = text.split(regex);
  
  return parts.map((part, index) => 
    regex.test(part) ? (
      <mark key={index} className="bg-yellow-200 text-yellow-900 px-1 rounded">
        {part}
      </mark>
    ) : part
  );
};

export default function Dashboard({ onJobClick }) {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const searchInputRef = useRef(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch jobs and applications
        const jobsData = await fetchJobs();
        
        // Fetch applications for each job
        const applicationsData = {};
        await Promise.all(
          jobsData.map(async (job) => {
            applicationsData[job.job_id] = await fetchApplicationsForJob(job.job_id);
          })
        );
        
        // Transform data for the UI
        const transformedJobs = transformJobData(jobsData, applicationsData);
        setJobs(transformedJobs);
        setFilteredJobs(transformedJobs); // Initialize filtered jobs
      } catch (err) {
        setError(err.message);
        console.error('Failed to load dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Filter jobs based on search term
  useEffect(() => {
    if (!searchTerm.trim()) {
      setFilteredJobs(jobs);
    } else {
      const filtered = jobs.filter(job => 
        job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.status.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredJobs(filtered);
    }
    // Reset to first page when search changes
    setCurrentPage(1);
  }, [searchTerm, jobs]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  // Pagination calculations
  const totalPages = Math.ceil(filteredJobs.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentJobs = filteredJobs.slice(startIndex, endIndex);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handlePrevPage = () => {
    setCurrentPage(prev => Math.max(prev - 1, 1));
  };

  const handleNextPage = () => {
    setCurrentPage(prev => Math.min(prev + 1, totalPages));
  };

  // Add keyboard shortcut to focus search (Ctrl+K or Cmd+K)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);
  return (
    <div className="bg-slate-100 min-h-screen flex justify-center font-sans">
      <div className="w-full max-w-7xl bg-white rounded-2xl shadow-lg flex min-h-[800px]">

        {/* Main Content */}
        <main className="flex-1 p-8">
          {/* Search and Actions */}
          <div className="flex justify-between items-center my-6">
            <div className="relative w-full max-w-sm">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <SearchIcon className="text-slate-400" />
              </div>
              <input
                type="text"
                ref={searchInputRef}
                placeholder="Search jobs by title, description, or status... (Ctrl+K)"
                value={searchTerm}
                onChange={handleSearchChange}
                style={{ 
                  color: '#1f2937', 
                  backgroundColor: 'white',
                  fontSize: '14px'
                }}
                className="w-full bg-white border border-slate-300 rounded-lg py-2 pl-10 pr-4 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {searchTerm && (
                <button
                  onClick={() => setSearchTerm('')}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
                >
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
          </div>

          {/* Job Postings Table */}
          <div className="mt-2 bg-white rounded-xl border border-slate-200">
            <div className="p-6 border-b border-slate-200">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-slate-800">Current Job Postings</h2>
                {searchTerm && (
                  <div className="text-sm text-slate-600">
                    {filteredJobs.length} of {jobs.length} jobs match "{searchTerm}"
                  </div>
                )}
                {!searchTerm && filteredJobs.length > 0 && (
                  <div className="text-sm text-slate-600">
                    Showing {startIndex + 1}-{Math.min(endIndex, filteredJobs.length)} of {filteredJobs.length} jobs
                  </div>
                )}
              </div>
            </div>
            
            {loading && (
              <div className="flex justify-center items-center p-8">
                <div className="text-slate-600">Loading jobs...</div>
              </div>
            )}
            
            {error && (
              <div className="mx-6 mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                <strong>Error:</strong> {error}
                <div className="text-sm mt-2">
                  Make sure the backend server is running on http://localhost:8081
                </div>
              </div>
            )}
            
            {!loading && !error && jobs.length === 0 && (
              <div className="p-8 text-center text-slate-600">
                No jobs found. Create your first job posting!
              </div>
            )}

            {!loading && !error && jobs.length > 0 && filteredJobs.length === 0 && searchTerm && (
              <div className="p-8 text-center text-slate-600">
                <div className="flex flex-col items-center">
                  <SearchIcon className="w-12 h-12 text-slate-300 mb-4" />
                  <p className="text-lg font-medium">No jobs match your search</p>
                  <p className="text-sm">Try searching for different keywords or clear your search to see all jobs.</p>
                  <button
                    onClick={() => setSearchTerm('')}
                    className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Clear Search
                  </button>
                </div>
              </div>
            )}
            
            {!loading && !error && filteredJobs.length > 0 && (
              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider">Job Title</th>
                      <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider">Department</th>
                      <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider">Status</th>
                      <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider">Applicants</th>
                      <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200">
                    {currentJobs.map((job, index) => (
                      <tr 
                        key={job.job_id || index} 
                        className="hover:bg-slate-50 cursor-pointer transition-colors"
                        onClick={() => {
                          console.log('Dashboard: Job clicked:', { jobId: job.job_id, title: job.title });
                          onJobClick && onJobClick(job.job_id, job.title);
                        }}
                      >
                        <td className="px-6 py-4 whitespace-nowrap font-medium text-slate-900">
                          {highlightSearchTerm(job.title, searchTerm)}
                        </td>
                        <td className="px-6 py-4 text-slate-600" style={{maxWidth: '300px'}}>
                          <div className="truncate">
                            {highlightSearchTerm(job.department, searchTerm)}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <StatusBadge status={job.status} />
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-slate-600">{job.applicants}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-slate-600 font-medium">
                          {job.actions.length > 1 ? `${job.actions[0]} | ${job.actions[1]}` : (job.actions.length === 1 ? job.actions[0] : '')}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Pagination */}
            {!loading && !error && filteredJobs.length > itemsPerPage && (
              <div className="px-6 py-6 border-t border-slate-200 bg-slate-50">
                <div className="flex flex-col items-center space-y-4">
                  <div className="text-sm text-slate-600 font-medium">
                    Showing {startIndex + 1} to {Math.min(endIndex, filteredJobs.length)} of {filteredJobs.length} results
                  </div>
                  <div className="flex items-center space-x-1">
                    <button
                      onClick={handlePrevPage}
                      disabled={currentPage === 1}
                      className={`px-4 py-2 text-sm font-medium rounded-lg bg-transparent focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 transition-all duration-200 ${
                        currentPage === 1 
                          ? 'text-gray-400 cursor-not-allowed' 
                          : 'text-slate-700 hover:text-slate-900'
                      }`}
                    >
                      ← Previous
                    </button>
                    
                    <div className="flex space-x-1 mx-4">
                      {[...Array(totalPages)].map((_, index) => {
                        const pageNumber = index + 1;
                        const isCurrentPage = pageNumber === currentPage;
                        
                        // Show first page, last page, current page, and pages around current page
                        if (
                          pageNumber === 1 ||
                          pageNumber === totalPages ||
                          (pageNumber >= currentPage - 1 && pageNumber <= currentPage + 1)
                        ) {
                          return (
                            <button
                              key={pageNumber}
                              onClick={() => handlePageChange(pageNumber)}
                              className={`w-10 h-10 text-sm font-medium rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 ${
                                isCurrentPage
                                  ? 'bg-blue-600 text-white shadow-md hover:bg-blue-700'
                                  : 'bg-transparent text-slate-700 hover:text-slate-900'
                              }`}
                            >
                              {pageNumber}
                            </button>
                          );
                        } else if (
                          pageNumber === currentPage - 2 ||
                          pageNumber === currentPage + 2
                        ) {
                          return (
                            <div key={pageNumber} className="flex items-center px-2">
                              <span className="text-slate-400 font-medium">⋯</span>
                            </div>
                          );
                        }
                        return null;
                      })}
                    </div>
                    
                    <button
                      onClick={handleNextPage}
                      disabled={currentPage === totalPages}
                      className={`px-4 py-2 text-sm font-medium rounded-lg bg-transparent focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 transition-all duration-200 ${
                        currentPage === totalPages 
                          ? 'text-gray-400 cursor-not-allowed' 
                          : 'text-slate-700 hover:text-slate-900'
                      }`}
                    >
                      Next →
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};