// Simple test API using CommonJS syntax
module.exports = function handler(req, res) {
  res.status(200).json({ message: "Simple API test successful!" });
}