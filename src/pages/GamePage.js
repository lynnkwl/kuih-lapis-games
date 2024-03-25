import { useState, useEffect } from "react"
import axios from "axios"

// router
import { useParams } from "react-router-dom";

export const GamePage = () => {

    const { gameId } = useParams();

    const [ game, setGame ] = useState([]);
   
	
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
	
    <div className="game-page">
        <img src={game.CoverArt} alt=""/>
        <h1>{game.GameName}</h1>
        <h2>Publisher: {game.Publisher}</h2>
        <p>{game.Description }</p>
    </div>
  )
}