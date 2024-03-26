import React, { useContext } from "react";
import { Link } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import { useCart } from "../context/CartContext"; // Import CartContext to access cart state

export const Game = ({ game }) => {
  const { addToCart } = useCart();
  const handleAddToCart = () => {
    addToCart(game); // Add the game to the cart
  };

  return (
    <div className="game">
      <Card style={{ margin: "10px" }}>
        <Card.Img variant="top" src={game.CoverArt} />
<<<<<<< Updated upstream
        <Card.Body style={{height : '160px'}}>
            <Card.Title><Link to={`/game/${game._id}`}>{game.GameName}</Link></Card.Title>
            <Card.Text>Price: ${game.Price}</Card.Text>
=======
        <Card.Body style={{ height: "160px" }}>
          <Card.Title>
            <Link to={`/game/${game._id}`}>{game.GameName}</Link>
          </Card.Title>
          <Card.Text>Price: ${game.Price}</Card.Text>
          <Button
            style={{ marginRight: "8px" }}
            variant="primary"
          >
            Add to wishlist
          </Button>
          <Button variant="primary" onClick={handleAddToCart}>Add to cart</Button> {/* Call handleAddToCart when the button is clicked */}
>>>>>>> Stashed changes
        </Card.Body>
      </Card>
    </div>
  );
};

