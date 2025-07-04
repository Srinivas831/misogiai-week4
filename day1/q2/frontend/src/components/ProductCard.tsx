import React from 'react';
import { Link } from 'react-router-dom';
import { Star, Eye } from 'lucide-react';
import type { Product } from '../services/api';

interface ProductCardProps {
  product: Product;
  isAuthenticated: boolean;
  onViewProduct?: (productId: number) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ 
  product, 
  isAuthenticated, 
  onViewProduct 
}) => {
  const handleCardClick = () => {
    if (onViewProduct) {
      onViewProduct(product.product_id);
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
        <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
      );
    }

    if (hasHalfStar) {
      stars.push(
        <Star key="half" className="h-4 w-4 fill-yellow-400 text-yellow-400 opacity-50" />
      );
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <Star key={`empty-${i}`} className="h-4 w-4 text-gray-300" />
      );
    }

    return stars;
  };

  const CardContent = () => (
    <div className="card p-4 h-full flex flex-col transition-transform duration-200 hover:scale-105 hover:shadow-lg">
      {/* Product Image */}
      <div className="relative mb-4">
        <img
          src={product.image_url}
          alt={product.product_name}
          className="w-full h-48 object-cover rounded-lg"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = 'https://via.placeholder.com/300x200?text=No+Image';
          }}
        />
        {product.is_on_sale && (
          <div className="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-bold">
            Sale
          </div>
        )}
        {product.is_featured && (
          <div className="absolute top-2 right-2 bg-blue-500 text-white px-2 py-1 rounded-full text-xs font-bold">
            Featured
          </div>
        )}
      </div>

      {/* Product Info */}
      <div className="flex-1 flex flex-col">
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
          {product.product_name}
        </h3>
        
        <p className="text-sm text-gray-600 mb-2">
          {product.manufacturer}
        </p>

        <div className="flex items-center mb-3">
          <div className="flex items-center mr-2">
            {renderStars(product.rating)}
          </div>
          <span className="text-sm text-gray-600">
            ({product.rating.toFixed(1)})
          </span>
        </div>

        {/* Price */}
        <div className="flex items-center justify-between mb-4 mt-auto">
          <div className="flex items-center space-x-2">
            {product.is_on_sale && product.sale_price ? (
              <>
                <span className="text-xl font-bold text-red-600">
                  {formatPrice(product.sale_price)}
                </span>
                <span className="text-sm text-gray-500 line-through">
                  {formatPrice(product.price)}
                </span>
              </>
            ) : (
              <span className="text-xl font-bold text-gray-900">
                {formatPrice(product.price)}
              </span>
            )}
          </div>
        </div>

        {/* Stock Status */}
        <div className="flex items-center justify-between text-sm text-gray-600 mb-3">
          <span>Stock: {product.quantity_in_stock}</span>
          {product.viewCount && (
            <span className="flex items-center">
              <Eye className="h-4 w-4 mr-1" />
              {product.viewCount}
            </span>
          )}
        </div>

        {/* Category */}
        <div className="flex items-center justify-between">
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
    </div>
  );

  if (isAuthenticated) {
    return (
      <Link
        to={`/product/${product.product_id}`}
        onClick={handleCardClick}
        className="block h-full"
      >
        <CardContent />
      </Link>
    );
  }

  return (
    <div className="h-full cursor-pointer" onClick={handleCardClick}>
      <CardContent />
    </div>
  );
}; 