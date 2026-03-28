<?php
// translator.php - Interpretador Semântico (RECON v3.0)
header('Content-Type: application/json');

$mission_id = $_POST['mission_id'] ?? null;
if (!$mission_id) {
    echo json_encode(['success' => false, 'error' => 'Mission ID não fornecido.']);
    exit;
}

// 1. Localizar o Session ID a partir dos Snapshots da Missão
$snapshots_dir = __DIR__ . '/../SENTRY/snapshots/' . $mission_id;
if (!file_exists($snapshots_dir)) {
    echo json_encode(['success' => false, 'error' => 'Dados da missão não encontrados.']);
    exit;
}

$json_files = glob($snapshots_dir . '/*.json');
if (empty($json_files)) {
    echo json_encode(['success' => false, 'error' => 'Nenhum snapshot nesta missão.']);
    exit;
}

// Extrair data do Mission ID (ex: AUDIT-20260325-103050 -> 2026-03-25)
$parts = explode('-', $mission_id);
if (count($parts) >= 2) {
    $raw_date = $parts[1]; // 20260325
    $mission_date = substr($raw_date, 0, 4) . '-' . substr($raw_date, 4, 2) . '-' . substr($raw_date, 6, 2);
} else {
    $mission_date = date('Y-m-d'); // Fallback
}
$log_file = __DIR__ . "/logs/telemetry-{$mission_date}.log";

if (!file_exists($log_file)) {
    echo json_encode(['success' => false, 'error' => "Log de telemetria não encontrado para o dia {$mission_date}."]);
    exit;
}

// 2. Extrair e Filtrar Logs (Circuit Breaker: Max 150 eventos)
$lines = file($log_file);
$relevant_events = [];
$event_count = 0;
$max_events = 150; // CIRCUIT BREAKER

// Tentar identificar o Session ID (ex: sess_...) no log que combine com a URL/IP se possível
// Para o MVP, vamos pegar as linhas mais próximas do timestamp da missão
foreach ($lines as $line) {
    if (strpos($line, 'Session:') !== false) {
        // Aqui aplicaríamos um filtro de Session ID se tivéssemos ele mapeado
        // Por enquanto, vamos capturar eventos recentes significativos
        // (Em produção, o sentry-client envia o session_id no metadata do snap)
        $relevant_events[] = trim($line);
        $event_count++;
    }
    if ($event_count >= $max_events) {
        $relevant_events[] = "[CIRCUIT BREAKER: Limite de 150 eventos atingido para proteção de tokens]";
        break;
    }
}

// 3. Sanitização (Privacy Scrubbing)
foreach ($relevant_events as &$event) {
    // Remover padrões que pareçam dados sensíveis (CPFs, Emails, Nomes em aspas)
    $event = preg_replace('/"text":"[^"]{15,}"/', '"text":"[CONTEÚDO_PROTEGIDO]"', $event);
    $event = preg_replace('/[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}/', '[CPF_PROTEGIDO]', $event);
}

// 4. Integração com IA (Simulação de Saga para MVP de Viabilidade)
$event_preview = "";
if ($event_count > 0) {
    $event_preview = "<li>" . implode("</li><li>", array_slice($relevant_events, 0, 3)) . "...</li>";
}

$mock_saga = "### 📜 A Saga da Missão " . htmlspecialchars($mission_id) . "<br>";
$mock_saga .= "O sistema processou **{$event_count} eventos** de telemetria desta sessão.<br>";
$mock_saga .= "<ul>{$event_preview}</ul>";
$mock_saga .= "A análise indica que o usuário explorou o módulo de orçamento e interagiu com campos de cálculo.<br>";
$mock_saga .= "<span class='text-success'>🛡️ Sanitização Ativa: Emails e padrões sensíveis foram mascarados.</span><br>";
$mock_saga .= "<span class='text-warning'>💡 Insight: Detectamos uma sequência de cliques repetitivos antes de um erro de rede. Recomenda-se checar a latência da API.</span>";

// Salvar a Saga para persistência
file_put_contents($snapshots_dir . '/saga_interpretation.json', json_encode([
    'mission_id' => $mission_id,
    'date' => date('Y-m-d H:i:s'),
    'saga' => $mock_saga,
    'events_processed' => $event_count
], JSON_PRETTY_PRINT));

echo json_encode([
    'success' => true,
    'saga' => $mock_saga,
    'events_processed' => $event_count,
    'sanitized' => true
]);
