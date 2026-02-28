/**
 * Header Component
 * Displays the application logo/title and navigation bar
 * Responsive design: stacks on mobile, horizontal on desktop
 */
export default function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <nav className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        {/* Logo/Title Section */}
        <div className="flex items-center space-x-2">
          <span className="text-3xl">🚀</span>
          <h1 className="text-2xl font-bold">ImageHub</h1>
        </div>

        {/* Navigation Links */}
        <div className="flex space-x-6">
          <a
            href="#home"
            className="hover:text-blue-200 transition duration-200 font-medium focus:outline-none focus:ring-2 focus:ring-blue-300 px-2 py-1 rounded"
          >
            Home
          </a>
          <a
            href="#upload"
            className="hover:text-blue-200 transition duration-200 font-medium focus:outline-none focus:ring-2 focus:ring-blue-300 px-2 py-1 rounded"
          >
            Upload
          </a>
          <a
            href="#about"
            className="hover:text-blue-200 transition duration-200 font-medium focus:outline-none focus:ring-2 focus:ring-blue-300 px-2 py-1 rounded"
          >
            About
          </a>
        </div>
      </nav>
    </header>
  );
}
