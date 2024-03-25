import React from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react'; // Import useAuth0 hook
import { HomePage } from '../pages/HomePage';
import Profile from '../pages/Profile';
import { GamePage } from '../pages/GamePage';
import Admin from '../pages/Admin';
import SuccessPayment from '../pages/SuccessPayment';

function NavbarComp() {
  const { isAuthenticated, loginWithRedirect, logout } = useAuth0(); // Destructure the isAuthenticated, loginWithRedirect, and logout functions

  return (
    <Router>
      <div>
        <Navbar expand="lg" className="bg-body-tertiary">
          <Container>
            <Navbar.Brand href="#home">Kuih Lapis Games</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                <Nav.Link as={Link} to="/">Home</Nav.Link>
                <Nav.Link as={Link} to="/profile">Profile</Nav.Link>
                {/* Conditionally render login or logout button based on authentication status */}
                {isAuthenticated ? (
                  <Nav.Link onClick={() => logout({ returnTo: window.location.origin })}>Logout</Nav.Link>
                ) : (
                  <Nav.Link onClick={() => loginWithRedirect()}>Login</Nav.Link>
                )}
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/game/:gameId" element={<GamePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default NavbarComp;
