package com.example.vulnerable;

import java.io.*;
import java.net.*;
import java.sql.*;
import javax.xml.parsers.*;
import org.xml.sax.InputSource;

/**
 * Data Access Layer - VULNERABLE CODE (intentional for testing).
 */
public class DataAccessLayer {

    // VULNERABILITY: Hardcoded credentials
    private static final String DB_URL = "jdbc:mysql://prod-server:3306/app";
    private static final String DB_USER = "root";
    private static final String DB_PASS = "r00t_pr0d_p@ss!";
    private static final String API_KEY = "java-api-key-prod-abc123";

    private Connection connection;

    public DataAccessLayer() throws SQLException {
        this.connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
    }

    // VULNERABILITY: SQL Injection
    public ResultSet getUser(String userId) throws SQLException {
        Statement stmt = connection.createStatement();
        return stmt.executeQuery("SELECT * FROM users WHERE id = '" + userId + "'");
    }

    public ResultSet searchProducts(String keyword) throws SQLException {
        Statement stmt = connection.createStatement();
        return stmt.executeQuery("SELECT * FROM products WHERE name LIKE '%" + keyword + "%'");
    }

    public void deleteRecord(String table, String id) throws SQLException {
        Statement stmt = connection.createStatement();
        stmt.executeUpdate("DELETE FROM " + table + " WHERE id = " + id);
    }

    // VULNERABILITY: Command Injection
    public String runDiagnostic(String hostname) throws IOException {
        Process proc = Runtime.getRuntime().exec("ping -c 4 " + hostname);
        BufferedReader reader = new BufferedReader(new InputStreamReader(proc.getInputStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) sb.append(line).append("
");
        return sb.toString();
    }

    // VULNERABILITY: Path Traversal
    public byte[] readFile(String filename) throws IOException {
        return new FileInputStream(new File("/var/data/uploads/" + filename)).readAllBytes();
    }

    // VULNERABILITY: XXE
    public String parseXml(String xmlInput) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        var doc = builder.parse(new InputSource(new StringReader(xmlInput)));
        return doc.getDocumentElement().getTextContent();
    }

    // VULNERABILITY: SSRF
    public String fetchUrl(String targetUrl) throws IOException {
        HttpURLConnection conn = (HttpURLConnection) new URL(targetUrl).openConnection();
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) sb.append(line);
        return sb.toString();
    }

    // VULNERABILITY: Insecure Deserialization
    public Object deserialize(byte[] data) throws Exception {
        return new ObjectInputStream(new ByteArrayInputStream(data)).readObject();
    }

    // VULNERABILITY: Weak hashing
    public String hashData(String input) throws Exception {
        byte[] digest = java.security.MessageDigest.getInstance("MD5").digest(input.getBytes());
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) sb.append(String.format("%02x", b));
        return sb.toString();
    }
}
