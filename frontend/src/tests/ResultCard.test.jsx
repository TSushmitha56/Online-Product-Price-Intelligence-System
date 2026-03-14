import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import ResultCard from '../components/results/ResultCard';
import { describe, it, expect, vi } from 'vitest';

// Mock API
vi.mock('../api/axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

const mockOffer = {
  store: 'Amazon',
  price: 99.99,
  final_price: 105.99,
  seller_rating: 4.8,
  availability: 'In Stock',
  image_url: 'https://example.com/image.jpg',
  product_url: 'https://amazon.com/product',
  is_best_deal: true,
  title: 'Test Laptop'
};

const renderResultCard = (offer) => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <ResultCard offer={offer} productName="Test Laptop" />
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('ResultCard Component', () => {
  it('renders product title and store', () => {
    renderResultCard(mockOffer);
    expect(screen.getByText('Test Laptop')).toBeInTheDocument();
    expect(screen.getByText('Amazon')).toBeInTheDocument();
  });

  it('displays the final price correctly', () => {
    renderResultCard(mockOffer);
    expect(screen.getByText('105.99')).toBeInTheDocument();
  });

  it('shows Top Pick badge if is_best_deal is true', () => {
    renderResultCard(mockOffer);
    expect(screen.getByText('Top Pick')).toBeInTheDocument();
  });

  it('renders loading="lazy" on the image', () => {
    renderResultCard(mockOffer);
    const img = screen.getByAltText('Test Laptop');
    expect(img).toHaveAttribute('loading', 'lazy');
  });
});
