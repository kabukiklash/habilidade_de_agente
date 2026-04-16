<?php
/**
 * Antigravity Telemetry Backend Helper
 * Correlates PHP execution with Frontend Trace IDs.
 */

class AGTelemetry {
    private static $traceId = null;
    private static $logDir = null;

    public static function init() {
        self::$logDir = __DIR__ . '/logs';
        
        // Capture Trace ID from Header
        if (isset($_SERVER['HTTP_X_AG_TRACE_ID'])) {
            self::$traceId = $_SERVER['HTTP_X_AG_TRACE_ID'];
        } else {
            self::$traceId = 'server_side_' . uniqid();
        }
    }

    public static function log($message, $data = []) {
        if (!self::$logDir) self::init();

        $date = date('Y-m-d');
        $logFile = self::$logDir . "/telemetry-{$date}.log";

        if (!is_dir(self::$logDir)) {
            mkdir(self::$logDir, 0777, true);
        }

        $timestamp = date('Y-m-d H:i:s');
        $details = !empty($data) ? " : " . json_encode($data, JSON_UNESCAPED_UNICODE) : "";
        
        $logEntry = "[$timestamp] IP: " . $_SERVER['REMOTE_ADDR'] . "\n";
        $logEntry .= "Session: " . (isset($_SESSION['id']) ? $_SESSION['id'] : 'PHP_SESS') . " | URL: " . $_SERVER['REQUEST_URI'] . "\n";
        $logEntry .= "  -> [BACKEND] " . date('c') . " [Trace: " . self::$traceId . "] : $message $details\n";
        $logEntry .= str_repeat("-", 80) . "\n";

        file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
    }

    public static function getTraceId() {
        if (!self::$traceId) self::init();
        return self::$traceId;
    }
}

// Shortcut function
function AG_TraceLog($message, $data = []) {
    AGTelemetry::log($message, $data);
}
