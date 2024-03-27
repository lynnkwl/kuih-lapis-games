
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarComp from './components/NavbarComp';
import { CartProvider } from './context/CartContext';
import { WishlistProvider } from './context/WishlistContext';

function App() {
  return (
    <WishlistProvider>
    <CartProvider>
    <div className="App">
      <>
        <NavbarComp/>
      </>

    </div>
    </CartProvider>
    </WishlistProvider>
  );
}

export default App;