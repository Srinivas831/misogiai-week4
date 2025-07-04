import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Star, Eye, ShoppingCart, Heart, Share2 } from 'lucide-react';
import { Header } from '../components/Header';
import { ProductCard } from '../components/ProductCard';
import { useAuth } from '../contexts/AuthContext';
import { productsAPI, interactionsAPI } from '../services/api';
import type { Product, SimilarProductsResponse } from '../services/api';

export const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  
  const [product, setProduct] = useState<Product | null>(null);
  const [similarProducts, setSimilarProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isLiked, setIsLiked] = useState(false);

  useEffect(() => {
    if (id) {
      loadProduct(parseInt(id));
      loadSimilarProducts(parseInt(id));
    }
  }, [id]);

  const loadProduct = async (productId: number) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await productsAPI.getProduct(productId);
      setProduct(response.product);
      
      // Track view interaction
      if (isAuthenticated) {
        await interactionsAPI.trackInteraction({
          productId,
          action: 'viewed',
        });
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load product');
    } finally {
      setIsLoading(false);
    }
  };

  const loadSimilarProducts = async (productId: number) => {
    try {
      const response: SimilarProductsResponse = await productsAPI.getSimilarProducts(productId, 8);
      setSimilarProducts(response.similarProducts);
    } catch (err) {
      console.error('Failed to load similar products:', err);
    }
  };

  const handleLike = async () => {
    if (!product || !isAuthenticated) return;
    
    try {
      await interactionsAPI.trackInteraction({
        productId: product.product_id,
        action: 'liked',
      });
      setIsLiked(!isLiked);
    } catch (err) {
      console.error('Failed to track like:', err);
    }
  };

  const handleAddToCart = async () => {
    if (!product || !isAuthenticated) return;
    
    try {
      await interactionsAPI.trackInteraction({
        productId: product.product_id,
        action: 'added_to_cart',
      });
      // Here you would typically add to cart logic
      alert('Product added to cart! (Demo)');
    } catch (err) {
      console.error('Failed to track add to cart:', err);
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: product?.product_name,
          text: `Check out this product: ${product?.product_name}`,
          url: window.location.href,
        });
      } catch (err) {
        console.error('Failed to share:', err);
      }
    } else {
      // Fallback to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Product link copied to clipboard!');
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
      );
    }

    if (hasHalfStar) {
      stars.push(
        <Star key="half" className="h-5 w-5 fill-yellow-400 text-yellow-400 opacity-50" />
      );
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <Star key={`empty-${i}`} className="h-5 w-5 text-gray-300" />
      );
    }

    return stars;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header
          onLoginClick={() => {}}
          onRegisterClick={() => {}}
        />
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header
          onLoginClick={() => {}}
          onRegisterClick={() => {}}
        />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-600">{error || 'Product not found'}</p>
            <button
              onClick={() => navigate('/')}
              className="mt-2 text-red-600 hover:text-red-700 font-medium"
            >
              Go Back to Home
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        onLoginClick={() => {}}
        onRegisterClick={() => {}}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate('/')}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-6 transition-colors"
        >
          <ArrowLeft className="h-5 w-5 mr-2" />
          Back to Products
        </button>

        {/* Product Details */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Product Image */}
          <div className="space-y-4">
            <div className="relative">
              <img
                src={product.image_url}
                alt={product.product_name}
                className="w-full h-96 object-cover rounded-lg shadow-lg"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.src = 'https://via.placeholder.com/600x400?text=No+Image';
                }}
              />
              {product.is_on_sale && (
                <div className="absolute top-4 left-4 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                  Sale
                </div>
              )}
              {product.is_featured && (
                <div className="absolute top-4 right-4 bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                  Featured
                </div>
              )}
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {product.product_name}
              </h1>
              <p className="text-lg text-gray-600 mb-4">
                by {product.manufacturer}
              </p>
              
              {/* Rating */}
              <div className="flex items-center mb-4">
                <div className="flex items-center mr-3">
                  {renderStars(product.rating)}
                </div>
                <span className="text-lg font-medium text-gray-900">
                  {product.rating.toFixed(1)}
                </span>
                {product.viewCount && (
                  <span className="ml-4 flex items-center text-gray-600">
                    <Eye className="h-4 w-4 mr-1" />
                    {product.viewCount} views
                  </span>
                )}
              </div>
            </div>

            {/* Price */}
            <div className="border-t border-b border-gray-200 py-6">
              <div className="flex items-center space-x-4">
                {product.is_on_sale && product.sale_price ? (
                  <>
                    <span className="text-3xl font-bold text-red-600">
                      {formatPrice(product.sale_price)}
                    </span>
                    <span className="text-xl text-gray-500 line-through">
                      {formatPrice(product.price)}
                    </span>
                    <span className="bg-red-100 text-red-800 px-2 py-1 rounded-full text-sm font-medium">
                      {Math.round(((product.price - product.sale_price) / product.price) * 100)}% OFF
                    </span>
                  </>
                ) : (
                  <span className="text-3xl font-bold text-gray-900">
                    {formatPrice(product.price)}
                  </span>
                )}
              </div>
            </div>

            {/* Stock and Actions */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-lg font-medium text-gray-900">
                  Stock: {product.quantity_in_stock} available
                </span>
                <div className="flex items-center space-x-2">
                  <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full">
                    {product.category}
                  </span>
                  {product.subcategory && (
                    <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full">
                      {product.subcategory}
                    </span>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex space-x-4">
                <button
                  onClick={handleAddToCart}
                  disabled={product.quantity_in_stock === 0}
                  className="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  <ShoppingCart className="h-5 w-5 mr-2" />
                  Add to Cart
                </button>
                <button
                  onClick={handleLike}
                  className={`p-3 rounded-lg border-2 transition-colors ${
                    isLiked
                      ? 'border-red-500 bg-red-50 text-red-600'
                      : 'border-gray-300 hover:border-gray-400 text-gray-600'
                  }`}
                >
                  <Heart className={`h-5 w-5 ${isLiked ? 'fill-current' : ''}`} />
                </button>
                <button
                  onClick={handleShare}
                  className="p-3 rounded-lg border-2 border-gray-300 hover:border-gray-400 text-gray-600 transition-colors"
                >
                  <Share2 className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Product Description */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Product Description</h2>
          <p className="text-gray-700 leading-relaxed mb-6">
            {product.description}
          </p>
          
          {/* Product Specifications */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Specifications</h3>
              <dl className="space-y-2">
                <div className="flex justify-between">
                  <dt className="text-gray-600">Weight:</dt>
                  <dd className="font-medium">{product.weight}g</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Dimensions:</dt>
                  <dd className="font-medium">{product.dimensions}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Release Date:</dt>
                  <dd className="font-medium">{new Date(product.release_date).toLocaleDateString()}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Category:</dt>
                  <dd className="font-medium">{product.category}</dd>
                </div>
                {product.subcategory && (
                  <div className="flex justify-between">
                    <dt className="text-gray-600">Subcategory:</dt>
                    <dd className="font-medium">{product.subcategory}</dd>
                  </div>
                )}
              </dl>
            </div>
          </div>
        </div>

        {/* Similar Products */}
        {similarProducts.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Similar Products</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {similarProducts.map(similarProduct => (
                <ProductCard
                  key={similarProduct.product_id}
                  product={similarProduct}
                  isAuthenticated={isAuthenticated}
                />
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}; 