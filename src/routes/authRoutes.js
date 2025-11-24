const express = require('express');
const router = express.Router();
const { userStore } = require('../data/store');

/**
 * @route   POST /api/auth/login
 * @desc    Simple login (for demo purposes - returns user ID to use in headers)
 * @access  Public
 */
router.post('/login', (req, res) => {
  const { email, password } = req.body;
  
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }
  
  const user = userStore.findByEmail(email);
  
  if (!user || user.password !== password) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  res.json({
    message: 'Login successful',
    user: user.toSafeObject()
  });
});

/**
 * @route   GET /api/auth/users
 * @desc    Get all users (for demo purposes)
 * @access  Public
 */
router.get('/users', (req, res) => {
  const users = userStore.findAll();
  res.json(users.map(u => u.toSafeObject()));
});

module.exports = router;
