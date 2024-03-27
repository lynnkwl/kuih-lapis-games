import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useWishlist } from '../context/WishlistContext'; // import the WishlistContext

const Wishlist = () => {
  const { wishlist, removeFromWishlist } = useWishlist(); // use the WishlistContext

  const handleRemoveFromWishlist = (index) => {
    removeFromWishlist(index);
  };

  return (
    <div>
      <h2>Your Wishlist</h2>
      {wishlist.length === 0 ? (
        <p>Your wishlist is empty</p>
      ) : (
        wishlist.map((game, index) => (
          <div className="game" key={index}>
            <Card style={{ margin: "10px" }}>
              <Card.Img variant="top" src={game.CoverArt} />
              <Card.Body style={{ height: "160px" }}>
                <Card.Title>
                  <Link to={`/game/${game._id}`}>{game.GameName}</Link>
                </Card.Title>
                <Card.Text>Price: ${game.Price}</Card.Text>
                <Button variant="primary" onClick={() => handleRemoveFromWishlist(index)}>Remove from wishlist</Button>
              </Card.Body>
            </Card>
          </div>
        ))
      )}
    </div>
  );
};

export default Wishlist;