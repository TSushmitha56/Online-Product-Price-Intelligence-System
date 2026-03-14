import '@testing-library/jest-dom';
import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});

// Mocking Lucide icons to speed up tests and avoid potential JSDOM issues
vi.mock('lucide-react', () => ({
  Heart: () => <div data-testid="icon-heart" />,
  Layers: () => <div data-testid="icon-layers" />,
  Check: () => <div data-testid="icon-check" />,
  Star: () => <div data-testid="icon-star" />,
  ShieldCheck: () => <div data-testid="icon-shield" />,
  Package: () => <div data-testid="icon-package" />,
  ArrowRight: () => <div data-testid="icon-arrow" />,
  Truck: () => <div data-testid="icon-truck" />,
  CheckCircle: () => <div data-testid="icon-check-circle" />,
  XCircle: () => <div data-testid="icon-x-circle" />,
  Store: () => <div data-testid="icon-store" />,
}));
