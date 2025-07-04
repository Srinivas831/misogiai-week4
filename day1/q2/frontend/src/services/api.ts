import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('recommendation_project_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Types
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface Product {
  product_id: number;
  product_name: string;
  category: string;
  subcategory: string;
  price: number;
  quantity_in_stock: number;
  manufacturer: string;
  description: string;
  weight: number;
  dimensions: string;
  release_date: string;
  rating: number;
  is_featured: boolean;
  is_on_sale: boolean;
  sale_price?: number;
  image_url: string;
  viewCount?: number;
  purchaseCount?: number;
  createdAt?: string;
  updatedAt?: string;
}

export interface ProductsResponse {
  products: Product[];
  pagination: {
    currentPage: number;
    totalPages: number;
    totalProducts: number;
    limit: number;
  };
}

export interface SimilarProductsResponse {
  similarProducts: Product[];
  basedOn: {
    productId: number;
    productName: string;
    category: string;
    recommendationType: string;
  };
}

export interface SearchResponse {
  products: Product[];
  searchInfo: {
    keyword: string;
    resultsCount: number;
    category: string;
  };
  pagination: {
    currentPage: number;
    totalPages: number;
    totalProducts: number;
    limit: number;
  };
}

export interface AuthResponse {
  message: string;
  token: string;
  user: User;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface InteractionData {
  productId: number;
  action: 'viewed' | 'liked' | 'purchased' | 'added_to_cart';
  duration?: number;
  rating?: number;
}

// Auth API
export const authAPI = {
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<{ user: User }> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Products API
export const productsAPI = {
  getProducts: async (params?: {
    category?: string;
    minPrice?: number;
    maxPrice?: number;
    minRating?: number;
    sort?: string;
    page?: number;
    limit?: number;
  }): Promise<ProductsResponse> => {
    const response = await api.get('/products', { params });
    return response.data;
  },

  getProduct: async (id: number): Promise<{ product: Product }> => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  getSimilarProducts: async (id: number, limit = 5): Promise<SimilarProductsResponse> => {
    const response = await api.get(`/products/${id}/similar`, { params: { limit } });
    return response.data;
  },

  getCategories: async (): Promise<{ categories: string[] }> => {
    const response = await api.get('/products/categories/list');
    return response.data;
  },
};

// Search API
export const searchAPI = {
  searchProducts: async (data: {
    keyword: string;
    category?: string;
    sort?: string;
    page?: number;
    limit?: number;
  }): Promise<SearchResponse> => {
    const response = await api.post('/search', data);
    return response.data;
  },

  getSearchHistory: async (): Promise<any> => {
    const response = await api.get('/search/history');
    return response.data;
  },

  getSearchSuggestions: async (): Promise<any> => {
    const response = await api.get('/search/suggestions');
    return response.data;
  },
};

// Interactions API
export const interactionsAPI = {
  trackInteraction: async (data: InteractionData): Promise<any> => {
    const response = await api.post('/interactions', data);
    return response.data;
  },

  getInteractionHistory: async (): Promise<any> => {
    const response = await api.get('/interactions/history');
    return response.data;
  },

  getInteractionStats: async (): Promise<any> => {
    const response = await api.get('/interactions/stats');
    return response.data;
  },
};

// Health check
export const healthAPI = {
  check: async (): Promise<any> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api; 