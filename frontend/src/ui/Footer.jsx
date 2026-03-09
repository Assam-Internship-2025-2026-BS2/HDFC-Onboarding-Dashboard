import React from "react";

export default function Footer() {
  return (
    <footer className="footer-section">
      <div className="footer-content">
        <div className="footer-left">
          <p>&copy; {new Date().getFullYear()} HDFC Bank Ltd. All rights reserved.</p>
        </div>
        <div className="footer-right">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Service</a>
          <a href="#">Help Center</a>
        </div>
      </div>
    </footer>
  );
}
