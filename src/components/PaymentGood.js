import React from 'react';
import logo from '../assets/7efs.gif';
import Button from 'react-bootstrap/Button';



const PaymentGood = () => {
    return (
        <div>
            <img src={logo} alt="Tick" />
            <h2 className="mb-5">Payment confirmed</h2>
            <Button onClick={() => window.location.href = '/'}>Return to home</Button>
        </div>
    );
};

export default PaymentGood;