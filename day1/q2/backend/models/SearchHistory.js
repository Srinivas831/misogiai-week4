const mongoose = require('mongoose');

const searchHistorySchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  keyword: {
    type: String,
    required: true,
    trim: true
  },
  resultsCount: {
    type: Number,
    default: 0
  }
}, {
  timestamps: true
});

// Create index for better query performance
searchHistorySchema.index({ userId: 1, createdAt: -1 });
searchHistorySchema.index({ keyword: 'text' });

module.exports = mongoose.model('SearchHistory', searchHistorySchema); 