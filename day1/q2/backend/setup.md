# 🚀 Quick Setup Guide

## Step 1: Install Dependencies
```bash
cd day1/q2/backend
npm install
```

## Step 2: Create .env File (Optional)
Create a `.env` file in the backend directory with:
```env
PORT=5000
MONGODB_URI=""
JWT_SECRET=""
NODE_ENV=development
```

**Note**: If you don't create the `.env` file, the system will use the MongoDB URI already configured in `config.js`.

## Step 3: Seed the Database
```bash
npm run seed
```

This will:
- Connect to your MongoDB Atlas database
- Clear any existing products
- Import all products from `products.json`
- Show statistics about the imported data

## Step 4: Start the Server
```bash
# Development mode (with auto-reload)
npm run dev

# OR Production mode
npm start
```

## Step 5: Test the API
Open your browser or use curl to test:
```bash
# Health check
curl http://localhost:5000/api/health

# Get all products
curl http://localhost:5000/api/products

# Get categories
curl http://localhost:5000/api/products/categories/list

# Search products
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "wall art"}'

# Get similar products
curl http://localhost:5000/api/products/1/similar
```

## 🎉 You're Ready!

Your AI-Powered Product Recommendation System backend is now running with:
- ✅ MongoDB Atlas connection
- ✅ Your product data imported
- ✅ Category-based recommendations
- ✅ Search functionality
- ✅ User authentication ready
- ✅ Interaction tracking ready

Next steps:
1. Test the API endpoints
2. Build a frontend to interact with the API
3. Register users and test the recommendation system 