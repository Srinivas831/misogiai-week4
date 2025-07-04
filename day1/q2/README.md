# AI-Powered Product Recommendation System

A full-stack e-commerce application with AI-powered product recommendations, built with React, Node.js, Express, and MongoDB.

## Features

### Frontend (React + TypeScript + Tailwind CSS)
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Authentication**: JWT-based login/register system
- **Product Catalog**: Grid/list view with pagination (20 products per page)
- **Search & Filter**: Category-based filtering and sorting
- **Product Details**: Detailed product pages with specifications
- **AI Recommendations**: Similar products based on category and user behavior
- **User Interactions**: View tracking, likes, and cart functionality
- **Responsive Design**: Works on desktop, tablet, and mobile

### Backend (Node.js + Express + MongoDB)
- **RESTful API**: Complete CRUD operations for products
- **Authentication**: JWT middleware for protected routes
- **Database**: MongoDB with Mongoose ODM
- **AI Recommendations**: Category-based content filtering
- **Search Engine**: Keyword-based product search
- **User Tracking**: Interaction logging (views, likes, purchases)
- **Data Seeding**: 1000+ products across multiple categories

## Tech Stack

### Frontend
- React 19 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls
- Lucide React for icons

### Backend
- Node.js with Express
- MongoDB with Mongoose
- JWT for authentication
- bcryptjs for password hashing
- CORS for cross-origin requests

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- MongoDB Atlas account or local MongoDB
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd day1/q2
   ```

2. **Backend Setup**
   ```bash
   cd backend
   npm install
   
   # Create .env file with your MongoDB connection string

   echo "JWT_SECRET=your-super-secret-jwt-key-here" >> .env
   echo "PORT=5000" >> .env
   
   # Start the backend server
   npm start
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   
   # Start the development server
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (protected)

### Products
- `GET /api/products` - Get all products with pagination
- `GET /api/products/:id` - Get single product
- `GET /api/products/:id/similar` - Get similar products (AI recommendations)
- `GET /api/products/categories/list` - Get all categories

### Search
- `POST /api/search` - Search products by keyword
- `GET /api/search/history` - Get user's search history (protected)
- `GET /api/search/suggestions` - Get search suggestions (protected)

### Interactions
- `POST /api/interactions` - Track user interaction (protected)
- `GET /api/interactions/history` - Get user's interaction history (protected)
- `GET /api/interactions/stats` - Get interaction statistics (protected)

## User Flow

### Public Users (Non-authenticated)
1. **Home Page**: View all products with pagination
2. **Product Grid**: See product cards with basic info (name, price, rating, image)
3. **Login Prompt**: Click on product card shows login modal
4. **Authentication**: Register or login to access full features

### Authenticated Users
1. **Full Access**: Click product cards to view detailed pages
2. **Search**: Use search bar to find specific products
3. **Recommendations**: View similar products on detail pages
4. **Interactions**: Track views, likes, and cart additions
5. **Personalization**: Get better recommendations based on behavior

## AI Recommendation Engine

The system uses a category-based content filtering approach:

1. **Content Analysis**: Products are categorized by type and attributes
2. **Similarity Matching**: Find products in the same category
3. **Ranking Algorithm**: Sort by rating, view count, and user preferences
4. **Personalization**: Factor in user's interaction history
5. **Real-time Updates**: Recommendations improve with user behavior

## Database Schema

### User Model
- `name`: String (required)
- `email`: String (unique, required)
- `password`: String (hashed, required)
- `createdAt`: Date
- `updatedAt`: Date

### Product Model
- `product_id`: Number (unique)
- `product_name`: String
- `category`: String
- `subcategory`: String
- `price`: Number
- `sale_price`: Number (optional)
- `is_on_sale`: Boolean
- `quantity_in_stock`: Number
- `manufacturer`: String
- `description`: String
- `rating`: Number
- `image_url`: String
- `viewCount`: Number
- `purchaseCount`: Number

### User Interaction Model
- `userId`: ObjectId (ref: User)
- `productId`: Number
- `action`: String (viewed, liked, purchased, added_to_cart)
- `timestamp`: Date
- `duration`: Number (optional)
- `rating`: Number (optional)

## Features in Detail

### Authentication System
- **JWT Tokens**: Stored in localStorage as `recommendation_project_token`
- **Protected Routes**: Product detail pages require authentication
- **Modal System**: Login/register modals for seamless UX
- **Auto-redirect**: Redirect to intended page after login

### Product Catalog
- **Pagination**: 20 products per page with navigation
- **Grid/List View**: Toggle between different viewing modes
- **Category Filter**: Filter products by category
- **Sorting Options**: Price, rating, name, newest
- **Search Integration**: Keyword-based product search

### AI Recommendations
- **Similar Products**: Show related items on product detail pages
- **Category-based**: Find products in same category
- **Behavior Tracking**: Improve recommendations with user interactions
- **Real-time**: Updated recommendations based on current trends

## Development

### Running in Development Mode
```bash
# Backend (Terminal 1)
cd backend
npm run dev

# Frontend (Terminal 2)
cd frontend
npm run dev
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
npm start
```

### Environment Variables
Create `.env` file in backend directory:
```env
MONGODB_URI=your-mongodb-connection-string
JWT_SECRET=your-jwt-secret-key
PORT=5000
```

## Testing

The system has been tested with:
- ✅ User registration and login
- ✅ Product catalog loading
- ✅ Search functionality
- ✅ AI recommendations
- ✅ User interaction tracking
- ✅ Responsive design
- ✅ Error handling

## Future Enhancements

1. **Advanced AI**: Machine learning models for better recommendations
2. **Shopping Cart**: Complete e-commerce functionality
3. **Payment Integration**: Stripe or PayPal integration
4. **Reviews System**: User reviews and ratings
5. **Wishlist**: Save products for later
6. **Admin Panel**: Product management interface
7. **Analytics**: Advanced user behavior analytics
8. **Mobile App**: React Native mobile application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. 