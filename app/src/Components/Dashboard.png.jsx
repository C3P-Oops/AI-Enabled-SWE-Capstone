import React, { useEffect, useState } from 'react';

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
    default:
      return <span className="text-gray-600 text-sm capitalize">{status}</span>;
  }
};

const jobsData = [
    { title: 'Software Engineer', department: 'New York, NY', status: 'Open', applicants: 85, actions: ['View', 'Edit'] },
    { title: 'Engineering', department: 'New Francisco, CA', status: 'Open', applicants: 0, actions: ['0'] },
    { title: 'Product Manager', department: 'Design', status: 'Draft', applicants: 2, actions: [] },
    { title: 'UX Designer', department: 'London, UK', status: 'Interviewing', applicants: 32, actions: ['View', 'Edit'] },
    { title: 'HR Specialist', department: 'Austin, TX', status: 'Closed', applicants: 110, actions: ['110'] },
    { title: 'Project Lead', department: 'Engineering', status: 'Open', applicants: 55, actions: ['View', 'Edit'] },
    { title: 'Marketing Coordinator', department: 'Berlin Germany', status: 'Open', applicants: 55, actions: ['View', 'Edit'] },
    { title: 'Sydney. AU', department: 'Offer Extended', status: 'Open', applicants: 40, actions: ['View', 'Edit'] },
];

export default function Dashboard({ onJobClick }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchJobs = async() => {
      try {
        const response = await fetch('http://localhost:8081/jobs/');

        if(!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const jobsData = await response.json();
        console.log(jobsData);
        setJobs(jobsData);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching jobs:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchJobs();
  }, []);

  if (loading) {
    return <div className="p-8">Loading jobs...</div>;
  }

  // Handle error state
  if (error) {
    return <div className="p-8 text-red-600">Error: {error}</div>;
  }

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
                placeholder="Search for jobs..."
                className="w-full bg-white border border-slate-300 rounded-lg py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            {/* <button className="flex items-center text-white font-semibold px-4 py-2 rounded-lg shadow-sm transition-colors">
              <PlusIcon className="mr-2" />
              Create New Job Post
            </button> */}
          </div>

          {/* Job Postings Table */}
          <div className="mt-4 bg-white rounded-xl border border-slate-200">
            <h2 className="text-xl font-bold text-slate-800 p-6">Current Job Postings</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left table-fixed">
                <colgroup>
                  <col className="w-1/4" />
                  <col className="w-1/2" />
                  <col className="w-1/4" />
                </colgroup>
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider w-1/4">Job Title</th>
                    <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider w-1/2">Description</th>
                    <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider w-1/4">Created By</th>
                    <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider w-1/4">Department</th>
                    <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider w-1/4">Location</th>
                    <th scope="col" className="px-6 py-3 font-medium text-slate-500 uppercase tracking-wider w-1/4">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {jobs.map((job, index) => (
                    <tr 
                      key={index} 
                      className="hover:bg-slate-50 cursor-pointer transition-colors"
                      onClick={() => onJobClick && onJobClick(job.title)}
                    >
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-slate-900">{job.title}</td>
                      <td className="px-6 py-4 text-slate-600 max-w-xs">
                        <div className="truncate" title={job.description}>
                          {job.description}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-slate-600">{job.created_by_user_id}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-slate-600">{job.department}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-slate-600">{job.location}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <StatusBadge status={job.status} />
                      </td>
                      {/* <td className="px-6 py-4 whitespace-nowrap text-slate-600">{job.applicants}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-slate-600 font-medium">
                        {job.actions.length > 2 ? `${job.actions[0]} | ${job.actions[1]}` : (job.actions.length === 1 ? job.actions[0] : '')}
                      </td> */}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};