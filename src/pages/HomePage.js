import { useState, useEffect } from "react";
import axios from 'axios';

import {Game} from '../components/Game'

export const HomePage = () => {

    const [ games, setGames ] = useState([]);
	
	useEffect(() => {
		const handleGameList = () => {
			const options = {
				method: 'GET',
				url: 'http://localhost:4300/api/games',
			};
			axios.request(options).then(function(response){
				setGames(response.data);
			}).catch(function (error) {
				console.error(error);
			})
		}
		handleGameList();
	}, [])

        return (
            <div className="home">
				{games.map((game, index) => {
					// Calculate row and column indexes
					const row = Math.floor(index / 3);
					const col = index % 3;

					// Define styles for grid positioning
					const style = {
						gridColumn: col + 1,
						gridRow: row + 1
					};

					return (
						<div key={index} className="game" style={style}>
							<Game game={game} />
						</div>
					);
				})}
			</div>

        )
      }