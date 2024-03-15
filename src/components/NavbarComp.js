import React from 'react'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";
import Home from '../pages/Home';
import Profile from '../pages/Profile';
import Admin from '../pages/Admin';

function NavbarComp() {
  return (
    <Router>
    <div>
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="#home">Kuih Lapis Games</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to ={"/"}>Home</Nav.Link>
            <Nav.Link  as={Link} to ={"/profile"}>Profile</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    <Routes>
      <Route path="/" element={<Home />}/>
      <Route path="/profile" element={<Profile />}/>
      <Route path="/admin" element={<Admin />}/>
    </Routes>
    </div>
    </Router>
  )
}

export default NavbarComp
