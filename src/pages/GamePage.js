import { useState, useEffect } from "react"
import axios from "axios"
import { Card, ListGroup, Container, Row, Col, Image, Button } from 'react-bootstrap';
import { useCart } from "../context/CartContext";
import {useWishlist} from "../context/WishlistContext";

// router
import { useParams } from "react-router-dom";

export const GamePage = () => {

    const { gameId } = useParams();

    const [ game, setGame ] = useState([]);
	
	const { addToCart } = useCart();
	const handleAddToCart = () => {
	  addToCart(game); // Add the game to the cart
	};
    
	const { addToWishlist } = useWishlist();
	const handleAddToWishlist = () => {
	  addToWishlist(game); // Add the game to the wishlist
	};
	
	useEffect(() => {
		const handleGameList = () => {
			const options = {
				method: 'GET',
				url: 'http://localhost:4300/api/getgame/' + gameId,
			};
			axios.request(options).then(function(response){
				setGame(response.data);
			}).catch(function (error) {
				console.error(error);
			})
		}
		handleGameList();
	}, [ gameId ])

  return (
	<Container className="mt-5">
	<Row className="justify-content-center">
	  <Col md={6}>
		<Card>
		  <Card.Header as="h5">{game.GameName}</Card.Header>
		  <Row noGutters>
			<Col md={6}>
			  <Image src={game.CoverArt} alt={game.GameName} fluid rounded />
			</Col>
			<Col md={6}>
			  <ListGroup variant="flush">
				<ListGroup.Item>Publisher: {game.Publisher}</ListGroup.Item>
				<ListGroup.Item>{game.Description}</ListGroup.Item>
			  </ListGroup>
			  <Button
            style={{ marginRight: "8px" }}
            variant="primary" onClick={handleAddToWishlist}
          >
            Add to wishlist
          </Button>
          <Button variant="primary" onClick={handleAddToCart}>Add to cart</Button> {/* Call handleAddToCart when the button is clicked */}
			</Col>
		  </Row>
		</Card>
	  </Col>
	</Row>
  </Container>
  )
}