jsx
// src/App.js
import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import Menu from './components/Menu';
import Cart from './components/Cart';

// Replace 'pk_test_TYooMQauvdEDq5DRpFSxPsmh' with your actual Stripe publishable key
// Get your key from the Stripe Dashboard: Developers -> API Keys
const stripePromise = loadStripe('pk_test_TYooMQauvdEDq5DRpFSxPsmh');

// Dummy Menu Items (in a real app, these would be fetched from an API)
const dummyMenuItems = [
  { id: '1', name: 'Margherita Pizza', price: 12.99, description: 'Classic cheese and tomato pizza' },
  { id: '2', name: 'Pepperoni Pizza', price: 14.50, description: 'Pizza with spicy pepperoni' },
  { id: '3', name: 'Vegan Burger', price: 11.00, description: 'Plant-based burger with fresh toppings' },
  { id: '4', name: 'Chicken Salad', price: 9.75, description: 'Grilled chicken, mixed greens, and vinaigrette' },
  { id: '5', name: 'Soda', price: 2.00, description: 'Refreshing carbonated drink' },
  { id: '6', name: 'Water', price: 1.50, description: 'Bottled still water' },
];

export default function App() {
  const [menuItems, setMenuItems] = useState([]);
  // cartItems stores items as { itemId: { item: {id, name, price}, quantity: N } }
  const [cartItems, setCartItems] = useState({});

  useEffect(() => {
    // Simulate fetching menu items on component mount
    setMenuItems(dummyMenuItems);
  }, []);

  const handleAddToCart = useCallback((itemToAdd) => {
    setCartItems(prevCartItems => {
      const existingItem = prevCartItems[itemToAdd.id];
      if (existingItem) {
        return {
          ...prevCartItems,
          [itemToAdd.id]: {
            ...existingItem,
            quantity: existingItem.quantity + 1,
          },
        };
      } else {
        return {
          ...prevCartItems,
          [itemToAdd.id]: {
            item: itemToAdd,
            quantity: 1,
          },
        };
      }
    });
  }, []);

  const handleUpdateCartQuantity = useCallback((itemId, newQuantity) => {
    setCartItems(prevCartItems => {
      if (newQuantity <= 0) {
        const newItems = { ...prevCartItems };
        delete newItems[itemId];
        return newItems;
      }
      return {
        ...prevCartItems,
        [itemId]: {
          ...prevCartItems[itemId],
          quantity: newQuantity,
        },
      };
    });
  }, []);

  const cartTotal = useMemo(() => {
    return Object.values(cartItems).reduce((total, cartItem) => {
      return total + cartItem.item.price * cartItem.quantity;
    }, 0);
  }, [cartItems]);

  const cartItemsArray = useMemo(() => Object.values(cartItems), [cartItems]);

  return (
    <Elements stripe={stripePromise}>
      <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: '1200px', margin: '20px auto', display: 'flex', gap: '20px' }}>
        <div style={{ flex: 2 }}>
          <h1 style={{ textAlign: 'center', color: '#333' }}>Our Menu</h1>
          <Menu menuItems={menuItems} onAddToCart={handleAddToCart} />
        </div>
        <div style={{ flex: 1, borderLeft: '1px solid #eee', paddingLeft: '20px' }}>
          <h1 style={{ textAlign: 'center', color: '#333' }}>Your Cart</h1>
          <Cart
            cartItems={cartItemsArray}
            onUpdateQuantity={handleUpdateCartQuantity}
            cartTotal={cartTotal}
          />
        </div>
      </div>
    </Elements>
  );
}

// src/components/Menu.jsx
import React from 'react';
import MenuItem from './MenuItem';

export default function Menu({ menuItems, onAddToCart }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
      {menuItems.map(item => (
        <MenuItem key={item.id} item={item} onAddToCart={onAddToCart} />
      ))}
    </div>
  );
}

// src/components/MenuItem.jsx
import React from 'react';

export default function MenuItem({ item, onAddToCart }) {
  return (
    <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '15px', textAlign: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
      <h3 style={{ color: '#555', marginBottom: '10px' }}>{item.name}</h3>
      <p style={{ fontSize: '1.1em', fontWeight: 'bold', color: '#333', marginBottom: '10px' }}>${item.price.toFixed(2)}</p>
      <p style={{ color: '#777', fontSize: '0.9em', minHeight: '40px' }}>{item.description}</p>
      <button
        onClick={() => onAddToCart(item)}
        style={{
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          padding: '10px 15px',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '15px',
          fontSize: '1em',
        }}
      >
        Add to Cart
      </button>
    </div>
  );
}

// src/components/Cart.jsx
import React from 'react';
import CartItem from './CartItem';
import CheckoutForm from './CheckoutForm';

export default function Cart({ cartItems, onUpdateQuantity, cartTotal }) {
  return (
    <div style={{ padding: '10px' }}>
      {cartItems.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#777' }}>Your cart is empty.</p>
      ) : (
        <>
          {cartItems.map(cartItem => (
            <CartItem
              key={cartItem.item.id}
              cartItem={cartItem}
              onUpdateQuantity={onUpdateQuantity}
            />
          ))}
          <div style={{ borderTop: '1px solid #eee', paddingTop: '15px', marginTop: '20px', textAlign: 'right' }}>
            <h3 style={{ color: '#333', marginBottom: '15px' }}>Total: ${cartTotal.toFixed(2)}</h3>
            <CheckoutForm amount={cartTotal} />
          </div>
        </>
      )}
    </div>
  );
}

// src/components/CartItem.jsx
import React from 'react';

export default function CartItem({ cartItem, onUpdateQuantity }) {
  const { item, quantity } = cartItem;

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid #eee' }}>
      <div>
        <h4 style={{ margin: '0', color: '#555' }}>{item.name}</h4>
        <p style={{ margin: '0', color: '#777', fontSize: '0.9em' }}>${item.price.toFixed(2)} each</p>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <button
          onClick={() => onUpdateQuantity(item.id, quantity - 1)}
          style={{
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            width: '30px',
            height: '30px',
            cursor: 'pointer',
            fontSize: '1.2em',
          }}
        >
          -
        </button>
        <span style={{ fontSize: '1.1em', minWidth: '20px', textAlign: 'center' }}>{quantity}</span>
        <button
          onClick={() => onUpdateQuantity(item.id, quantity + 1)}
          style={{
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            width: '30px',
            height: '30px',
            cursor: 'pointer',
            fontSize: '1.2em',
          }}
        >
          +
        </button>
      </div>
      <div style={{ fontWeight: 'bold', color: '#333', minWidth: '60px', textAlign: 'right' }}>
        ${(item.price * quantity).toFixed(2)}
      </div>
    </div>
  );
}

// src/components/CheckoutForm.jsx
import React, { useState } from 'react';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';

const CARD_ELEMENT_OPTIONS = {
  style: {
    base: {
      color: '#32325d',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4',
      },
    },
    invalid: {
      color: '#fa755a',
      iconColor: '#fa755a',
    },
  },
};

export default function CheckoutForm({ amount }) {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    if (!stripe || !elements) {
      // Stripe.js has not yet loaded. Make sure to disable form submission until Stripe.js has loaded.
      setLoading(false);
      return;
    }

    const cardElement = elements.getElement(CardElement);

    // Create PaymentMethod
    const { error: createPaymentMethodError, paymentMethod } = await stripe.createPaymentMethod({
      type: 'card',
      card: cardElement,
    });

    if (createPaymentMethodError) {
      setError(createPaymentMethodError.message);
      setLoading(false);
      return;
    }

    // --- IMPORTANT ---
    // In a real application, you would send `paymentMethod.id` to your server.
    // Your server would then use the Stripe API to create a PaymentIntent and confirm the payment.
    // For this client-side-only example, we'll just log the paymentMethod and simulate success.
    console.log('PaymentMethod:', paymentMethod);
    console.log(`Simulating a payment of $${amount.toFixed(2)} with paymentMethod.id: ${paymentMethod.id}`);

    // Simulate server-side processing and successful payment
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
      // In a real app, you would typically clear the cart and redirect to an order confirmation page here.
    }, 1500);
  };

  if (amount <= 0) {
    return <p style={{ textAlign: 'center', color: '#777', marginTop: '20px' }}>Add items to your cart to checkout.</p>;
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3 style={{ marginBottom: '15px', color: '#333' }}>Payment Details</h3>
      <div style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}>
        <CardElement options={CARD_ELEMENT_OPTIONS} />
      </div>

      {error && <div style={{ color: '#dc3545', marginBottom: '15px' }}>{error}</div>}
      {success && <div style={{ color: '#28a745', marginBottom: '15px' }}>Payment successful! Thank you for your order.</div>}

      <button
        type="submit"
        disabled={!stripe || loading}
        style={{
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          padding: '12px 20px',
          borderRadius: '5px',
          cursor: (!stripe || loading) ? 'not-allowed' : 'pointer',
          fontSize: '1.1em',
          width: '100%',
          opacity: (!stripe || loading) ? 0.6 : 1,
        }}
      >
        {loading ? 'Processing...' : `Pay $${amount.toFixed(2)}`}
      </button>
    </form>
  );
}