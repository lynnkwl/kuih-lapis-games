
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarComp from './components/NavbarComp';
import { CartProvider } from './context/CartContext';

function App() {
  return (
    <CartProvider>
    <div className="App">
      <>
        <NavbarComp/>
      </>

    </div>
    </CartProvider>
  );
}

export default App;