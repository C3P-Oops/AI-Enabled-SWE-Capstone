import React from 'react';

// SVG Icons (defined as functional components for clarity)
const LightBulbIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={props.className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
  </svg>
);

const HandshakeIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={props.className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.875 9.168-4.684C19.486 4.414 21 7.433 21 11c0 3.567-1.514 6.586-3.832 7.684a.75.75 0 01-.836-.342l-3.236-5.235A3 3 0 0012 11H7a4 4 0 01-1.564 3.683z" />
  </svg>
);

const ShieldIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={props.className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.286zm0 13.036h.008v.008h-.008v-.008z" />
  </svg>
);

// Data for sections
const values = [
  {
    icon: <LightBulbIcon className="h-12 w-12 text-blue-600 mb-4" />,
    title: "Innovation",
    description: "Pushing boundaries, smarter solutions",
  },
  {
    icon: <HandshakeIcon className="h-12 w-12 text-blue-600 mb-4" />,
    title: "Collaboration",
    description: "Building success through teamwork partnership",
  },
  {
    icon: <ShieldIcon className="h-12 w-12 text-blue-600 mb-4" />,
    title: "Integrity",
    description: "Acting with honesty transparency",
  },
];

const teamMembers = [
  {
    name: "Sarah Martinez",
    role: "HR Manager",
    imageUrl: "https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=250&q=80",
  },
  {
    name: "James Liu",
    role: "Recruiter",
    imageUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=250&q=80",
  },
  {
    name: "Rachel Green",
    role: "Hiring Manager",
    imageUrl: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=250&q=80",
  },
  {
    name: "Emily Nguyen",
    role: "Project Manager",
    imageUrl: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=250&q=80",
  },
];

const AboutUsPage = () => {
  return (
    <div className="bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">SmartHire ATS</h1>
          <nav>
            <ul className="flex items-center space-x-8">
              <li><a href="#" className="text-gray-600 hover:text-blue-600">Home</a></li>
              <li><a href="#" className="text-gray-600 hover:text-blue-600">Features</a></li>
              <li><a href="#" className="text-blue-600 font-semibold">About Us</a></li>
              <li><a href="#" className="text-gray-600 hover:text-blue-600">Blog</a></li>
              <li><a href="#" className="text-gray-600 hover:text-blue-600">Contact</a></li>
            </ul>
          </nav>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="relative h-[450px] text-white">
          <img
            src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1742&q=80"
            alt="A team of professionals in a meeting room"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black bg-opacity-40" />
          <div className="absolute inset-0 flex items-center">
            <div className="container mx-auto px-6">
              <h2 className="text-5xl md:text-6xl font-bold tracking-tight">
                Transforming <br />
                Hiring, Together
              </h2>
            </div>
          </div>
        </section>

        {/* Our Story Section */}
        <section className="py-24 bg-white">
          <div className="container mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
              <div>
                <h3 className="text-3xl font-bold text-gray-900 mb-4">Our Story</h3>
                <p className="text-gray-600 mb-4 leading-relaxed">
                  SmartHire ATS was founded on the principle of making recruitment intuitive, efficient, and human-centric.
                </p>
                <p className="text-gray-600 leading-relaxed">
                  From humble beginnings, we've grown into a trusted partner for organizations worldwide, driven by a shared passion for innovation and a commitment to excellence.
                </p>
              </div>
              <div>
                <img
                  src="https://images.unsplash.com/photo-1556761175-5973dc0f32e7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1932&q=80"
                  alt="Modern office interior with the SmartHire logo"
                  className="rounded-lg shadow-xl w-full"
                />
              </div>
            </div>
          </div>
        </section>

        {/* Wavy Background Section for Values */}
        <div className="relative">
          {/* Top Wave */}
          <div className="absolute top-0 w-full h-24 bg-white">
            <svg viewBox="0 0 1440 100" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" className="w-full h-full">
              <path d="M0 100V0C480 100 960 0 1440 100V100H0Z" fill="#f0f9ff"></path>
            </svg>
          </div>

          {/* Our Values Section */}
          <section className="bg-sky-50 pt-32 pb-24">
            <div className="container mx-auto px-6 text-center">
              <h3 className="text-3xl font-bold text-gray-900 mb-16">Our Values</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                {values.map((value) => (
                  <div key={value.title} className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
                    {value.icon}
                    <h4 className="text-xl font-semibold text-gray-800 mb-2">{value.title}</h4>
                    <p className="text-gray-600">{value.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Bottom Wave */}
          <div className="absolute bottom-0 w-full h-24 bg-white -mb-1">
             <svg viewBox="0 0 1440 100" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" className="w-full h-full transform rotate-180">
              <path d="M0 100V0C480 100 960 0 1440 100V100H0Z" fill="#f0f9ff"></path>
            </svg>
          </div>
        </div>


        {/* Meet the Team Section */}
        <section className="py-24 bg-white">
          <div className="container mx-auto px-6 text-center">
            <h3 className="text-3xl font-bold text-gray-900 mb-16">Meet the Team</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-x-8 gap-y-12">
              {teamMembers.map((member) => (
                <div key={member.name} className="flex flex-col items-center">
                  <img
                    src={member.imageUrl}
                    alt={`Portrait of ${member.name}`}
                    className="w-32 h-32 object-cover rounded-full mb-4 shadow-lg border-4 border-white"
                  />
                  <h4 className="text-lg font-semibold text-gray-800">{member.name}</h4>
                  <p className="text-gray-500">{member.role}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

      </main>
    </div>
  );
};

export default AboutUsPage;