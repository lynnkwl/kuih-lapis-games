// router
import { Link } from "react-router-dom"

export const Game = ({game}) => {

  return (
    <div className="game">
      <img src={game.CoverArt} alt="" />
      <Link to={`/game/${game._id}`}>{game.GameName}</Link>
    </div>
  )
}