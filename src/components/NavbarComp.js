import React from 'react'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";
import Home from '../pages/Home'
import Profile from '../pages/Profile'

function NavbarComp() {
  return (
    <Router>
    <div>
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to ={"/home"}>Home</Nav.Link>
            <Nav.Link  as={Link} to ={"/profile"}>Profile</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    <Routes>
      <Route path="/home" element={<Home />}/>
      <Route path="/profile" element={<Profile />}/>
    </Routes>
    </div>
    </Router>
  )
}

export default NavbarComp
