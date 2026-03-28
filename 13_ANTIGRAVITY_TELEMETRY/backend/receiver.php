<?php
/**
 * Antigravity Telemetry Receiver
 */
// Allow CORS
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Ensure logs directory exists
$logDir = __DIR__ . '/logs';
if (!is_dir($logDir)) {
    mkdir($logDir, 0777, true);
}

// Receive raw POST data
$input = file_get_contents('php://input');

if ($input) {
    $data = json_decode($input, true);
    if ($data) {
        $date = date('Y-m-d');
        $logFile = $logDir . "/telemetry-{$date}.log";
        
        $logEntry = "[" . date('Y-m-d H:i:s') . "] IP: " . $_SERVER['REMOTE_ADDR'] . "\n";
        $logEntry .= "Session: " . ($data['sessionId'] ?? 'Unknown') . " | URL: " . ($data['url'] ?? 'Unknown') . "\n";
        
        if (!empty($data['events']) && is_array($data['events'])) {
            foreach($data['events'] as $evt) {
                $type = strtoupper($evt['type'] ?? 'UNKNOWN');
                $timestamp = $evt['timestamp'] ?? '';
                $details = json_encode($evt['data'] ?? [], JSON_UNESCAPED_UNICODE);
                $logEntry .= "  -> [$type] $timestamp : $details\n";
            }
        }
        $logEntry .= str_repeat("-", 80) . "\n";
        
        file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
        
        http_response_code(200);
        echo json_encode(["status" => "success"]);
    } else {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Invalid JSON payload"]);
    }
} else {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "No payload received"]);
}
