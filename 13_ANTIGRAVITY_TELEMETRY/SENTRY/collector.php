<?php
// collector.php - Receptor de Telemetria Nível Militar
header('Content-Type: application/json');

$config_file = __DIR__ . '/config.json';
$snapshots_dir = __DIR__ . '/snapshots';

if (!file_exists($snapshots_dir)) {
    mkdir($snapshots_dir, 0777, true);
}

// DEBUG LOGGING (Standard)
$debug_file = __DIR__ . '/debug.log';
if (isset($_REQUEST['action']) && $_REQUEST['action'] !== 'get_status') {
    $log_entry = "[" . date('Y-m-d H:i:s') . "] ACTION: " . $_REQUEST['action'] . PHP_EOL;
    file_put_contents($debug_file, $log_entry, FILE_APPEND);
}

$action = $_REQUEST['action'] ?? null;

// Carregar configuração atual
$config = json_decode(file_get_contents($config_file), true);

$missions_file = __DIR__ . '/missions.json';
if (!file_exists($missions_file)) {
    file_put_contents($missions_file, json_encode([], JSON_PRETTY_PRINT));
}

if ($action === 'start_mission') {
    $type = $_REQUEST['type'] ?? 'STEALTH';
    $mission_id = $type . '-' . date('Ymd-His');
    $config['active'] = true;
    $config['current_mission'] = $mission_id;
    
    $mission_dir = $snapshots_dir . '/' . $mission_id;
    if (!file_exists($mission_dir)) {
        mkdir($mission_dir, 0777, true);
    }
    
    // Registrar na história
    $missions = json_decode(file_get_contents($missions_file), true);
    $missions[] = [
        'id' => $mission_id,
        'type' => $type,
        'start' => date('Y-m-d H:i:s'),
        'end' => null,
        'status' => 'IN_PROGRESS',
        'snapshots' => 0
    ];
    file_put_contents($missions_file, json_encode($missions, JSON_PRETTY_PRINT));
    
    file_put_contents($config_file, json_encode($config, JSON_PRETTY_PRINT));
    echo json_encode(['success' => true, 'mission' => $mission_id]);
    exit;
}

if ($action === 'end_mission') {
    $mission_id = $config['current_mission'];
    $config['active'] = false;
    $config['current_mission'] = "";
    
    // Atualizar história
    $missions = json_decode(file_get_contents($missions_file), true);
    foreach ($missions as &$m) {
        if ($m['id'] === $mission_id) {
            $m['end'] = date('Y-m-d H:i:s');
            $m['status'] = 'AWAITING_ANALYSIS';
            // Contar snapshots na pasta
            $files = glob($snapshots_dir . '/' . $mission_id . '/*.json');
            $m['snapshots'] = count($files);
        }
    }
    file_put_contents($missions_file, json_encode($missions, JSON_PRETTY_PRINT));
    
    file_put_contents($config_file, json_encode($config, JSON_PRETTY_PRINT));
    echo json_encode(['success' => true]);
    exit;
}

if ($action === 'list_snapshots') {
    $mission_id = $_GET['mission_id'] ?? null;
    if (!$mission_id) {
        echo json_encode(['success' => false, 'message' => 'Mission ID required']);
        exit;
    }
    
    $mission_dir = $snapshots_dir . '/' . $mission_id;
    if (!file_exists($mission_dir)) {
        echo json_encode(['success' => false, 'message' => 'Mission directory not found']);
        exit;
    }
    
    $json_files = glob($mission_dir . '/*.json');
    $snapshots = [];
    
    foreach ($json_files as $file) {
        $id_full = basename($file, '.json');
        $id = str_replace('snap-', '', $id_full);
        
        $jpg = $mission_dir . '/' . $id_full . '.jpg';
        $content = json_decode(file_get_contents($file), true);
        
        // Remover DOM pesado do list para preservar performance
        unset($content['dom_state']);
        
        $snapshots[] = [
            'id' => $id,
            'json_url' => 'snapshots/' . $mission_id . '/' . basename($file),
            'jpg_url' => file_exists($jpg) ? 'snapshots/' . $mission_id . '/' . basename($jpg) : null,
            'metadata' => $content
        ];
    }
    
    // Ordenar cronologicamente por ID (timestamp)
    usort($snapshots, function($a, $b) {
        return strcmp($a['id'], $b['id']);
    });
    
    // Verificar se existe interpretação da IA (Saga)
    $saga_file = $mission_dir . '/saga_interpretation.json';
    $saga_data = file_exists($saga_file) ? json_decode(file_get_contents($saga_file), true) : null;
    
    echo json_encode(['success' => true, 'snapshots' => $snapshots, 'saga' => $saga_data]);
    exit;
}

if ($action === 'get_status') {
    $missions = json_decode(file_get_contents($missions_file), true);
    $config['history'] = array_reverse(array_slice($missions, -10)); // Últimas 10 missões para melhor visão
    echo json_encode($config);
    exit;
}

if ($action === 'save_log') {
    $msg = $_POST['msg'] ?? '';
    $level = $_POST['level'] ?? 'info';
    $mission_id = $_POST['mission_id'] ?? $config['current_mission'];
    
    if ($mission_id) {
        $log_file = $snapshots_dir . '/' . $mission_id . '/mission_events.log';
        $entry = "[" . date('Y-m-d H:i:s') . "] [$level] $msg" . PHP_EOL;
        file_put_contents($log_file, $entry, FILE_APPEND);
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => 'No active mission for log']);
    }
    exit;
}

if ($action === 'save_snapshot') {
    if (!$config['active']) {
        echo json_encode(['success' => false, 'message' => 'Telemetry is inactive']);
        exit;
    }

    $data = $_POST['data'] ?? null;
    $metadata = $_POST['metadata'] ?? null;
    $visual = $_POST['visual'] ?? null; // Novo: Imagem visual
    
    if ($data) {
        $snapshot_id = time() . '-' . rand(100, 999);
        $meta_data = json_decode($metadata, true);
        
        // Determinar o diretório de destino
        $target_dir = $snapshots_dir;
        $active_mission = $config['current_mission'];
        
        // Priorizar a missão enviada pelo cliente (para evitar race conditions no fechamento da missão)
        if (!empty($meta_data['mission_id'])) {
            $active_mission = $meta_data['mission_id'];
        }

        if (!empty($active_mission)) {
            $mission_dir = $snapshots_dir . '/' . $active_mission;
            if (!file_exists($mission_dir)) {
                @mkdir($mission_dir, 0777, true);
            }
            if (file_exists($mission_dir)) {
                $target_dir = $mission_dir;
            }
        }

        $filename = $target_dir . '/snap-' . $snapshot_id . '.json';
        
        // Salvar JSON de Dados
        $payload = [
            'id' => $snapshot_id,
            'timestamp' => date('Y-m-d H:i:s'),
            'mission' => $config['current_mission'] ?? 'LEGACY',
            'metadata' => json_decode($metadata, true),
            'dom_state' => $data
        ];
        
        file_put_contents($filename, json_encode($payload));

        // Salvar Imagem Visual (se houver)
        if ($visual && strpos($visual, 'data:image/jpeg;base64,') === 0) {
            $imageData = base64_decode(str_replace('data:image/jpeg;base64,', '', $visual));
            $imageFilename = $target_dir . '/snap-' . $snapshot_id . '.jpg';
            file_put_contents($imageFilename, $imageData);
        }
        
        $config['total_snapshots']++;
        file_put_contents($config_file, json_encode($config, JSON_PRETTY_PRINT));
        
        echo json_encode(['success' => true, 'id' => $snapshot_id, 'total' => $config['total_snapshots']]);
        exit;
    }
}

echo json_encode(['success' => false, 'message' => 'Invalid action']);
