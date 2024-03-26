import React, { createContext, useState, useContext } from "react";

// Create the CartContext
const CartContext = createContext();

// Create a provider component
export const CartProvider = ({ children }) => {
    const [cart, setCart] = useState(() => {
      const localData = localStorage.getItem('cart');
      return localData ? JSON.parse(localData) : [];
    });
  
    const addToCart = (item) => {
      const newCart = [...cart, item];
      setCart(newCart);
      localStorage.setItem('cart', JSON.stringify(newCart));
    };
  
    const removeFromCart = (index) => {
      const newCart = [...cart];
      newCart.splice(index, 1);
      setCart(newCart);
      localStorage.setItem('cart', JSON.stringify(newCart));
    };
  
    return (
      <CartContext.Provider value={{ cart, addToCart, removeFromCart }}>
        {children}
      </CartContext.Provider>
    );
  };

// Custom hook to use the CartContext
export const useCart = () => {
  return useContext(CartContext);
};


