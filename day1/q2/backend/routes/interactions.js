const express = require('express');
const UserInteraction = require('../models/UserInteraction');
const Product = require('../models/Product');
const { auth } = require('../middleware/auth');

const router = express.Router();

// @route   POST /api/interactions
// @desc    Track user interaction with a product
// @access  Private
router.post('/', auth, async (req, res) => {
  try {
    const { productId, action, duration = 0, rating } = req.body;

    if (!productId || !action) {
      return res.status(400).json({ error: 'Product ID and action are required' });
    }

    // Validate action
    const validActions = ['viewed', 'liked', 'purchased', 'added_to_cart'];
    if (!validActions.includes(action)) {
      return res.status(400).json({ 
        error: 'Invalid action. Must be one of: ' + validActions.join(', ') 
      });
    }

    // Check if product exists
    const product = await Product.findOne({ product_id: productId });
    if (!product) {
      return res.status(404).json({ error: 'Product not found' });
    }

    // Create interaction record
    const interactionData = {
      userId: req.user._id,
      productId,
      action,
      duration: Number(duration)
    };

    if (rating !== undefined) {
      interactionData.rating = Number(rating);
    }

    const interaction = new UserInteraction(interactionData);
    await interaction.save();

    // Update product counts based on action
    const updateData = {};
    if (action === 'viewed') {
      updateData.$inc = { viewCount: 1 };
    } else if (action === 'purchased') {
      updateData.$inc = { purchaseCount: 1 };
    }

    if (Object.keys(updateData).length > 0) {
      await Product.findOneAndUpdate({ product_id: productId }, updateData);
    }

    res.status(201).json({
      message: 'Interaction tracked successfully',
      interaction: {
        id: interaction._id,
        productId,
        action,
        duration,
        rating: rating || null,
        timestamp: interaction.createdAt
      }
    });
  } catch (error) {
    console.error('Track interaction error:', error);
    res.status(500).json({ error: 'Server error while tracking interaction' });
  }
});

// @route   GET /api/interactions/history
// @desc    Get user's interaction history
// @access  Private
router.get('/history', auth, async (req, res) => {
  try {
    const { action, limit = 20, page = 1 } = req.query;

    // Build filter
    const filter = { userId: req.user._id };
    if (action) {
      filter.action = action;
    }

    // Get interactions with product details
    const interactions = await UserInteraction.find(filter)
      .sort({ createdAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .populate('productId', 'product_name price rating category image_url');

    const total = await UserInteraction.countDocuments(filter);

    res.json({
      interactions,
      pagination: {
        currentPage: Number(page),
        totalPages: Math.ceil(total / limit),
        totalInteractions: total,
        limit: Number(limit)
      }
    });
  } catch (error) {
    console.error('Get interaction history error:', error);
    res.status(500).json({ error: 'Server error while fetching interaction history' });
  }
});

// @route   GET /api/interactions/stats
// @desc    Get user's interaction statistics
// @access  Private
router.get('/stats', auth, async (req, res) => {
  try {
    const stats = await UserInteraction.aggregate([
      { $match: { userId: req.user._id } },
      {
        $group: {
          _id: '$action',
          count: { $sum: 1 },
          avgDuration: { $avg: '$duration' }
        }
      }
    ]);

    // Get favorite categories based on interactions
    const favoriteCategories = await UserInteraction.aggregate([
      { $match: { userId: req.user._id } },
      {
        $lookup: {
          from: 'products',
          localField: 'productId',
          foreignField: '_id',
          as: 'product'
        }
      },
      { $unwind: '$product' },
      {
        $group: {
          _id: '$product.category',
          count: { $sum: 1 }
        }
      },
      { $sort: { count: -1 } },
      { $limit: 5 }
    ]);

    res.json({
      actionStats: stats.map(stat => ({
        action: stat._id,
        count: stat.count,
        avgDuration: Math.round(stat.avgDuration || 0)
      })),
      favoriteCategories: favoriteCategories.map(cat => ({
        category: cat._id,
        interactionCount: cat.count
      }))
    });
  } catch (error) {
    console.error('Get interaction stats error:', error);
    res.status(500).json({ error: 'Server error while fetching interaction stats' });
  }
});

module.exports = router; 