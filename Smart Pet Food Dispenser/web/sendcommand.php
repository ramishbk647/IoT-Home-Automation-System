<?php
$command = $_POST['command'];

// Open serial port
$serialPort = fopen('/dev/ttyUSB0', 'w');
if (!$serialPort) {
    die('Failed to open serial port');
}

// Send command to Arduino
fwrite($serialPort, $command);

// Close serial port
fclose($serialPort);
?>
