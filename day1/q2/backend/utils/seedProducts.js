const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const Product = require('../models/Product');
const config = require('../config');

// Connect to MongoDB
const connectDB = async () => {
  try {
    await mongoose.connect(config.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('✅ Connected to MongoDB');
  } catch (error) {
    console.error('❌ MongoDB connection error:', error);
    process.exit(1);
  }
};

// Seed products from JSON file
const seedProducts = async () => {
  try {
    // Read products from JSON file
    const productsPath = path.join(__dirname, '..', 'products.json');
    const productsData = JSON.parse(fs.readFileSync(productsPath, 'utf8'));

    // Clear existing products
    await Product.deleteMany({});
    console.log('🗑️  Cleared existing products');

    // Insert new products
    await Product.insertMany(productsData);
    console.log(`✅ Successfully seeded ${productsData.length} products`);

    // Display categories summary
    const categories = await Product.distinct('category');
    console.log(`📊 Categories available: ${categories.join(', ')}`);

    // Display some stats
    const stats = await Product.aggregate([
      {
        $group: {
          _id: '$category',
          count: { $sum: 1 },
          avgPrice: { $avg: '$price' },
          avgRating: { $avg: '$rating' }
        }
      },
      { $sort: { count: -1 } }
    ]);

    console.log('\n📈 Product Statistics:');
    stats.forEach(stat => {
      console.log(`  ${stat._id}: ${stat.count} products, Avg Price: $${Math.round(stat.avgPrice)}, Avg Rating: ${stat.avgRating.toFixed(1)}`);
    });

    // Display subcategory stats
    const subcategoryStats = await Product.aggregate([
      {
        $group: {
          _id: { category: '$category', subcategory: '$subcategory' },
          count: { $sum: 1 }
        }
      },
      { $sort: { '_id.category': 1, count: -1 } }
    ]);

    console.log('\n📊 Top Subcategories by Category:');
    let currentCategory = '';
    subcategoryStats.forEach(stat => {
      if (stat._id.category !== currentCategory) {
        currentCategory = stat._id.category;
        console.log(`\n  ${currentCategory}:`);
      }
      console.log(`    - ${stat._id.subcategory}: ${stat.count} products`);
    });

  } catch (error) {
    console.error('❌ Error seeding products:', error);
  }
};

// Run the seeding process
const run = async () => {
  await connectDB();
  await seedProducts();
  await mongoose.connection.close();
  console.log('✅ Database seeding completed');
  process.exit(0);
};

// Execute if run directly
if (require.main === module) {
  run();
}

module.exports = { seedProducts, connectDB }; 