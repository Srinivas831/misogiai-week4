const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  product_id: {
    type: Number,
    required: true,
    unique: true
  },
  product_name: {
    type: String,
    required: true,
    trim: true
  },
  category: {
    type: String,
    required: true,
    trim: true
  },
  subcategory: {
    type: String,
    required: true,
    trim: true
  },
  price: {
    type: Number,
    required: true,
    min: 0
  },
  quantity_in_stock: {
    type: Number,
    required: true,
    min: 0
  },
  manufacturer: {
    type: String,
    required: true,
    trim: true
  },
  description: {
    type: String,
    required: true
  },
  weight: {
    type: Number,
    required: true,
    min: 0
  },
  dimensions: {
    type: String,
    required: true
  },
  release_date: {
    type: String,
    required: true
  },
  rating: {
    type: Number,
    required: true,
    min: 0,
    max: 5
  },
  is_featured: {
    type: Boolean,
    default: false
  },
  is_on_sale: {
    type: Boolean,
    default: false
  },
  sale_price: {
    type: Number,
    min: 0
  },
  image_url: {
    type: String,
    required: true
  },
  viewCount: {
    type: Number,
    default: 0
  },
  purchaseCount: {
    type: Number,
    default: 0
  }
}, {
  timestamps: true
});

// Create indexes for better search performance
productSchema.index({ product_name: 'text', description: 'text', manufacturer: 'text' });
productSchema.index({ category: 1 });
productSchema.index({ subcategory: 1 });
productSchema.index({ price: 1 });
productSchema.index({ rating: -1 });
productSchema.index({ is_featured: 1 });
productSchema.index({ is_on_sale: 1 });

module.exports = mongoose.model('Product', productSchema); 