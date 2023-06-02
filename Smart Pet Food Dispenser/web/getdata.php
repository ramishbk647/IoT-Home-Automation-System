<?php
// Database connection details
$host = 'localhost';
$username = 'root';
$password = 'root';
$database = 'smartpetfeeder';

// Create connection
$conn = new mysqli($host, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die('Connection failed: ' . $conn->connect_error);
}

// Fetch data from the database
$sql = 'SELECT * FROM datasaver';
$result = $conn->query($sql);
$data = array();
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

// Send data as JSON response
header('Content-Type: application/json');
echo json_encode($data);

$conn->close();
?>
