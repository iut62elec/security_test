/**
 * API Handler - CLEAN CODE (secure implementation).
 * A security scanner should NOT flag any issues here.
 */
const crypto = require("crypto");
const path = require("path");
const { execFile } = require("child_process");

const DB_CONFIG = {
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
};

function getUser(db, req, res) {
  const userId = parseInt(req.params.id, 10);
  if (isNaN(userId)) return res.status(400).json({ error: "Invalid ID" });
  db.query("SELECT id, name, email FROM users WHERE id = ?", [userId], (err, r) => {
    if (err) return res.status(500).json({ error: "DB error" });
    res.json(r[0] || null);
  });
}

function searchUsers(db, req, res) {
  db.query("SELECT id, name FROM users WHERE name LIKE ?", [`%${req.query.name}%`], (err, r) => {
    if (err) return res.status(500).json({ error: "DB error" });
    res.json(r);
  });
}

function downloadFile(req, res) {
  const filename = path.basename(req.params.filename);
  const basePath = "/var/data/files";
  const fullPath = path.resolve(basePath, filename);
  if (!fullPath.startsWith(basePath)) return res.status(403).json({ error: "Denied" });
  res.sendFile(fullPath);
}

function renderPage(req, res) {
  const name = escapeHtml(req.query.name || "Guest");
  res.send(`<html><body><h1>Hello ${name}</h1></body></html>`);
}

function verifyWebhook(payload, signature, secret) {
  const expected = crypto.createHmac("sha256", secret).update(payload).digest("hex");
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}

function generateToken() {
  return crypto.randomBytes(32).toString("hex");
}

function convertImage(input, output, cb) {
  execFile("convert", [input, output], cb);
}

function escapeHtml(text) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

function calculateTotal(items) {
  return items.reduce((sum, i) => sum + i.price * i.quantity, 0);
}

module.exports = { getUser, searchUsers, downloadFile, renderPage, verifyWebhook, generateToken, convertImage, calculateTotal };
