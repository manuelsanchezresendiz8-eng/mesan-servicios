<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Limpieza | MESAN Servicios</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{ --bg:#020617; --card:#0f172a; --cyan:#00e5ff; --white:#fff; --muted:#94a3b8; }
*{ margin:0; padding:0; box-sizing:border-box; }
body{ background:var(--bg); color:white; font-family:'DM Sans',sans-serif; }
.back-link{ display:inline-block; margin:20px 20px 0; color:var(--muted); font-size:13px; text-decoration:none; }
.back-link:hover{ color:var(--cyan); }
header{ padding:40px 20px; text-align:center; }
header h1{ font-family:'Syne',sans-serif; font-size:52px; color:var(--cyan); margin-bottom:10px; }
header p{ color:var(--muted); font-size:16px; line-height:1.6; }
.grid{ width:95%; max-width:1200px; margin:auto; display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:24px; padding-bottom:80px; }
.card{ background:var(--card); border-radius:20px; padding:28px; border:1px solid rgba(255,255,255,.05); transition:.3s; }
.card:hover{ transform:translateY(-5px); border-color:rgba(0,229,255,.3); }
.icon{ font-size:42px; margin-bottom:16px; }
.card h2{ font-family:'Syne',sans-serif; color:var(--cyan); margin-bottom:14px; }
.card p{ color:var(--muted); line-height:1.7; margin-bottom:20px; }
.btn{ width:100%; padding:14px; background:var(--cyan); border:none; border-radius:10px; font-family:'Syne',sans-serif; font-weight:800; font-size:13px; cursor:pointer; transition:.2s; }
.btn:hover{ opacity:.85; }
.inp{ width:100%; padding:10px 14px; background:#0f172a; border:1px solid rgba(0,229,255,.15); color:white; border-radius:8px; font-size:13px; outline:none; box-sizing:border-box; }
.inp.error{ border-color:#ef4444 !important; }
.lbl{ font-size:10px; color:var(--cyan); letter-spacing:.08em; text-transform:uppercase; display:block; margin-bottom:5px; }
.seccion{ background:#0a1628; border:1px solid rgba(0,229,255,.08); border-radius:10px; padding:14px; margin-bottom:14px; }
.sec-titulo{ font-size:9px; color:var(--cyan); font-weight:700; letter-spacing:.1em; margin-bottom:12px; }
</style>
</head>
<body>

<a href="/" class="back-link">← Volver al inicio</a>

<header>
  <h1>Limpieza Profesional</h1>
  <p>Cotizaciones operativas para corporativos,<br>instituciones educativas y centros de salud.</p>
</header>

<section class="grid">
  <div class="card">
    <div class="icon">🏢</div>
    <h2>Oficinas Corporativas</h2>
    <p>Limpieza profesional de espacios de trabajo, salas de juntas, áreas comunes y recepciones.</p>
    <button class="btn" onclick="abrirCotLimp('oficinas')">Cotizar servicio</button>
  </div>
  <div class="card">
    <div class="icon">🏫</div>
    <h2>Escuelas e Instituciones</h2>
    <p>Higiene integral en aulas, laboratorios, comedores y áreas recreativas. Cumplimiento de normativas sanitarias.</p>
    <button class="btn" onclick="abrirCotLimp('escuelas')">Cotizar servicio</button>
  </div>
  <div class="card">
    <div class="icon">🏥</div>
    <h2>Hospitales y Clínicas</h2>
    <p>Protocolos de bioseguridad para consultorios, quirófanos y zonas de alta ocupación.</p>
    <button class="btn" onclick="abrirCotLimp('hospitales')">Cotizar servicio</button>
  </div>
</section>

<!-- MODAL -->
<div id="modal-limp" style="position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:1000;backdrop-filter:blur(6px)">
  <div style="background:#08101d;border:1px solid rgba(0,229,255,.2);width:95%;max-width:500px;padding:24px;border-radius:16px;max-height:92vh;overflow-y:auto">

    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <div id="lmp-titulo" style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:var(--cyan)"></div>
      <button onclick="cerrarModalLimp()" style="background:none;border:none;color:var(--muted);cursor:pointer;font-size:20px">✕</button>
    </div>

    <!-- DATOS CLIENTE -->
    <div class="seccion">
      <div class="sec-titulo">DATOS DEL CLIENTE</div>
      <div style="margin-bottom:10px">
        <label class="lbl">Empresa / Institución *</label>
        <input id="lmp-cliente" class="inp" type="text" placeholder="Nombre de la empresa">
      </div>
      <div style="margin-bottom:10px">
        <label class="lbl">Teléfono *</label>
        <input id="lmp-telefono" class="inp" type="tel" placeholder="10 dígitos">
      </div>
      <div style="margin-bottom:10px">
        <label class="lbl">Correo Electrónico *</label>
        <input id="lmp-correo" class="inp" type="email" placeholder="contacto@empresa.com">
      </div>
      <div>
        <label class="lbl">RFC (opcional)</label>
        <input id="lmp-rfc" class="inp" type="text" placeholder="RFC de la empresa" style="text-transform:uppercase">
      </div>
    </div>

    <!-- DATOS SERVICIO -->
    <div class="seccion">
      <div class="sec-titulo">DATOS DEL SERVICIO</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
        <div>
          <label id="lmp-lbl-qty" class="lbl">Superficie (m²)</label>
          <input id="lmp-qty" class="inp" type="number" value="300" min="1">
        </div>
        <div>
          <label class="lbl">Zona</label>
          <select id="lmp-zona" class="inp">
            <option value="frontera">Frontera (IVA 8%)</option>
            <option value="interior">Interior (IVA 16%)</option>
          </select>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
        <div>
          <label class="lbl">Turno</label>
          <select id="lmp-turno" class="inp">
            <option value="1">1 turno (8 hrs)</option>
            <option value="2">2 turnos (16 hrs)</option>
            <option value="3">3 turnos (24 hrs)</option>
          </select>
        </div>
        <div>
          <label class="lbl">Sector</label>
          <select id="lmp-sector" class="inp">
            <option value="gobierno">Gobierno / Educación</option>
            <option value="industrial">Industrial / Maquila</option>
            <option value="corporativo" selected>Corporativo / Privado</option>
          </select>
        </div>
      </div>
      <div>
        <label class="lbl">Insumos</label>
        <select id="lmp-insumos" class="inp">
          <option value="no">Sin insumos — solo mano de obra</option>
          <option value="si">Con insumos incluidos</option>
        </select>
      </div>
    </div>

    <!-- ERROR -->
    <div id="lmp-error" style="display:none;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;padding:10px;margin-bottom:12px;font-size:12px;color:#f87171;text-align:center"></div>

    <!-- BOTÓN CALCULAR -->
    <button onclick="recalcularLimp()" style="width:100%;padding:13px;background:#0f172a;border:1px solid rgba(0,229,255,.4);color:var(--cyan);font-family:'Syne',sans-serif;font-weight:800;font-size:12px;letter-spacing:.08em;cursor:pointer;border-radius:8px;margin-bottom:12px">
      ⚡ CALCULAR COTIZACIÓN
    </button>

    <!-- ACCIONES — solo aparecen después de validar -->
    <div id="lmp-acciones" style="display:none">
      <div style="background:#0f172a;border:1px solid rgba(0,229,255,.15);border-radius:10px;padding:14px;margin-bottom:12px;text-align:center">
        <div style="font-size:11px;color:var(--muted);margin-bottom:4px">Propuesta lista para</div>
        <div id="lmp-nombre-empresa" style="font-size:14px;color:var(--cyan);font-family:'Syne',sans-serif;font-weight:700"></div>
        <div style="font-size:10px;color:var(--muted);margin-top:6px">Descarga el PDF para ver el detalle completo de la cotización</div>
      </div>

      <button onclick="generarPDFLimp()" style="width:100%;padding:14px;background:var(--cyan);border:none;color:#000;font-family:'Syne',sans-serif;font-weight:800;font-size:12px;letter-spacing:.08em;cursor:pointer;border-radius:8px;margin-bottom:10px">
        ⬇ DESCARGAR PROPUESTA PDF
      </button>

      <a id="lmp-wa" href="#" target="_blank" style="display:block;width:100%;padding:13px;background:transparent;border:1px solid #25d366;color:#25d366;font-family:'Syne',sans-serif;font-weight:700;font-size:12px;letter-spacing:.06em;border-radius:8px;text-align:center;text-decoration:none;box-sizing:border-box">
        💬 SOLICITAR POR WHATSAPP
      </a>
    </div>

    <p style="font-size:9px;color:var(--muted);text-align:center;margin-top:14px;line-height:1.5">
      Datos tratados de forma confidencial conforme a la
      <a href="/privacidad" style="color:var(--cyan);text-decoration:none">LFPDPPP</a>.
    </p>

  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="/static/js/limpieza.js?v=4"></script>
</body>
</html>
