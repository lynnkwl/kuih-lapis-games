import React from 'react'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";
import Home from '../pages/Home';
import Profile from '../pages/Profile';
import Admin from '../pages/Admin';
import SuccessPayment from '../pages/SuccessPayment';

function NavbarComp() {
  return (
    <Router>
      <div>
        <Navbar expand="lg" className="bg-body-tertiary">
          <Container>
            <Navbar.Brand href="/">Kuih Lapis Games</Navbar.Brand>
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
                <Nav.Link as={Link} to="/cart" class="ml-auto">Cart
                <Badge pill variant="danger">{cart.length}</Badge> {/* Display the number of items in the cart */}
                </Nav.Link>
                <Nav.Link as={Link} to="/wishlist">Wishlist
                <Badge pill variant="danger">{wishlist.length}</Badge> {/* Display the number of items in the wishlist */}
                </Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/game/:gameId" element={<GamePage />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/wishlist" element={<Wishlist />} />
          <Route path="/successpayment" element={<SuccessPayment />} />
        </Routes>
      </div>
    </Router>
  )
}

export default NavbarComp
