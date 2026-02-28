/**
 * Footer Component
 * Simple footer with copyright and additional links
 * Responsive: adjusts padding and text size on mobile
 */
export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-gray-300 mt-16">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="border-t border-gray-700 pt-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-6">
            {/* About Section */}
            <div>
              <h3 className="text-white font-bold mb-3">About</h3>
              <p className="text-sm text-gray-400">
                ImageHub is a modern image management platform for uploading and organizing your photos.
              </p>
            </div>

            {/* Links Section */}
            <div>
              <h3 className="text-white font-bold mb-3">Links</h3>
              <ul className="text-sm space-y-2">
                <li>
                  <a href="#privacy" className="hover:text-white transition duration-200">
                    Privacy Policy
                  </a>
                </li>
                <li>
                  <a href="#terms" className="hover:text-white transition duration-200">
                    Terms of Service
                  </a>
                </li>
                <li>
                  <a href="#contact" className="hover:text-white transition duration-200">
                    Contact Us
                  </a>
                </li>
              </ul>
            </div>

            {/* Social Section */}
            <div>
              <h3 className="text-white font-bold mb-3">Follow Us</h3>
              <div className="flex space-x-4">
                <a href="#twitter" className="hover:text-blue-400 transition duration-200" aria-label="Twitter">
                  Twitter
                </a>
                <a href="#github" className="hover:text-gray-100 transition duration-200" aria-label="GitHub">
                  GitHub
                </a>
              </div>
            </div>
          </div>

          {/* Copyright */}
          <div className="border-t border-gray-700 pt-6 text-center text-sm">
            <p>&copy; {currentYear} ImageHub. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
}
