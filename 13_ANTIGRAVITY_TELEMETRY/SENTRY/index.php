<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SENTRY V3 - Painel de Controle de Telemetria</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <style>
        :root {
            --bg-dark: #0a0a0c;
            --card-dark: #16161a;
            --primary-neon: #00f2ff;
            --danger-neon: #ff0055;
            --success-neon: #39ff14;
            --text-muted: #8a8a8e;
        }

        body {
            background-color: var(--bg-dark);
            color: white;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
        }

        .sentry-header {
            border-bottom: 1px solid #ffffff10;
            padding: 20px 0;
            background: rgba(10, 10, 12, 0.8);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .neon-text {
            text-shadow: 0 0 10px var(--primary-neon);
            color: var(--primary-neon);
            font-weight: 800;
            letter-spacing: 2px;
        }

        .card-sentry {
            background: var(--card-dark);
            border: 1px solid #ffffff05;
            border-radius: 16px;
            padding: 30px;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .status-badge {
            padding: 8px 20px;
            border-radius: 100px;
            font-size: 0.8rem;
            text-transform: uppercase;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .status-online { background: rgba(57, 255, 20, 0.1); color: var(--success-neon); border: 1px solid var(--success-neon); }
        .status-offline { background: rgba(255, 0, 85, 0.1); color: var(--danger-neon); border: 1px solid var(--danger-neon); }

        .btn-toggle {
            padding: 15px 40px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1.1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            width: 100%;
        }

        .btn-activate { background: var(--primary-neon); color: black; box-shadow: 0 0 20px rgba(0, 242, 255, 0.4); }
        .btn-activate:hover { transform: translateY(-3px); box-shadow: 0 0 40px rgba(0, 242, 255, 0.6); }

        .btn-deactivate { background: #333; color: white; }
        .btn-deactivate:hover { background: var(--danger-neon); color: white; }

        .counter-box {
            text-align: center;
            padding: 20px;
        }

        .counter-value {
            font-size: 4rem;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 5px;
        }

        .pulse {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--success-neon);
            box-shadow: 0 0 0 0 rgba(57, 255, 20, 0.7);
            animation: pulse-green 2s infinite;
        }

        @keyframes pulse-green {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(57, 255, 20, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(57, 255, 20, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(57, 255, 20, 0); }
        }

        .log-box {
            background: #000;
            border-radius: 8px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            height: 300px;
            overflow-y: auto;
            color: #ccc;
        }

        .log-entry { margin-bottom: 5px; border-bottom: 1px solid #222; padding-bottom: 5px; }
        .log-time { color: var(--text-muted); margin-right: 10px; }
        .log-action { color: var(--primary-neon); }

        /* Neural Replay Styles */
        .replay-viewport {
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            min-height: 500px;
            border: 1px solid #ffffff10;
        }

        .replay-img {
            width: 100%;
            height: auto;
            display: block;
        }

        .replay-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.8);
            padding: 15px;
            backdrop-filter: blur(5px);
            border-top: 1px solid #ffffff10;
        }

        .scrubber-container {
            padding: 20px 0;
        }

        .scrubber-slider {
            -webkit-appearance: none;
            width: 100%;
            height: 10px;
            border-radius: 5px;
            background: #333;
            outline: none;
        }

        .scrubber-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--primary-neon);
            cursor: pointer;
            box-shadow: 0 0 10px var(--primary-neon);
        }

        .metadata-pill {
            background: rgba(255,255,255,0.05);
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.75rem;
            color: var(--text-muted);
            border: 1px solid #ffffff10;
        }

        .modal-neon {
            background: var(--bg-dark) !important;
            border: 1px solid #ffffff20;
            box-shadow: 0 0 50px rgba(0, 242, 255, 0.2);
        }

        .modal-header-neon {
            border-bottom: 1px solid #ffffff10;
        }
    </style>
</head>
<body>

<header class="sentry-header">
    <div class="container d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-3">
            <i class="bi bi-shield-lock-fill fs-3 text-primary"></i>
            <h1 class="h4 mb-0 neon-text">SENTRY <span style="color:white; opacity:0.5">V3.0</span></h1>
        </div>
        <div id="status-container">
            <div class="status-badge status-offline">
                <i class="bi bi-circle-fill" style="font-size: 0.5rem"></i> OFFLINE
            </div>
        </div>
    </div>
</header>

<div class="container mt-5">
    <div class="row g-4">
        <!-- Controle principal -->
        <div class="col-lg-6">
            <div class="card-sentry h-100">
                <h5 class="mb-4">CONTROLE OPERACIONAL</h5>
                <p class="text-muted small">Ao ativar o Sentinela, o sistema passará a registrar cada interação visual e erros do motor de cálculo em tempo real.</p>
                
                <div class="mt-5">
                    <div id="mission-controls">
                        <!-- Botões dinâmicos via JS -->
                    </div>
                </div>

                <div class="mt-4 p-3 rounded" style="background: rgba(255,255,255,0.03)">
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="text-muted">Status do Motor</span>
                        <span class="text-success small">Operacional (AES-256)</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Estatísticas e Missão -->
        <div class="col-lg-6">
            <div class="card-sentry h-100">
                <h5 class="mb-4">MISSÃO EM CURSO</h5>
                <div class="p-4 rounded text-center mb-4" style="background: rgba(0,242,255,0.05); border: 1px dashed rgba(0,242,255,0.2)">
                    <code class="text-primary fs-4" id="mission-id">NENHUMA</code>
                </div>
                
                <div class="row text-center mt-5">
                    <div class="col-6 border-end" style="border-color: #333 !important">
                        <div class="h3 mb-0" id="snap-count">0</div>
                        <div class="text-muted small">Snapshots</div>
                    </div>
                    <div class="col-6">
                        <div class="h3 mb-0" id="mission-status-text">--</div>
                        <div class="text-muted small">Status</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Histórico de Missões -->
        <div class="col-12">
            <div class="card-sentry">
                <h5 class="mb-4">HISTÓRICO DE MISSÕES RECENTES</h5>
                <div class="table-responsive">
                    <table class="table table-dark table-hover border-0">
                        <thead>
                            <tr style="border-color: #333">
                                <th>Missão ID</th>
                                <th>Início</th>
                                <th>Fim</th>
                                <th>Snapshots</th>
                                <th>Status</th>
                                <th>Ação</th>
                            </tr>
                        </thead>
                        <tbody id="mission-history">
                            <!-- Injetado via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Logs em tempo real -->
        <div class="col-12">
            <div class="card-sentry">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h5 class="mb-0">TRILHA DE EVIDÊNCIAS DE CAMPO</h5>
                    <button class="btn btn-sm btn-outline-secondary" onclick="clearLogs()">Limpar</button>
                </div>
                <div class="log-box" id="log-box"></div>
            </div>
        </div>
    </div>
</div>

<!-- Modal Neural Replay -->
<div class="modal fade" id="replayModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content modal-neon">
            <div class="modal-header modal-header-neon">
                <h5 class="modal-title neon-text" id="replayTitle">NEURAL REPLAY: CARREGANDO...</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body p-4">
                <div class="row">
                    <div class="col-md-9">
                        <div class="replay-viewport" id="replayViewport">
                            <div class="d-flex align-items-center justify-content-center h-100" id="replayLoader">
                                <div class="spinner-border text-primary" role="status"></div>
                            </div>
                            <img src="" id="replayImage" class="replay-img d-none">
                            <div class="replay-overlay d-none" id="replayMetadata">
                                <div class="d-flex gap-3 flex-wrap">
                                    <span class="metadata-pill" id="meta-time"></span>
                                    <span class="metadata-pill" id="meta-action"></span>
                                    <span class="metadata-pill" id="meta-url"></span>
                                    <span class="metadata-pill" id="meta-screen"></span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="scrubber-container">
                            <input type="range" class="scrubber-slider" id="scrubber" min="0" max="0" value="0">
                            <div class="d-flex justify-content-between mt-2 small text-muted">
                                <span id="scrubber-current">Snapshot 0/0</span>
                                <span id="scrubber-timestamp">--:--:--</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <h6 class="text-white mb-3">CONCEITO ISO FORENSE</h6>
                        <div class="p-3 rounded mb-3" style="background: rgba(255,255,255,0.03); font-size: 0.85rem">
                            <p class="text-muted mb-2"><strong>Interpretação da IA:</strong></p>
                            <div id="ai-interpretation" class="text-white fw-bold mb-3" style="line-height: 1.4">Aguardando telemetria...</div>
                            
                            <p class="text-muted mb-2"><strong>Análise de Impacto:</strong></p>
                            <div id="forensic-summary" class="text-info">Protocolo de segurança ativo.</div>
                            <hr style="opacity:0.1">
                            <div class="d-grid gap-2">
                                <button id="btn-gerar-saga" class="btn btn-sm btn-primary" onclick="gerarSagaIA()">
                                    <i class="bi bi-magic me-2"></i> GERAR SAGA COM IA
                                </button>
                                <button class="btn btn-sm btn-outline-info" onclick="copySnapshotURL()">Copiar URL da Evidência</button>
                                <button class="btn btn-sm btn-outline-primary" onclick="viewFullLog()">Ver Log Completo</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
    let isMonitoring = false;
    let currentMission = "";

    const MISSION_TYPES = {
        'STEALTH': { name: 'MAPEAMENTO STEALTH', color: '#00f2ff', icon: 'bi-eye-slash-fill', btnClass: 'btn-outline-info' },
        'RECON': { name: 'RECONHECIMENTO', color: '#ff0055', icon: 'bi-bug-fill', btnClass: 'btn-outline-danger' },
        'AUDIT': { name: 'AUDITORIA', color: '#39ff14', icon: 'bi-shield-check', btnClass: 'btn-outline-success' },
        'INFILTRATION': { name: 'INFILTRAÇÃO', color: '#ffffff', icon: 'bi-incognito', btnClass: 'btn-outline-light' }
    };

    function updateDashboard() {
        $.post('collector.php', { action: 'get_status' }, function(data) {
            isMonitoring = data.active;
            currentMission = data.current_mission;

            // Update Status Header
            const container = $('#status-container');
            if (isMonitoring) {
                container.html('<div class="status-badge status-online"><div class="pulse"></div> MISSION ACTIVE</div>');
            } else {
                container.html('<div class="status-badge status-offline">STANDBY</div>');
            }

            // Update Mission Info
            $('#mission-id').text(currentMission || "ESTRUTURA STANDBY");
            $('#snap-count').text(data.total_snapshots || 0);
            $('#mission-status-text').text(isMonitoring ? "CAPTURING" : "IDLE");

            // Update Buttons
            const controls = $('#mission-controls');
            if (isMonitoring) {
                controls.html(`
                    <button class="btn-toggle btn-deactivate bg-danger text-white w-100 p-3 rounded-3 fw-bold" onclick="endMission()">
                        <i class="bi bi-stop-circle-fill me-2"></i> ENCERRAR MISSÃO E ANALISAR
                    </button>
                `);
            } else {
                let buttons = '<div class="row g-2">';
                Object.keys(MISSION_TYPES).forEach(type => {
                    const m = MISSION_TYPES[type];
                    buttons += `
                        <div class="col-6">
                            <button class="btn ${m.btnClass} w-100 py-3 d-flex flex-column align-items-center gap-2 fw-bold" onclick="startMission('${type}')">
                                <i class="bi ${m.icon} fs-4"></i>
                                <span style="font-size: 0.7rem">${m.name}</span>
                            </button>
                        </div>
                    `;
                });
                buttons += '</div>';
                controls.html(buttons);
            }

            // Update History
            let historyHtml = "";
            if (data.history && data.history.length > 0) {
                data.history.forEach(m => {
                    const statusClass = m.status === 'IN_PROGRESS' ? 'text-primary' : 'text-success';
                    const typeConfig = MISSION_TYPES[m.type] || MISSION_TYPES.STEALTH;
                    historyHtml += `
                        <tr style="border-color: #222">
                            <td>
                                <i class="bi ${typeConfig.icon} me-2" style="color: ${typeConfig.color}"></i>
                                <code>${m.id}</code>
                            </td>
                            <td>${m.start}</td>
                            <td>${m.end || '--'}</td>
                            <td>${m.snapshots}</td>
                            <td class="${statusClass} fw-bold">${m.status}</td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary py-0" onclick="explorarMissao('${m.id}')">Explorar</button>
                            </td>
                        </tr>
                    `;
                });
            }
            $('#mission-history').html(historyHtml);
        }, 'json');
    }

    function startMission(type) {
        $.post('collector.php', { action: 'start_mission', type: type }, function(data) {
            if (data.success) {
                localStorage.setItem('sentry_active', 'true');
                localStorage.setItem('sentry_mission_id', data.mission);
                addLog(`Missão ${type} iniciada: ${data.mission}`);
                updateDashboard();
            }
        }, 'json');
    }

    function endMission() {
        if (confirm("Deseja encerrar a missão e marcar para análise?")) {
            $.post('collector.php', { action: 'end_mission' }, function() {
                localStorage.setItem('sentry_active', 'false');
                localStorage.removeItem('sentry_mission_id');
                addLog("Missão encerrada. Relatório pendente.");
                updateDashboard();
            });
        }
    }

    function addLog(message) {
        const time = new Date().toLocaleTimeString();
        const entry = `<div class="log-entry"><span class="log-time">${time}</span> <span class="log-action">${message}</span></div>`;
        $('#log-box').prepend(entry);
    }

    let missionSnapshots = [];
    function explorarMissao(missionId) {
        $('#replayModal').modal('show');
        $('#replayTitle').text(`NEURAL REPLAY: ${missionId}`);
        $('#replayLoader').removeClass('d-none');
        $('#replayImage').addClass('d-none');
        $('#replayMetadata').addClass('d-none');
        
        $.get('collector.php', { action: 'list_snapshots', mission_id: missionId }, function(data) {
            if (data.success && data.snapshots.length > 0) {
                missionSnapshots = data.snapshots;
                $('#scrubber').attr('max', missionSnapshots.length - 1).val(0);
                updateReplayView(0);
                $('#replayLoader').addClass('d-none');
                $('#replayImage').removeClass('d-none');
                $('#replayMetadata').removeClass('d-none');
                
                // Resumo ISO Básico
                $('#forensic-summary').text(`${missionSnapshots.length} evidências capturadas sob protocolo de segurança.`);

                // Carregar Saga Persistida se houver
                if (data.saga) {
                    $('#ai-interpretation').html(data.saga.saga);
                    $('#btn-gerar-saga').html('<i class="bi bi-check-all me-2"></i>SAGA GERADA').addClass('btn-success').removeClass('btn-primary');
                } else {
                    $('#ai-interpretation').html('Aguardando telemetria...');
                    $('#btn-gerar-saga').html('<i class="bi bi-magic me-2"></i> GERAR SAGA COM IA').addClass('btn-primary').removeClass('btn-success');
                }
            } else {
                $('#replayLoader').html('<div class="text-danger">Nenhum snapshot encontrado para esta missão.</div>');
            }
        });
    }

    function updateReplayView(index) {
        const snap = missionSnapshots[index];
        if (!snap) return;

        // Atualizar Imagem (usando o JPG se existir)
        const imgUrl = snap.jpg_url || 'assets/images/no-image.png'; // Fallback
        $('#replayImage').attr('src', imgUrl);

        // Atualizar Metadados
        const meta = snap.metadata.metadata || {};
        $('#meta-time').html(`<i class="bi bi-clock"></i> ${snap.metadata.timestamp}`);
        $('#meta-action').html(`<i class="bi bi-cursor-fill"></i> ${meta.action || 'auto'}`);
        $('#meta-url').html(`<i class="bi bi-link-45deg"></i> ${meta.url || '--'}`);
        $('#meta-screen').html(`<i class="bi bi-display"></i> ${meta.screen_size || '--'}`);
        
        $('#scrubber-current').text(`Snapshot ${parseInt(index) + 1}/${missionSnapshots.length}`);
        $('#scrubber-timestamp').text(snap.metadata.timestamp.split(' ')[1]);

        // Tradução para Leigos (IA Interpretation)
        let desc = "O sistema registrou o estado da tela.";
        if (meta.action === 'click') desc = `O usuário <b>clicou</b> em um elemento da página.`;
        if (meta.action === 'input') desc = `O usuário está <b>digitando</b> informações nos campos.`;
        if (meta.action === 'load') desc = `A página foi <b>carregada</b> ou atualizada pelo navegador.`;
        if (meta.action === 'error') desc = `<span class="text-danger">⚠️ Um <b>erro técnico</b> foi detectado neste exato momento!</span>`;
        if (meta.action === 'audit_fix') desc = `<span class="text-success">🛡️ A <b>Proteção Antigravity</b> atuou para corrigir um valor inválido.</span>`;
        
        $('#ai-interpretation').html(desc);
    }

    $('#scrubber').on('input', function() {
        updateReplayView($(this).val());
    });

    function copySnapshotURL() {
        const index = $('#scrubber').val();
        const snap = missionSnapshots[index];
        if (snap) {
            const url = window.location.href.split('index.php')[0] + snap.json_url;
            navigator.clipboard.writeText(url).then(() => {
                alert("URL da evidência copiada para o clipboard!");
            });
        }
    }

    function viewFullLog() {
        const index = $('#scrubber').val();
        const snap = missionSnapshots[index];
        if (snap) {
            window.open(snap.json_url, '_blank');
        }
    }

    function clearLogs() {
        $('#log-box').html('');
    }

    function gerarSagaIA() {
        const btn = $('#btn-gerar-saga');
        const container = $('#ai-interpretation');
        const missionId = $('#replayTitle').text().replace('NEURAL REPLAY: ', '');

        btn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-2"></span>PROCESSANDO...');
        container.html('<div class="text-info"><i class="bi bi-hourglass-split me-2"></i>Interpretando eventos da missão...</div>');

        $.post('../backend/translator.php', { mission_id: missionId }, function(data) {
            if (data.success) {
                container.fadeOut(200, function() {
                    $(this).html(data.saga).fadeIn(200);
                });
                btn.html('<i class="bi bi-check-all me-2"></i>SAGA GERADA').addClass('btn-success').removeClass('btn-primary').prop('disabled', false);
            } else {
                container.html(`<div class="text-danger">⚠️ ${data.error || 'Erro na interpretação'}</div>`);
                btn.prop('disabled', false).text('TENTAR NOVAMENTE');
            }
        }, 'json').fail(function() {
            container.html('<div class="text-danger">⚠️ Falha crítica no tradutor.</div>');
            btn.prop('disabled', false).text('TENTAR NOVAMENTE');
        });
    }

    // Polling para atualizar o contador
    setInterval(updateDashboard, 2000);
    updateDashboard();
</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
