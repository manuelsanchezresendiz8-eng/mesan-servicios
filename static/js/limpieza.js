// ============================================================
// COTIZADOR LIMPIEZA + PDF — MESAN SERVICIOS
// Servicios: Oficinas, Escuelas/Instituciones, Hospitales/Clínicas
// ============================================================

const SMG_L      = { frontera: 440.62, interior: 248.93 };
const IVA_L      = { frontera: 0.08,   interior: 0.16   };
const MARGENES_L = { gobierno: 0.20, industrial: 0.28, corporativo: 0.35 };

const SERVICIOS_L = {
  oficinas: {
    label:       'Limpieza Corporativa — Oficinas',
    icono:       '🏢',
    m2_x_elem:   500,
    insumos_esp: 800,
    unidad:      'm²',
    default_qty: 300,
    riesgo:      'MEDIO',
    area:        'Espacios de trabajo, salas de juntas y áreas comunes'
  },
  escuelas: {
    label:       'Limpieza Institucional — Escuelas',
    icono:       '🏫',
    m2_x_elem:   400,
    insumos_esp: 900,
    unidad:      'm²',
    default_qty: 500,
    riesgo:      'MEDIO-ALTO',
    area:        'Aulas, laboratorios, comedores y áreas recreativas'
  },
  hospitales: {
    label:       'Limpieza Sanitaria — Hospitales / Clínicas',
    icono:       '🏥',
    m2_x_elem:   200,
    insumos_esp: 1800,
    unidad:      'm²',
    default_qty: 200,
    riesgo:      'ALTO',
    area:        'Quirófanos, consultorios, pasillos y zonas de alta ocupación'
  }
};

// ── MOTOR SMG ────────────────────────────────────────────────
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
let _srv    = null;
let _cot    = null;
const fmtL  = n => '$' + Math.round(n).toLocaleString('es-MX');
const fmtD  = n => '$' + n.toLocaleString('es-MX', { minimumFractionDigits: 1, maximumFractionDigits: 1 });

// ── MODAL ────────────────────────────────────────────────────
function abrirCotLimp(servicio) {
  _srv = servicio;
  const srv = SERVICIOS_L[servicio];
  document.getElementById('lmp-titulo').textContent  = srv.icono + '  ' + srv.label;
  document.getElementById('lmp-lbl-qty').textContent = 'Superficie (m²)';
  document.getElementById('lmp-qty').value = srv.default_qty;
  document.getElementById('modal-limp').style.display = 'flex';
  recalcularLimp();
}

function cerrarModalLimp() {
  document.getElementById('modal-limp').style.display = 'none';
}

// ── RECALCULAR ───────────────────────────────────────────────
function recalcularLimp() {
  if (!_srv) return;
  const r = calcularLimpieza({
    servicio:    _srv,
    zona:        document.getElementById('lmp-zona').value,
    sector:      document.getElementById('lmp-sector').value,
    cantidad:    parseInt(document.getElementById('lmp-qty').value) || 1,
    turnos:      parseInt(document.getElementById('lmp-turno').value) || 1,
    con_insumos: document.getElementById('lmp-insumos').value === 'si'
  });
  _cot = r;

  document.getElementById('lmp-r-base').textContent  = fmtL(r.servicio_base);
  document.getElementById('lmp-r-ins').textContent   = r.con_insumos ? fmtL(r.insumos_carga) : '$0';
  document.getElementById('lmp-r-total').textContent = fmtD(r.total_neto) + ' MXN/mes';
  document.getElementById('lmp-r-unidad').textContent = fmtL(r.por_unidad) + ' por ' + r.unidad;
  document.getElementById('lmp-preview').style.display = 'block';

  const cliente = document.getElementById('lmp-cliente').value || 'su empresa';
  const msg = encodeURIComponent(
    `Hola MESAN, requiero cotización de ${r.label} para ${cliente}. ` +
    `${r.cantidad} ${r.unidad}s. Total estimado: ${fmtL(r.total_neto)} MXN/mes.`
  );
  document.getElementById('lmp-wa').href = `https://wa.me/526861629643?text=${msg}`;
}

// ── PDF — FORMATO PROPUESTA MESAN ────────────────────────────
function generarPDFLimp() {
  if (!_cot) return;
  const r       = _cot;
  const cliente = (document.getElementById('lmp-cliente').value.trim() || 'CLIENTE').toUpperCase();
  const zona_txt = r.zona === 'frontera' ? 'Mexicali, B.C.' : 'Interior del País';
  const sector_txt = { gobierno: 'Gobierno / Educación', industrial: 'Industrial / Maquila', corporativo: 'Corporativo / Privado' }[r.sector];
  const turno_txt  = r.turnos === 1 ? '1 turno (8 hrs)' : r.turnos === 2 ? '2 turnos (16 hrs)' : '3 turnos (24 hrs)';
  const fecha  = new Date().toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' });
  const folio  = 'MX-OPS-' + Math.floor(Math.random() * 9000 + 1000);

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: 'pt', format: 'letter' });
  const W   = 612;

  // FONDO NEGRO
  doc.setFillColor(2, 6, 23);
  doc.rect(0, 0, W, 792, 'F');

  // HEADER
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(22);
  doc.setTextColor(0, 229, 255);
  doc.setCharSpace(3);
  doc.text('MESAN SERVICIOS ©', W / 2, 58, { align: 'center' });
  doc.setCharSpace(0);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(10);
  doc.setTextColor(200, 210, 220);
  doc.text('Continuidad Operativa Industrial', W / 2, 75, { align: 'center' });

  doc.setDrawColor(0, 229, 255);
  doc.setLineWidth(0.5);
  doc.line(40, 85, W - 40, 85);

  // DATOS CLIENTE
  doc.setFontSize(9);
  doc.setTextColor(148, 163, 184);
  doc.text('Cliente: ' + cliente, 40, 102);
  doc.text('Ubicación: ' + zona_txt, 40, 114);
  doc.text('Folio: ' + folio, 40, 126);
  doc.text('Fecha: ' + fecha, 40, 138);

  // CONTEXTO ESTRATÉGICO
  let y = 162;
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('CONTEXTO ESTRATÉGICO', 40, y);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);
  doc.setTextColor(200, 210, 220);

  const contextos = {
    oficinas:   'Entendemos que la limpieza de oficinas no es un gasto operativo, sino un factor clave de imagen, productividad y bienestar laboral. Un ambiente limpio reduce ausentismo y fortalece la cultura organizacional.',
    escuelas:   'La limpieza institucional en escuelas impacta directamente en la salud, el desempeño académico y el cumplimiento de normativas sanitarias. Un entorno limpio es la base de una educación de calidad.',
    hospitales: 'En entornos hospitalarios, la limpieza no es opcional: es un protocolo crítico de bioseguridad. La ausencia de control genera riesgos de infecciones nosocomiales, incumplimiento normativo y responsabilidad legal.'
  };

  const ctx = doc.splitTextToSize(contextos[r.servicio] || contextos.oficinas, W - 80);
  doc.text(ctx, 40, y + 14);
  y += 14 + ctx.length * 12;

  // DIAGNÓSTICO DETECTADO
  y += 14;
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('DIAGNÓSTICO DETECTADO', 40, y);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);
  doc.setTextColor(200, 210, 220);
  const bullets = [
    '• Nivel de Riesgo Operativo: ' + r.riesgo,
    '• Área Crítica: ' + r.area,
    '• Superficie a cubrir: ' + r.cantidad + ' m²',
    '• Turno de operación: ' + turno_txt,
    '• Insumos: ' + (r.con_insumos ? 'INCLUIDOS EN PROPUESTA' : 'POR CUENTA DEL CLIENTE'),
    '• Sector: ' + sector_txt,
  ];
  bullets.forEach((b, i) => doc.text(b, 40, y + 14 + i * 12));
  y += 14 + bullets.length * 12;

  // SISTEMA MESAN
  y += 14;
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('SISTEMA MESAN © INCLUYE:', 40, y);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8.5);
  doc.setTextColor(200, 210, 220);
  const incluyeItems = [
    '✔  Mano de obra capacitada y certificada en protocolos de higiene y seguridad.',
    '✔  Supervisión monitoreada en tiempo real mediante GPS de asistencia del personal.',
    '✔  Reporte diario de actividades entregado al responsable de instalaciones.',
    '✔  Protocolos STPS  |  Control de calidad por turno  |  Bitácora operativa mensual.'
  ];
  incluyeItems.forEach((item, i) => doc.text(item, 40, y + 14 + i * 12));
  y += 14 + incluyeItems.length * 12 + 6;

  // MODELO FINANCIERO
  y += 6;
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
  doc.text('Servicio Base ©:  ' + fmtL(r.servicio_base), 54, y + 34);
  doc.text('Insumos/Carga:  ' + (r.con_insumos ? fmtL(r.insumos_carga) : '$0'), 54, y + 48);

  doc.setDrawColor(50, 60, 80);
  doc.line(54, y + 56, W - 54, y + 56);

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.setTextColor(255, 255, 255);
  doc.text('TOTAL NETO MENSUAL:  ' + fmtD(r.total_neto), 54, y + 72);

  y += boxH + 18;

  // PÉRDIDAS POTENCIALES
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(8);
  doc.setTextColor(248, 113, 113);
  doc.text(
    'Este modelo previene pérdidas potenciales de $150,000 – $800,000 MXN anuales.',
    40, y
  );
  y += 22;

  // DIFERENCIAL MESAN
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(0, 229, 255);
  doc.text('DIFERENCIAL MESAN:', 40, y);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(200, 210, 220);
  doc.setCharSpace(1);
  doc.text('No vendemos limpieza.  Vendemos CONTINUIDAD operativa.', 40, y + 14);
  doc.setCharSpace(0);
  y += 36;

  // FIRMA
  doc.setDrawColor(100, 116, 139);
  doc.setLineWidth(0.4);
  doc.line(40, y, 220, y);

  try {
    const firma = document.getElementById('firma-hidden');
    if (firma && firma.src && firma.src.length > 100) {
      doc.addImage(firma.src, 'PNG', 40, y - 45, 100, 44);
    }
  } catch(e) {}

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(200, 210, 220);
  doc.text('Lic. Manuel Sánchez', 40, y + 13);

  doc.setFontSize(8);
  doc.setTextColor(0, 229, 255);
  doc.text('Dirección General – MESAN SERVICIOS ©', 40, y + 25);

  // AVISO DE PRIVACIDAD
  y += 45;
  doc.setFillColor(10, 18, 35);
  doc.rect(40, y, W - 80, 36, 'F');
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(7);
  doc.setTextColor(100, 116, 139);
  const aviso = doc.splitTextToSize(
    'AVISO DE PRIVACIDAD: Los datos proporcionados en esta propuesta son tratados de forma confidencial por MESAN SERVICIOS conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP). No serán compartidos con terceros sin su consentimiento. Para más información: mesanservicios.com/privacidad',
    W - 100
  );
  doc.text(aviso, 50, y + 10);
  y += 44;

  // FOOTER
  doc.setDrawColor(0, 229, 255);
  doc.setLineWidth(0.3);
  doc.line(40, 755, W - 40, 755);
  doc.setFontSize(7);
  doc.setTextColor(100, 116, 139);
  doc.text('Propuesta válida 30 días · Sujeta a visita técnica · mesanservicios.com', W / 2, 766, { align: 'center' });

  doc.save('Propuesta_MESAN_' + cliente.replace(/\s+/g, '_') + '_' + folio + '.pdf');
}
