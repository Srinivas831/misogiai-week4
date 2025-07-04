# 🛒 AI-Powered Product Recommendation System - Backend

A Node.js + Express + MongoDB backend for an AI-powered product recommendation system with user authentication, product catalog, search functionality, and category-based recommendations.

## 🚀 Features

- **User Authentication**: JWT-based registration and login
- **Product Catalog**: Full CRUD operations with filtering and pagination
- **Search Engine**: Keyword-based product search with history tracking
- **AI Recommendations**: Category-based similar product suggestions
- **User Interactions**: Track user behavior (views, likes, purchases)
- **Analytics**: User interaction statistics and favorite categories

## 📋 Prerequisites

- Node.js (v14 or higher)
- MongoDB (local or cloud instance)
- npm or yarn

## 🔧 Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```env
   PORT=5000
   MONGODB_URI=mongodb+srv://srinivasan:srinivashari@cluster0.gmtgxdz.mongodb.net/AI-Powered-Product-Recommend?retryWrites=true&w=majority&appName=Cluster0
   JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-srinivasan-2024
   NODE_ENV=development
   ```
   
   **Note**: The MongoDB URI is already configured in `config.js` as a fallback, so you can skip creating the `.env` file if you want to use the default connection.

3. **Database Setup**:
   The system is configured to use MongoDB Atlas cloud database. No local MongoDB setup required.

4. **Seed the database**:
   ```bash
   npm run seed
   ```

5. **Start the server**:
   ```bash
   # Development mode (with auto-reload)
   npm run dev
   
   # Production mode
   npm start
   ```

## 📁 Project Structure

```
backend/
├── config.js              # Configuration settings
├── server.js              # Main server file
├── products.json          # Sample product data
├── package.json           # Dependencies and scripts
├── models/                # Database models
│   ├── User.js            # User schema
│   ├── Product.js         # Product schema
│   ├── SearchHistory.js   # Search history schema
│   └── UserInteraction.js # User interaction schema
├── routes/                # API routes
│   ├── auth.js            # Authentication routes
│   ├── products.js        # Product routes
│   ├── search.js          # Search routes
│   └── interactions.js    # User interaction routes
├── middleware/            # Custom middleware
│   └── auth.js            # JWT authentication middleware
└── utils/                 # Utility functions
    └── seedProducts.js    # Database seeding script
```

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Products
- `GET /api/products` - Get all products (with filtering)
- `GET /api/products/:id` - Get single product
- `GET /api/products/:id/similar` - Get similar products (AI Recommendation)
- `GET /api/products/categories/list` - Get all categories

### Search
- `POST /api/search` - Search products by keyword
- `GET /api/search/history` - Get user's search history
- `GET /api/search/suggestions` - Get search suggestions

### User Interactions
- `POST /api/interactions` - Track user interaction
- `GET /api/interactions/history` - Get user's interaction history
- `GET /api/interactions/stats` - Get user's interaction statistics

## 🤖 AI Recommendation Algorithm

The system uses **Category-Based Content Filtering**:

1. **Product Similarity**: When a user views a product, the system finds similar products in the same category
2. **Ranking**: Similar products are ranked by:
   - Product rating (higher rated products first)
   - View count (more popular products first)
3. **Personalization**: User interactions are tracked to improve future recommendations

### Example API Response:
```json
{
  "similarProducts": [
    {
      "product_id": 2,
      "product_name": "Handheld Garment Steamer",
      "category": "Home",
      "subcategory": "Home Appliances",
      "price": 936.36,
      "rating": 3.8,
      "manufacturer": "Browsezoom"
    }
  ],
  "basedOn": {
    "productId": 1,
    "productName": "Inspirational Wall Art",
    "category": "Home",
    "recommendationType": "Category-Based Content Filtering"
  }
}
```

## 🎯 Usage Examples

### Register a new user:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Search for products:
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "wall art",
    "category": "Home"
  }'
```

### Get similar products:
```bash
curl -X GET http://localhost:5000/api/products/1/similar?limit=3
```

### Track user interaction:
```bash
curl -X POST http://localhost:5000/api/interactions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "productId": 1,
    "action": "viewed",
    "duration": 30
  }'
```

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Request rate limiting
- Input validation
- CORS protection
- Security headers with Helmet

## 📊 Sample Data

The system comes with a comprehensive product dataset including:
- **Home**: Decorative items, appliances, bedding, furniture
- **Food**: Condiments, baking goods, snacks, beverages
- **Travel**: Accessories, luggage, comfort items
- **Pets**: Accessories, food, toys, care products
- **Health**: Personal care, wellness, fitness equipment
- **Clothing**: Footwear, apparel, accessories
- **Art Supplies**: Traditional and digital art materials
- **Electronics**: Gadgets, accessories, computing devices
- **Sports**: Equipment, apparel, accessories
- **Books**: Various genres and formats
- **Toys**: Educational, entertainment, outdoor play
- **Beauty**: Cosmetics, skincare, hair care
- **Automotive**: Parts, accessories, maintenance
- **Garden**: Tools, plants, outdoor equipment
- **Office**: Supplies, furniture, technology

## 🧪 Testing

Run the test suite:
```bash
npm test
```

## 📈 Future Enhancements

- Collaborative filtering based on user similarities
- Machine learning-based product embeddings
- Real-time recommendations
- A/B testing for recommendation algorithms
- Advanced analytics and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Happy coding! 🚀** 