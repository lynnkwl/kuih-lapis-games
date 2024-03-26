import React from 'react';
import { useCart } from '../context/CartContext';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

const Cart = () => {
  const { cart, removeFromCart } = useCart();

  const handleRemoveFromCart = (index) => {
    removeFromCart(index);
  };
  const handleOutputJson = () => {
    console.log(JSON.stringify(cart));
  };

  return (
    <div>
      <h2>Your Cart</h2>
      {cart.length === 0 ? (
        <p>Your cart is empty</p>
      ) : (
        cart.map((game, index) => (
          <div className="game" key={index}>
            <Card style={{ margin: "10px" }}>
              <Card.Img variant="top" src={game.CoverArt} />
              <Card.Body style={{ height: "160px" }}>
                <Card.Title>
                  <Link to={`/game/${game._id}`}>{game.GameName}</Link>
                </Card.Title>
                <Card.Text>Price: ${game.Price}</Card.Text>
                <Button variant="primary" onClick={() => handleRemoveFromCart(index)}>Remove from cart</Button>
              </Card.Body>
            </Card>
            
          </div>
          
        ))
      )}
      <Button variant="primary" onClick={handleOutputJson}>Output JSON</Button>
    </div>
  );
};

export default Cart;