<?php
require_once "WORKSPACE/PROJETOS/AfixcontrolAfixgraf/requires/connection.php";
require_once "WORKSPACE/PROJETOS/AfixcontrolAfixgraf/classes/propostas.php";

$proposta_id = 19860; // Just a guess based on user message, but let's get the latest one instead
$stmt = $pdo->query("SELECT proposta_id FROM propostas ORDER BY proposta_id DESC LIMIT 1");
$row = $stmt->fetch();
$id = $row['proposta_id'];

$produtos = Proposta::GetAllProdutos($pdo, $id);
echo "PROPOSTA ID: $id\n";
foreach ($produtos['resultados'] as $p) {
    $resumo = json_decode($p['proposta_resumo'], true);
    echo "PRODUTO: " . ($resumo['produto']['codigo'] ?? 'N/A') . "\n";
    echo "PESO NO RESUMO: " . ($resumo['peso'] ?? 'N/A') . "\n";
    echo "QUANTIDADE: " . ($resumo['quantidade'] ?? 'N/A') . "\n";
    echo "-------------------\n";
}
?>
