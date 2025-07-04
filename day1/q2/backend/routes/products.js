const express = require('express');
const Product = require('../models/Product');
const UserInteraction = require('../models/UserInteraction');
const { optionalAuth } = require('../middleware/auth');

const router = express.Router();

// @route   GET /api/products
// @desc    Get all products with optional filtering
// @access  Public
router.get('/', optionalAuth, async (req, res) => {
  try {
    const {
      category,
      minPrice,
      maxPrice,
      minRating,
      sort = 'name',
      page = 1,
      limit = 20
    } = req.query;

    // Build filter object
    const filter = {};
    
    if (category) {
      filter.category = new RegExp(category, 'i');
    }
    
    if (minPrice || maxPrice) {
      filter.price = {};
      if (minPrice) filter.price.$gte = Number(minPrice);
      if (maxPrice) filter.price.$lte = Number(maxPrice);
    }
    
    if (minRating) {
      filter.rating = { $gte: Number(minRating) };
    }

    // Build sort object
    const sortOptions = {};
    switch (sort) {
      case 'price_low':
        sortOptions.price = 1;
        break;
      case 'price_high':
        sortOptions.price = -1;
        break;
      case 'rating':
        sortOptions.rating = -1;
        break;
      case 'popular':
        sortOptions.viewCount = -1;
        break;
      default:
        sortOptions.name = 1;
    }

    console.log("filter",filter);
    console.log("sortOptions",sortOptions);
    // Execute query with pagination
    const products = await Product.find(filter)
      .sort(sortOptions)
      .limit(limit * 1)
      .skip((page - 1) * limit);

    const total = await Product.countDocuments(filter);
    res.json({
      products,
      pagination: {
        currentPage: Number(page),
        totalPages: Math.ceil(total / limit),
        totalProducts: total,
        limit: Number(limit)
      }
    });
  } catch (error) {
    console.error('Get products error:', error);
    res.status(500).json({ error: 'Server error while fetching products' });
  }
});

// @route   GET /api/products/:id
// @desc    Get single product by ID
// @access  Public
router.get('/:id', optionalAuth, async (req, res) => {
  try {
    const product = await Product.findOne({ product_id: req.params.id });
    
    if (!product) {
      return res.status(404).json({ error: 'Product not found' });
    }

    // Increment view count
    await Product.findOneAndUpdate({ product_id: req.params.id }, { $inc: { viewCount: 1 } });

    // If user is logged in, track the interaction
    if (req.user) {
      await UserInteraction.create({
        userId: req.user._id,
        productId: req.params.id,
        action: 'viewed'
      });
    }

    res.json({ product });
  } catch (error) {
    console.error('Get product error:', error);
    res.status(500).json({ error: 'Server error while fetching product' });
  }
});

// @route   GET /api/products/:id/similar
// @desc    Get similar products based on category (AI Recommendation)
// @access  Public
router.get('/:id/similar', optionalAuth, async (req, res) => {
  try {
    const { limit = 5 } = req.query;
    
    // Get the current product
    const currentProduct = await Product.findOne({ product_id: req.params.id });
    console.log("currentProduct",currentProduct);
    if (!currentProduct) {
      return res.status(404).json({ error: 'Product not found' });
    }

    // Find similar products in the same category
    const similarProducts = await Product.find({
      category: currentProduct.category,
      product_id: { $ne: currentProduct.product_id } // Exclude the current product
    })
    .sort({ 
      rating: -1,      // Higher rated products first
      viewCount: -1    // More popular products first
    })
    .limit(Number(limit));

    res.json({
      similarProducts,
      basedOn: {
        productId: currentProduct.product_id,
        productName: currentProduct.product_name,
        category: currentProduct.category,
        recommendationType: 'Category-Based Content Filtering'
      }
    });
  } catch (error) {
    console.error('Get similar products error:', error);
    res.status(500).json({ error: 'Server error while fetching similar products' });
  }
});

// @route   GET /api/products/categories/list
// @desc    Get all unique product categories
// @access  Public
router.get('/categories/list', async (req, res) => {
  try {
    const categories = await Product.distinct('category');
    res.json({ categories });
  } catch (error) {
    console.error('Get categories error:', error);
    res.status(500).json({ error: 'Server error while fetching categories' });
  }
});

module.exports = router; 