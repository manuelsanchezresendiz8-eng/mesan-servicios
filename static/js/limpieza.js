// ============================================================
// COTIZADOR LIMPIEZA — MESAN SERVICIOS
// Validación obligatoria: nombre, teléfono, correo
// Monto solo en PDF — no visible en modal
// ============================================================

const SMG_L      = { frontera: 440.62, interior: 248.93 };
const IVA_L      = { frontera: 0.08,   interior: 0.16   };
const MARGENES_L = { gobierno: 0.20, industrial: 0.28, corporativo: 0.35 };

const SERVICIOS_L = {
  oficinas: {
    label:       'Limpieza Corporativa - Oficinas',
    icono:       '🏢',
    m2_x_elem:   500,
    insumos_esp: 800,
    unidad:      'm2',
    default_qty: 300,
    riesgo:      'MEDIO',
    area:        'Espacios de trabajo, salas de juntas y areas comunes'
  },
  escuelas: {
    label:       'Limpieza Institucional - Escuelas',
    icono:       '🏫',
    m2_x_elem:   400,
    insumos_esp: 900,
    unidad:      'm2',
    default_qty: 500,
    riesgo:      'MEDIO-ALTO',
    area:        'Aulas, laboratorios, comedores y areas recreativas'
  },
  hospitales: {
    label:       'Limpieza Sanitaria - Hospitales / Clinicas',
    icono:       '🏥',
    m2_x_elem:   200,
    insumos_esp: 1800,
    unidad:      'm2',
    default_qty: 200,
    riesgo:      'ALTO',
    area:        'Quirofanos, consultorios, pasillos y zonas de alta ocupacion'
  }
};

// ── MOTOR ────────────────────────────────────────────────────
function calcularLimpieza({ servicio, zona, sector, cantidad, turnos, con_insumos }) {
  const srv      = SERVICIOS_L[servicio];
  const smg      = SMG_L[zona];
  const iva      = IVA_L[zona];
  const margen   = MARGENES_L[sector];
  const dias_mes = (6 / 7) * 30;
  const cap      = srv.m2_x_elem * turnos;
  const elementos = Math.ceil(cantidad / cap);
  const nomina    = smg * dias_mes * turnos;
  const carga     = nomina * 0.45;
  const ins_base  = con_insumos ? 1200 : 0;
  const ins_esp   = con_insumos ? srv.insumos_esp : 0;
  const costo_e   = nomina + carga + ins_base + ins_esp;
  const costo_t   = costo_e * elementos;
  const sin_iva   = costo_t / (1 - margen);
  const iva_t     = sin_iva * iva;
  const total     = sin_iva + iva_t;
  return {
    servicio, zona, sector, cantidad, turnos, con_insumos,
    label: srv.label, icono: srv.icono, unidad: srv.unidad,
    riesgo: srv.riesgo, area: srv.area,
    elementos,
    servicio_base: sin_iva,
    insumos_carga: ins_base * elementos + ins_esp * elementos,
    total_neto:    total,
    por_unidad:    total / cantidad,
    tasa_margen:   margen,
    tasa_iva:      iva
  };
}

// ── ESTADO ───────────────────────────────────────────────────
let _srv = null;
let _cot = null;
const fmtL = n => '$' + Math.round(n).toLocaleString('es-MX');
const fmtD = n => '$' + n.toLocaleString('es-MX', { minimumFractionDigits: 1, maximumFractionDigits: 1 });

// ── MODAL ────────────────────────────────────────────────────
function abrirCotLimp(servicio) {
  _srv = servicio;
  _cot = null;
  const srv = SERVICIOS_L[servicio];
  document.getElementById('lmp-titulo').textContent = srv.icono + '  ' + srv.label;
  document.getElementById('lmp-qty').value = srv.default_qty;
  document.getElementById('lmp-acciones').style.display = 'none';
  document.getElementById('lmp-error').style.display = 'none';
  // Limpiar campos cliente
  ['lmp-cliente','lmp-telefono','lmp-correo','lmp-rfc'].forEach(id => {
    const el = document.getElementById(id);
    el.value = '';
    el.classList.remove('error');
  });
  document.getElementById('modal-limp').style.display = 'flex';
}

function cerrarModalLimp() {
  document.getElementById('modal-limp').style.display = 'none';
}

// ── VALIDACIÓN ───────────────────────────────────────────────
function validarCampos() {
  const cliente  = document.getElementById('lmp-cliente').value.trim();
  const telefono = document.getElementById('lmp-telefono').value.trim();
  const correo   = document.getElementById('lmp-correo').value.trim();

  let errores = [];

  document.getElementById('lmp-cliente').classList.remove('error');
  document.getElementById('lmp-telefono').classList.remove('error');
  document.getElementById('lmp-correo').classList.remove('error');

  if (!cliente || cliente.length < 3) {
    errores.push('Ingresa el nombre de la empresa o institución.');
    document.getElementById('lmp-cliente').classList.add('error');
  }

  if (!telefono || !/^\d{10}$/.test(telefono.replace(/\s|-/g, ''))) {
    errores.push('Ingresa un teléfono válido de 10 dígitos.');
    document.getElementById('lmp-telefono').classList.add('error');
  }

  if (!correo || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) {
    errores.push('Ingresa un correo electrónico válido.');
    document.getElementById('lmp-correo').classList.add('error');
  }

  return errores;
}

// ── RECALCULAR ───────────────────────────────────────────────
function recalcularLimp() {
  if (!_srv) return;

  const errores = validarCampos();
  const errorDiv = document.getElementById('lmp-error');

  if (errores.length > 0) {
    errorDiv.textContent = errores[0];
    errorDiv.style.display = 'block';
    document.getElementById('lmp-acciones').style.display = 'none';
    return;
  }

  errorDiv.style.display = 'none';

  const r = calcularLimpieza({
    servicio:    _srv,
    zona:        document.getElementById('lmp-zona').value,
    sector:      document.getElementById('lmp-sector').value,
    cantidad:    parseInt(document.getElementById('lmp-qty').value) || 1,
    turnos:      parseInt(document.getElementById('lmp-turno').value) || 1,
    con_insumos: document.getElementById('lmp-insumos').value === 'si'
  });
  _cot = r;

  // Mostrar nombre empresa en confirmación
  const cliente = document.getElementById('lmp-cliente').value.trim();
  document.getElementById('lmp-nombre-empresa').textContent = cliente.toUpperCase();

  // WhatsApp
  const correo  = document.getElementById('lmp-correo').value.trim();
  const telefono = document.getElementById('lmp-telefono').value.trim();
  const msg = encodeURIComponent(
    'Hola MESAN, requiero cotizacion de ' + r.label + ' para ' + cliente + '. ' +
    r.cantidad + ' m2. Tel: ' + telefono + ' Correo: ' + correo
  );
  document.getElementById('lmp-wa').href = 'https://wa.me/526861629643?text=' + msg;

  // Mostrar acciones
  document.getElementById('lmp-acciones').style.display = 'block';

  // Enviar lead al CRM
  enviarLeadCRM(r, cliente, telefono, correo);
}

// ── ENVIAR AL CRM ─────────────────────────────────────────────
async function enviarLeadCRM(r, cliente, telefono, correo) {
  try {
    const rfc = document.getElementById('lmp-rfc').value.trim();
    await fetch('/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nombre:          cliente,
        servicio:        r.label,
        total_estimado:  Math.round(r.total_neto),
        fecha:           new Date().toLocaleDateString('es-MX'),
        estado:          'nuevo',
        zona:            r.zona === 'frontera' ? 'Mexicali, B.C.' : 'Interior del Pais',
        sector:          r.sector,
        telefono:        telefono,
        correo:          correo,
        rfc:             rfc || ''
      })
    });
  } catch(e) {
    console.log('CRM:', e);
  }
}

// ── PDF ───────────────────────────────────────────────────────
function generarPDFLimp() {
  if (!_cot) return;
  const r       = _cot;
  const cliente = (document.getElementById('lmp-cliente').value.trim() || 'CLIENTE').toUpperCase();
  const correo  = document.getElementById('lmp-correo').value.trim();
  const telefono = document.getElementById('lmp-telefono').value.trim();
  const rfc     = document.getElementById('lmp-rfc').value.trim();
  const zona_txt = r.zona === 'frontera' ? 'Mexicali, B.C.' : 'Interior del Pais';
  const sector_txt = { gobierno: 'Gobierno / Educacion', industrial: 'Industrial / Maquila', corporativo: 'Corporativo / Privado' }[r.sector];
  const turno_txt  = r.turnos === 1 ? '1 turno (8 hrs)' : r.turnos === 2 ? '2 turnos (16 hrs)' : '3 turnos (24 hrs)';
  const fecha  = new Date().toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' });
  const folio  = 'MX-OPS-' + Math.floor(Math.random() * 9000 + 1000);

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: 'pt', format: 'letter' });
  const W   = 612;

  // FONDO
  doc.setFillColor(2, 6, 23);
  doc.rect(0, 0, W, 792, 'F');

  // HEADER
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(22);
  doc.setTextColor(0, 229, 255);
  doc.text('MESAN SERVICIOS', W / 2, 58, { align: 'center' });

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(10);
  doc.setTextColor(200, 210, 220);
  doc.text('Continuidad Operativa', W / 2, 75, { align: 'center' });

  doc.setDrawColor(0, 229, 255);
  doc.setLineWidth(0.5);
  doc.line(40, 85, W - 40, 85);

  // DATOS CLIENTE
  doc.setFontSize(9);
  doc.setTextColor(148, 163, 184);
  doc.text('Cliente: ' + cliente, 40, 102);
  doc.text('Ubicacion: ' + zona_txt, 40, 114);
  if (rfc) doc.text('RFC: ' + rfc.toUpperCase(), 40, 126);
  doc.text('Tel: ' + telefono + '   Correo: ' + correo, 40, rfc ? 138 : 126);
  doc.text('Folio: ' + folio + '   Fecha: ' + fecha, 40, rfc ? 150 : 138);

  let y = rfc ? 174 : 162;

  // CONTEXTO
  const contextos = {
    oficinas:   'Entendemos que la limpieza de oficinas no es un gasto operativo, sino un factor clave de imagen, productividad y bienestar laboral. Un ambiente limpio reduce ausentismo y fortalece la cultura organizacional.',
    escuelas:   'La limpieza institucional en escuelas impacta directamente en la salud, el desempeno academico y el cumplimiento de normativas sanitarias. Un entorno limpio es la base de una educacion de calidad.',
    hospitales: 'En entornos hospitalarios la limpieza es un protocolo critico de bioseguridad. La ausencia de control genera riesgos de infecciones nosocomiales, incumplimiento normativo y responsabilidad legal.'
  };

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('CONTEXTO ESTRATEGICO', 40, y);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);
  doc.setTextColor(200, 210, 220);
  const ctx = doc.splitTextToSize(contextos[r.servicio] || contextos.oficinas, W - 80);
  doc.text(ctx, 40, y + 14);
  y += 14 + ctx.length * 12 + 14;

  // DIAGNÓSTICO
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('DIAGNOSTICO DETECTADO', 40, y);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);
  doc.setTextColor(200, 210, 220);
  const bullets = [
    '- Superficie a cubrir: ' + r.cantidad + ' m2',
    '- Turno de operacion: ' + turno_txt,
    '- Insumos: ' + (r.con_insumos ? 'INCLUIDOS EN PROPUESTA' : 'POR CUENTA DEL CLIENTE'),
    '- Sector: ' + sector_txt
  ];
  bullets.forEach((b, i) => doc.text(b, 40, y + 14 + i * 12));
  y += 14 + bullets.length * 12 + 14;

  // SISTEMA MESAN
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('SISTEMA MESAN INCLUYE:', 40, y);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);
  doc.setTextColor(200, 210, 220);
  const incluye = [
    '- Mano de obra capacitada y certificada en protocolos de higiene y seguridad.',
    '- Supervision monitoreada en tiempo real mediante GPS de asistencia del personal.',
    '- Reporte diario de actividades entregado al responsable de instalaciones.',
    '- Protocolos STPS | Control de calidad por turno | Bitacora operativa mensual.'
  ];
  incluye.forEach((item, i) => {
    const lines = doc.splitTextToSize(item, W - 80);
    doc.text(lines, 40, y + 14 + i * 14);
  });
  y += 14 + incluye.length * 14 + 14;

  // MODELO FINANCIERO
  const boxH = 80;
  doc.setFillColor(15, 23, 42);
  doc.setDrawColor(30, 41, 59);
  doc.setLineWidth(0.5);
  doc.rect(40, y, W - 80, boxH, 'FD');

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('MODELO FINANCIERO', 54, y + 18);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(200, 210, 220);
  doc.text('Servicio Base:  ' + fmtL(r.servicio_base), 54, y + 34);
  doc.text('Insumos/Carga:  ' + (r.con_insumos ? fmtL(r.insumos_carga) : '$0'), 54, y + 48);

  doc.setDrawColor(50, 60, 80);
  doc.line(54, y + 56, W - 54, y + 56);

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.setTextColor(255, 255, 255);
  doc.text('TOTAL NETO MENSUAL:  ' + fmtD(r.total_neto) + ' MXN', 54, y + 72);

  y += boxH + 18;

    // DIFERENCIAL
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('DIFERENCIAL MESAN:', 40, y);
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(200, 210, 220);
  doc.text('No vendemos limpieza. Vendemos CONTINUIDAD operativa.', 40, y + 14);
  y += 36;

  // FIRMA
  doc.setDrawColor(100, 116, 139);
  doc.setLineWidth(0.4);
  doc.line(40, y, 220, y);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(200, 210, 220);
  doc.text('Lic. Manuel Sanchez', 40, y + 13);
  doc.setFontSize(8);
  doc.setTextColor(0, 229, 255);
  doc.text('Direccion General - MESAN SERVICIOS', 40, y + 25);

  // AVISO PRIVACIDAD
  y += 45;
  doc.setFillColor(10, 18, 35);
  doc.rect(40, y, W - 80, 36, 'F');
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(7);
  doc.setTextColor(100, 116, 139);
  const aviso = doc.splitTextToSize(
    'AVISO DE PRIVACIDAD: Los datos proporcionados son tratados de forma confidencial por MESAN SERVICIOS conforme a la Ley Federal de Proteccion de Datos Personales en Posesion de los Particulares (LFPDPPP). No seran compartidos con terceros sin su consentimiento.',
    W - 100
  );
  doc.text(aviso, 50, y + 10);

  // FOOTER
  doc.setDrawColor(0, 229, 255);
  doc.setLineWidth(0.3);
  doc.line(40, 755, W - 40, 755);
  doc.setFontSize(7);
  doc.setTextColor(100, 116, 139);
  doc.text('Propuesta valida 30 dias · Sujeta a visita tecnica · mesanservicios.com', W / 2, 766, { align: 'center' });

  doc.save('Propuesta_MESAN_' + cliente.replace(/\s+/g, '_') + '_' + folio + '.pdf');
}
