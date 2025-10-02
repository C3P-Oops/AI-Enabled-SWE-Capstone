const LogoIcon = () => (
  <svg className="h-8 w-auto" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 0C31.0457 0 40 8.9543 40 20C40 31.0457 31.0457 40 20 40C8.9543 40 0 31.0457 0 20C0 8.9543 8.9543 0 20 0Z" fill="#4F46E5"/>
    <path d="M25.45 10.9L14.65 29.1H18.6L29.4 10.9H25.45Z" fill="white"/>
    <path d="M10.6 10.9L21.4 29.1H17.45L6.65 10.9H10.6Z" fill="white" fillOpacity="0.5"/>
  </svg>
);

const DocumentIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
);

const ChatIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>
);

const UserIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const PlaceholderIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ChevronDownIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
  </svg>
);

const applicantsData = [
  { id: 1, name: 'Sarah Martinez', date: 'Oct 25, 2025', status: 'Screening', resumeText: 'View', notesText: 'Add Note', isSelected: true },
  { id: 2, name: 'James Liu', date: '', status: 'Screening', resumeText: 'View', notesText: 'Dropdown' },
  { id: 3, name: 'Rachel Green', date: '', status: 'Interview', resumeText: 'View', notesText: 'View Notes' },
  { id: 4, name: 'Rachel Nguyen', date: '', status: 'Screening', resumeText: 'View', notesText: 'View Notes' },
  { id: 5, name: 'Emily Ngulyen', date: '', status: 'Screening', resumeText: 'View', notesText: 'View Notes' },
  { id: 6, name: 'David Chen', date: '', status: 'New', resumeText: 'New', notesText: 'Add Notes' },
  { id: 7, name: 'Sophia Lee', date: '', status: 'Rejected', resumeText: 'Haa', notesText: 'Add Notes' },
  { id: 8, name: 'Alex Brown', date: '', status: 'Offer Extended', resumeText: 'Hired', notesText: 'Add Notes' },
];

const StatusPill = ({ status }) => {
  const baseClasses = 'px-3 py-1 text-xs font-medium rounded-full inline-block';
  let specificClasses = '';

  switch (status.toLowerCase()) {
    case 'screening':
      specificClasses = 'bg-green-100 text-green-800';
      break;
    case 'interview':
      specificClasses = 'bg-orange-100 text-orange-800';
      break;
    case 'new':
      specificClasses = 'bg-blue-100 text-blue-800';
      break;
    case 'rejected':
      specificClasses = 'bg-purple-100 text-purple-800';
      break;
    case 'offer extended':
      specificClasses = 'bg-red-100 text-red-800';
      break;
    default:
      specificClasses = 'bg-gray-100 text-gray-800';
  }

  return <span className={`${baseClasses} ${specificClasses}`}>{status}</span>;
};


const JobDetailsScreen = () => {
  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-800">
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <LogoIcon />
            <h1 className="text-xl font-bold text-gray-800">SmartHire ATS</h1>
          </div>
          <nav className="flex items-center gap-6">
            <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900">Diepd Lloots</a>
            <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900">CestVastes</a>
            <div className="flex items-center gap-3">
              <img
                src="https://i.pravatar.cc/32?u=ceritcotin"
                alt="User avatar"
                className="w-8 h-8 rounded-full"
              />
              <span className="text-sm font-medium text-gray-800">Ceritcotin</span>
            </div>
          </nav>
        </div>
      </header>

      <main className="container mx-auto p-8">
        <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-600">Job Details</h2>
        </div>
        <div className="grid grid-cols-12 gap-8">
          {/* Left Column: Job Details */}
          <div className="col-span-12 lg:col-span-4">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">UI/UX Senior Product Designer</h3>
              
              <div className="space-y-6">
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Description</h4>
                  <ul className="list-disc list-inside text-gray-600 space-y-2 text-sm">
                    <li>We are seeking a talented and experienced UI/UX tating yvut jwist biswd br Frodud Desigeer to <strong>to join ist cespnicralti ncxltlte pitnz join or growing our and growing tesm.</strong></li>
                    <li>a tloest or lbi(t,k) UFS:I to thuls Is aint ato amsiorattsign to on citsicn. tite eg de nod tey in avot olist bito tind aer inted reast.</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Requirements</h4>
                   <ul className="list-disc list-inside text-gray-600 space-y-2 text-sm">
                    <li>5+ years of experience in UI/UX design</li>
                    <li>Proficiency with design tools (<strong>Fijmtch, Adebe XD</strong>)</li>
                    <li>Strong portfsillo</li>
                    <li>Excellent communication skills</li>
                    <li>Bachelor's degree in Design or related field</li>
                  </ul>
                </div>
                 <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Salary</h4>
                  <p className="text-gray-600 text-sm">$120,000 - $166,000 Annually</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Applicants Table */}
          <div className="col-span-12 lg:col-span-8">
            <div className="bg-white rounded-lg shadow-md">
              <div className="p-6 flex justify-between items-center border-b border-gray-200">
                <h3 className="text-xl font-bold text-gray-900">Applicants for UI/UX Senior Product Designer</h3>
                <button className="bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
                  Add New Applicant
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead className="text-xs text-gray-500 uppercase bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 font-medium">Applicant Name</th>
                      <th scope="col" className="px-6 py-3 font-medium">Application Date</th>
                      <th scope="col" className="px-6 py-3 font-medium">Status</th>
                      <th scope="col" className="px-6 py-3 font-medium">Resume/CV</th>
                      <th scope="col" className="px-6 py-3 font-medium">Feedback/Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {applicantsData.map((applicant) => (
                      <tr key={applicant.id} className={`border-b border-gray-200 hover:bg-gray-50 ${applicant.isSelected ? 'bg-blue-50' : 'bg-white'}`}>
                        <td className={`px-6 py-4 font-medium whitespace-nowrap ${applicant.isSelected ? 'text-blue-600 border-l-4 border-blue-600' : 'text-gray-900'}`}>
                          {applicant.name}
                        </td>
                        <td className="px-6 py-4 text-gray-600">{applicant.date}</td>
                        <td className="px-6 py-4"><StatusPill status={applicant.status} /></td>
                        <td className="px-6 py-4">
                            <a href="#" className="flex items-center gap-2 text-gray-600 hover:text-gray-900 font-medium">
                                {applicant.resumeText === 'Hired' && <UserIcon className="w-4 h-4" />}
                                {applicant.resumeText === 'Haa' && <PlaceholderIcon className="w-4 h-4" />}
                                {applicant.resumeText !== 'Hired' && applicant.resumeText !== 'Haa' && <DocumentIcon className="w-4 h-4" />}
                                <span>{applicant.resumeText}</span>
                            </a>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center justify-between">
                            <a href="#" className="flex items-center gap-2 text-gray-600 hover:text-gray-900 font-medium">
                              <ChatIcon className="w-4 h-4" />
                              <span>{applicant.notesText !== 'Dropdown' ? applicant.notesText : 'View'}</span>
                            </a>
                            {applicant.notesText === 'Dropdown' && (
                              <button aria-label="More options">
                                <ChevronDownIcon className="w-5 h-5 text-gray-500" />
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
ReactDOM.render(<JobDetailsScreen />, document.getElementById("root"));