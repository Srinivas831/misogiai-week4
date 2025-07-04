const mongoose = require('mongoose');

const userInteractionSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  productId: {
    type: Number,
    required: true
  },
  action: {
    type: String,
    required: true,
    enum: ['viewed', 'liked', 'purchased', 'added_to_cart']
  },
  duration: {
    type: Number, // seconds spent viewing the product
    default: 0
  },
  rating: {
    type: Number,
    min: 0,
    max: 5
  }
}, {
  timestamps: true
});

// Create indexes for better query performance
userInteractionSchema.index({ userId: 1, createdAt: -1 });
userInteractionSchema.index({ productId: 1 });
userInteractionSchema.index({ action: 1 });
userInteractionSchema.index({ userId: 1, productId: 1 });

module.exports = mongoose.model('UserInteraction', userInteractionSchema); 