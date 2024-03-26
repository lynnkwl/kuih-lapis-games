import React, { useContext } from "react";
import { Link } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";

export const Game = ({ game }) => {

  return (
    <div className="game">
      <Card style={{ margin: "10px" }}>
        <Card.Img variant="top" src={game.CoverArt} />
        <Card.Body style={{ height: "160px" }}>
          <Card.Title>
            <Link to={`/game/${game._id}`}>{game.GameName}</Link>
          </Card.Title>
          <Card.Text>Price: ${game.Price}</Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
};

