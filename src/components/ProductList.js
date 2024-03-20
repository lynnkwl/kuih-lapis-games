import React from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default class ProductList extends React.Component {
    state = {
      games: []
    }
  
    componentDidMount() {
      axios.get(`http://localhost:4000/api/games`)
        .then(res => {
          const games = res.data;
          this.setState({ games });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }
    
    render() {
        const chunkSize = 4;
        const gameChunks = this.state.games.reduce((resultArray, item, index) => {
            const chunkIndex = Math.floor(index / chunkSize);
            if (!resultArray[chunkIndex]) {
                resultArray[chunkIndex] = []; // start a new chunk
            }
            resultArray[chunkIndex].push(item);
            return resultArray;
        }, []);

        return (
            <div>
                {gameChunks.map((chunk, index) => (
                <Row key={index}>
                    {chunk.map(game => (
                    <Col key={game._id} md={3}>
                        <Card style={{ margin: '10px' }}>
                        <Card.Img variant="top" src={game.CoverArt} />
                        <Card.Body style={{height : '160px'}}>
                            <Card.Title>{game.GameName}</Card.Title>
                            <Card.Text>Price: ${game.Price}</Card.Text>
                            <Button variant="primary">Go somewhere</Button>
                        </Card.Body>
                        </Card>
                    </Col>
                    ))}
                </Row>
                ))}
            </div>
        )
      }
    }