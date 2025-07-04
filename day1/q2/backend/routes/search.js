const express = require('express');
const Product = require('../models/Product');
const SearchHistory = require('../models/SearchHistory');
const { optionalAuth } = require('../middleware/auth');

const router = express.Router();

// @route   POST /api/search
// @desc    Search products by keyword
// @access  Public
router.post('/', optionalAuth, async (req, res) => {
  try {
    const { keyword, category, sort = 'relevance', page = 1, limit = 20 } = req.body;
    if (!keyword || keyword.trim() === '') {
      return res.status(400).json({ error: 'Search keyword is required' });
    }

    const searchKeyword = keyword.trim();

    // Build search filter
    const filter = {
      $or: [
        { product_name: { $regex: searchKeyword, $options: 'i' } },
        { description: { $regex: searchKeyword, $options: 'i' } },
        { manufacturer: { $regex: searchKeyword, $options: 'i' } },
        { category: { $regex: searchKeyword, $options: 'i' } },
        { subcategory: { $regex: searchKeyword, $options: 'i' } }
      ]
    };
    console.log("filter",filter);

    // Add category filter if specified
    if (category) {
      filter.category = new RegExp(category, 'i');
    }

    // Build sort options
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
        sortOptions.rating = -1; // Default to best rated for relevance
    }

    // Execute search
    const products = await Product.find(filter)
      .sort(sortOptions)
      .limit(limit * 1)
      .skip((page - 1) * limit);

    const total = await Product.countDocuments(filter);

    // Save search history if user is logged in
    if (req.user) {
      await SearchHistory.create({
        userId: req.user._id,
        keyword: searchKeyword,
        resultsCount: total
      });
    }

    res.json({
      products,
      searchInfo: {
        keyword: searchKeyword,
        resultsCount: total,
        category: category || 'all'
      },
      pagination: {
        currentPage: Number(page),
        totalPages: Math.ceil(total / limit),
        totalProducts: total,
        limit: Number(limit)
      }
    });
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({ error: 'Server error during search' });
  }
});

// @route   GET /api/search/history
// @desc    Get user's search history
// @access  Private
router.get('/history', optionalAuth, async (req, res) => {
  try {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    const { limit = 10 } = req.query;

    const searchHistory = await SearchHistory.find({ userId: req.user._id })
      .sort({ createdAt: -1 })
      .limit(Number(limit));

    res.json({ searchHistory });
  } catch (error) {
    console.error('Get search history error:', error);
    res.status(500).json({ error: 'Server error while fetching search history' });
  }
});

// @route   GET /api/search/suggestions
// @desc    Get search suggestions based on popular searches
// @access  Public
router.get('/suggestions', async (req, res) => {
  try {
    const { limit = 5 } = req.query;

    // Get most popular search terms
    const popularSearches = await SearchHistory.aggregate([
      {
        $group: {
          _id: '$keyword',
          count: { $sum: 1 },
          avgResults: { $avg: '$resultsCount' }
        }
      },
      { $sort: { count: -1 } },
      { $limit: Number(limit) }
    ]);

    // Also get suggestions based on product names
    const productSuggestions = await Product.aggregate([
      {
        $group: {
          _id: '$category',
          count: { $sum: 1 },
          avgRating: { $avg: '$rating' }
        }
      },
      { $sort: { count: -1 } },
      { $limit: Number(limit) }
    ]);

    res.json({
      popularSearches: popularSearches.map(item => ({
        keyword: item._id,
        searchCount: item.count,
        avgResults: Math.round(item.avgResults)
      })),
      categorySearches: productSuggestions.map(item => ({
        category: item._id,
        productCount: item.count,
        avgRating: Math.round(item.avgRating * 10) / 10
      }))
    });
  } catch (error) {
    console.error('Get suggestions error:', error);
    res.status(500).json({ error: 'Server error while fetching suggestions' });
  }
});

module.exports = router; 