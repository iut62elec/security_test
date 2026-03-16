// Utility functions with intentional security vulnerabilities

// VULNERABILITY: Hardcoded API token
const GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz";

// VULNERABILITY: eval() usage - code injection
function processUserFormula(formula) {
    return eval(formula);
}

// VULNERABILITY: innerHTML assignment - DOM XSS
function displayMessage(message) {
    document.getElementById("output").innerHTML = message;
}

// VULNERABILITY: No CSRF protection, credentials in URL
function fetchUserData(userId) {
    return fetch(`/api/users/${userId}?token=${GITHUB_TOKEN}`, {
        credentials: "include",
    });
}

// VULNERABILITY: Regex DoS (ReDoS)
function validateEmail(email) {
    const regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

module.exports = { processUserFormula, displayMessage, fetchUserData, validateEmail };
