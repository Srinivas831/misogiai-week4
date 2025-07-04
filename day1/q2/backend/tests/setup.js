// Jest setup file
process.env.NODE_ENV = 'test';
process.env.JWT_SECRET = 'test-jwt-secret';
process.env.MONGODB_URI_TEST = 'mongodb://localhost:27017/recommendation-system-test';

// Increase timeout for async operations
jest.setTimeout(30000);

// Mock console.log for cleaner test output
console.log = jest.fn();
console.error = jest.fn(); 