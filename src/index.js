import React from 'react';
import { Auth0Provider } from '@auth0/auth0-react'; // Import Auth0Provider
import ReactDOM from 'react-dom';
import './index.css';
import App from './App'; // Import your main application component
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    {/* Wrap your entire application with Auth0Provider */}
    <Auth0Provider
      domain="dev-n5qeqzcjfl6nyhqa.us.auth0.com"
      clientId="E4ANzHR9fQ7ycRnqDTKdDtbumTl5aoqA"
      redirectUri={window.location.origin}
    >
      <App />
    </Auth0Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

reportWebVitals();
