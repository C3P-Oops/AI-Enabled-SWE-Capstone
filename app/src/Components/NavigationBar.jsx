const LogoIcon = () => (
  <svg className="h-8 w-auto" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 0C31.0457 0 40 8.9543 40 20C40 31.0457 31.0457 40 20 40C8.9543 40 0 31.0457 0 20C0 8.9543 8.9543 0 20 0Z" fill="#4F46E5"/>
    <path d="M25.45 10.9L14.65 29.1H18.6L29.4 10.9H25.45Z" fill="white"/>
    <path d="M10.6 10.9L21.4 29.1H17.45L6.65 10.9H10.6Z" fill="white" fillOpacity="0.5"/>
  </svg>
);

export default function NavigationBar({ currentPage, setCurrentPage }) {
    return (
        <header className="bg-white shadow-sm sticky top-0 z-50">
            <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                <div className="flex items-center space-x-3">
                    <LogoIcon />
                    <h1 className="text-2xl font-bold text-gray-800">SmartHire ATS</h1>
                </div>

                <nav>
                    <ul className="flex items-center space-x-8">
                        <li>
                            <button 
                                onClick={() => setCurrentPage('home')}
                                className={`text-gray-600 hover:text-blue-600 ${currentPage === 'home' ? 'text-blue-600 font-semibold' : ''}`}
                            >
                                Dashboard
                            </button>
                        </li>
                        <li>
                            <button 
                                onClick={() => setCurrentPage('about')}
                                className={`text-gray-600 hover:text-blue-600 ${currentPage === 'about' ? 'text-blue-600 font-semibold' : ''}`}
                            >
                                About Us
                            </button>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>
    )
}