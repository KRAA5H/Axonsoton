const { userStore } = require('../data/store');

/**
 * Simple authentication middleware
 * In production, this would use JWT or session-based authentication
 */
const authenticate = (req, res, next) => {
  const userId = req.headers['x-user-id'];
  
  if (!userId) {
    return res.status(401).json({ error: 'Authentication required. Please provide X-User-Id header.' });
  }
  
  const user = userStore.findById(userId);
  
  if (!user) {
    return res.status(401).json({ error: 'Invalid user ID' });
  }
  
  req.user = user;
  next();
};

/**
 * Authorization middleware to ensure only GPs can access certain routes
 */
const authorizeGP = (req, res, next) => {
  if (!req.user) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  if (req.user.role !== 'gp') {
    return res.status(403).json({ error: 'Access denied. Only GPs can perform this action.' });
  }
  
  next();
};

/**
 * Authorization middleware to ensure only patients can access certain routes
 */
const authorizePatient = (req, res, next) => {
  if (!req.user) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  if (req.user.role !== 'patient') {
    return res.status(403).json({ error: 'Access denied. Only patients can access this resource.' });
  }
  
  next();
};

module.exports = {
  authenticate,
  authorizeGP,
  authorizePatient
};
