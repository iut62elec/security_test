/**
 * API Handler - VULNERABLE CODE (intentional for testing).
 */
const { exec } = require("child_process");
const mysql = require("mysql");
const fs = require("fs");
const serialize = require("node-serialize");

// VULNERABILITY: Hardcoded secrets
const DB_PASSWORD = "mysql_pr0d_p@ssw0rd!";
const JWT_SECRET = "super-secret-jwt-key-never-commit";
const API_KEY = "api_key_prod_x9y8z7w6v5u4";
const WEBHOOK_SECRET = "whsec_prod_abc123def456";

const db = mysql.createConnection({
  host: "prod-db.company.com",
  user: "root",
  password: DB_PASSWORD,
});

// VULNERABILITY: SQL Injection
function getUser(req, res) {
  db.query("SELECT * FROM users WHERE id = " + req.params.id, (err, r) => res.json(r));
}

function searchUsers(req, res) {
  db.query(`SELECT * FROM users WHERE name LIKE '%${req.query.name}%'`, (err, r) => res.json(r));
}

function loginUser(req, res) {
  const q = "SELECT * FROM users WHERE username='" + req.body.username + "' AND password='" + req.body.password + "'";
  db.query(q, (err, r) => res.json(r));
}

// VULNERABILITY: Command Injection
function convertImage(req, res) {
  exec("convert /uploads/" + req.body.filename + " /out/thumb.png", () => res.json({ ok: true }));
}

function pingHost(req, res) {
  exec(`ping -c 4 ${req.query.host}`, (err, stdout) => res.send(stdout));
}

// VULNERABILITY: Path Traversal
function downloadFile(req, res) {
  res.sendFile("/var/data/files/" + req.params.filename);
}

function readLog(req, res) {
  res.send(fs.readFileSync(`/var/log/app/${req.query.name}`, "utf8"));
}

// VULNERABILITY: Insecure Deserialization
function processPayload(req, res) {
  res.json(serialize.unserialize(req.body.data));
}

// VULNERABILITY: XSS (Reflected)
function renderPage(req, res) {
  res.send(`<html><body><h1>Hello ${req.query.name}</h1></body></html>`);
}

function renderError(req, res) {
  res.send("<div class='error'>" + req.query.message + "</div>");
}

// VULNERABILITY: Missing auth
function deleteUser(req, res) {
  db.query(`DELETE FROM users WHERE id = ${req.params.id}`, () => res.json({ deleted: true }));
}

module.exports = { getUser, searchUsers, loginUser, convertImage, pingHost, downloadFile, readLog, processPayload, renderPage, renderError, deleteUser };
