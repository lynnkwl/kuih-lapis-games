import React, { Component } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

class Profile extends Component {
  render() {
    return (
      <div>
        <h2>Profile</h2>
        <UserProfile />
      </div>
    );
  }
}

function UserProfile() {
  const { isAuthenticated, user } = useAuth0();

  if (!isAuthenticated) {
    return <div>Please log in to view your profile.</div>;
  }

  return (
    <div>
      <p>Welcome, {user.name}!</p>
      <p>Your email: {user.email}</p>
      <p>Your user ID: {user.sub}</p>
    </div>
  );
}

export default Profile;
