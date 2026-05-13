// ============================================================
// MESAN SERVICIOS — COTIZADOR + CRM + PDF
// ============================================================

// ─────────────────────────────────────────────
// VARIABLES
// ─────────────────────────────────────────────

const SMG_L = {
    frontera: 440.62,
    interior: 248.93
};

const IVA_L = {
    frontera: 0.08,
    interior: 0.16
};

const MARGENES_L = {
    gobierno: 0.20,
    industrial: 0.28,
    corporativo: 0.35
};

// ─────────────────────────────────────────────
// SERVICIOS
// ─────────────────────────────────────────────

const SERVICIOS_L = {

    postmudanza: {
        label: 'Post-Mudanza / Post-Construcción',
        icono: '🏗️',
        unidad: 'm²',
        default_qty: 150,
        riesgo: 'MEDIO-ALTO'
    },

    techclean: {
        label: 'Tech-Clean — Sanitización Electrónica',
        icono: '💻',
        unidad: 'equipos',
        default_qty: 20,
        riesgo: 'MEDIO'
    },

    outdoor: {
        label: 'Outdoor Refresh — Terrazas y Patios',
        icono: '🌿',
        unidad: 'm²',
        default_qty: 80,
        riesgo: 'MEDIO'
    }

};

// ─────────────────────────────────────────────
// ESTADO
// ─────────────────────────────────────────────

let _srv = null;
let _cot = null;

// ─────────────────────────────────────────────
// FORMATOS
// ─────────────────────────────────────────────

function money(n){

    return '$' + Math.round(n).toLocaleString('es-MX');

}

// ─────────────────────────────────────────────
// MODAL HTML
// ─────────────────────────────────────────────

document.body.insertAdjacentHTML("beforeend", `

<div id="modal-limp" style="
position:fixed;
inset:0;
background:rgba(0,0,0,.9);
display:none;
align-items:center;
justify-content:center;
z-index:9999;
padding:20px;
">

<div style="
background:#08101d;
width:100%;
max-width:520px;
border-radius:18px;
padding:28px;
border:1px solid rgba(0,229,255,.15);
max-height:95vh;
overflow-y:auto;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:20px;
">

<h2 id="lmp-titulo" style="
font-family:'Syne',sans-serif;
color:#00e5ff;
font-size:18px;
">
Cotizador
</h2>

<button onclick="cerrarModalLimp()" style="
background:none;
border:none;
color:white;
font-size:22px;
cursor:pointer;
">
✕
</button>

</div>

<input id="lmp-cliente" type="text" placeholder="Empresa / Cliente"
style="
width:100%;
padding:14px;
margin-bottom:14px;
background:#0f172a;
border:1px solid rgba(255,255,255,.08);
border-radius:10px;
color:white;
">

<input id="lmp-qty" type="number" placeholder="Cantidad"
style="
width:100%;
padding:14px;
margin-bottom:14px;
background:#0f172a;
border:1px solid rgba(255,255,255,.08);
border-radius:10px;
color:white;
">

<select id="lmp-zona"
style="
width:100%;
padding:14px;
margin-bottom:14px;
background:#0f172a;
border:1px solid rgba(255,255,255,.08);
border-radius:10px;
color:white;
">

<option value="frontera">Frontera</option>
<option value="interior">Interior</option>

</select>

<select id="lmp-sector"
style="
width:100%;
padding:14px;
margin-bottom:14px;
background:#0f172a;
border:1px solid rgba(255,255,255,.08);
border-radius:10px;
color:white;
">

<option value="corporativo">Corporativo</option>
<option value="industrial">Industrial</option>
<option value="gobierno">Gobierno</option>

</select>

<select id="lmp-turno"
style="
width:100%;
padding:14px;
margin-bottom:18px;
background:#0f172a;
border:1px solid rgba(255,255,255,.08);
border-radius:10px;
color:white;
">

<option value="1">1 Turno</option>
<option value="2">2 Turnos</option>
<option value="3">3 Turnos</option>

</select>

<div style="
background:#0f172a;
padding:18px;
border-radius:14px;
margin-bottom:20px;
">

<p style="margin-bottom:8px;color:#94a3b8;">
Servicio Base
</p>

<h3 id="lmp-total" style="
font-family:'Syne',sans-serif;
font-size:32px;
color:#00e5ff;
">
$0
</h3>

<p style="
margin-top:10px;
font-size:12px;
color:#94a3b8;
">
Estimación mensual operativa
</p>

</div>

<button onclick="guardarLead()"
style="
width:100%;
padding:15px;
border:none;
border-radius:10px;
background:#00e5ff;
color:black;
font-family:'Syne',sans-serif;
font-weight:800;
cursor:pointer;
margin-bottom:12px;
">
Guardar Lead
</button>

<button onclick="generarPDFLimp()"
style="
width:100%;
padding:15px;
border:none;
border-radius:10px;
background:white;
color:black;
font-family:'Syne',sans-serif;
font-weight:800;
cursor:pointer;
margin-bottom:12px;
">
Descargar PDF
</button>

<a id="wa-btn"
target="_blank"
style="
display:block;
width:100%;
padding:15px;
border-radius:10px;
text-align:center;
background:#25d366;
color:white;
text-decoration:none;
font-family:'Syne',sans-serif;
font-weight:800;
">
WhatsApp
</a>

</div>

</div>

`);

// ─────────────────────────────────────────────
// ABRIR MODAL
// ─────────────────────────────────────────────

function abrirCotLimp(servicio){

    _srv = servicio;

    const s = SERVICIOS_L[servicio];

    document.getElementById("lmp-titulo").innerHTML =
        s.icono + ' ' + s.label;

    document.getElementById("lmp-qty").value =
        s.default_qty;

    document.getElementById("modal-limp").style.display =
        "flex";

    recalcularLimp();
}

// ─────────────────────────────────────────────
// CERRAR
// ─────────────────────────────────────────────

function cerrarModalLimp(){

    document.getElementById("modal-limp").style.display =
        "none";

}

// ─────────────────────────────────────────────
// RECALCULAR
// ─────────────────────────────────────────────

function recalcularLimp(){

    const zona =
        document.getElementById("lmp-zona").value;

    const sector =
        document.getElementById("lmp-sector").value;

    const cantidad =
        parseInt(document.getElementById("lmp-qty").value || 1);

    const turnos =
        parseInt(document.getElementById("lmp-turno").value || 1);

    const smg = SMG_L[zona];
    const iva = IVA_L[zona];
    const margen = MARGENES_L[sector];

    const dias_mes = (6/7)*30;

    const nomina =
        smg * dias_mes * turnos;

    const carga =
        nomina * 0.45;

    const insumos = 1200;

    const costo =
        (nomina + carga + insumos) * cantidad;

    const subtotal =
        costo / (1 - margen);

    const iva_total =
        subtotal * iva;

    const total =
        subtotal + iva_total;

    _cot = {
        total,
        subtotal,
        iva_total,
        cantidad,
        zona,
        sector,
        turnos
    };

    document.getElementById("lmp-total").innerHTML =
        money(total);

    const cliente =
        document.getElementById("lmp-cliente").value || "Cliente";

    const wa =
`https://wa.me/526861629643?text=Hola MESAN Servicios, requiero información sobre una cotización de ${money(total)} para ${cliente}`;

    document.getElementById("wa-btn").href = wa;

}

// ─────────────────────────────────────────────
// EVENTOS
// ─────────────────────────────────────────────

document.addEventListener("input", function(e){

    if(
        e.target.id === "lmp-qty" ||
        e.target.id === "lmp-cliente"
    ){
        recalcularLimp();
    }

});

document.addEventListener("change", function(e){

    if(
        e.target.id === "lmp-zona" ||
        e.target.id === "lmp-sector" ||
        e.target.id === "lmp-turno"
    ){
        recalcularLimp();
    }

});

// ─────────────────────────────────────────────
// GUARDAR LEAD
// ─────────────────────────────────────────────

async function guardarLead(){

    if(!_cot) return;

    const cliente =
        document.getElementById("lmp-cliente").value || "Cliente";

    const lead = {

        nombre: cliente,

        servicio: SERVICIOS_L[_srv].label,

        total_estimado: Math.round(_cot.total),

        estado: "nuevo",

        fecha: new Date().toISOString()

    };

    try{

        const r = await fetch("/leads", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(lead)

        });

        const data = await r.json();

        alert("Lead guardado correctamente");

    }catch(err){

        alert("Error al guardar lead");

    }

}

// ─────────────────────────────────────────────
// PDF
// ─────────────────────────────────────────────

function generarPDFLimp(){

    if(!_cot) return;

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    const cliente =
        document.getElementById("lmp-cliente").value || "CLIENTE";

    doc.setFillColor(2,6,23);
    doc.rect(0,0,220,300,"F");

    doc.setTextColor(0,229,255);
    doc.setFontSize(22);

    doc.text("MESAN SERVICIOS", 105, 25, { align:"center" });

    doc.setTextColor(255,255,255);
    doc.setFontSize(12);

    doc.text("PROPUESTA OPERATIVA", 105, 38, { align:"center" });

    doc.setFontSize(10);

    doc.text("Cliente: " + cliente, 20, 60);

    doc.text(
        "Servicio: " + SERVICIOS_L[_srv].label,
        20,
        72
    );

    doc.text(
        "Zona: " + _cot.zona,
        20,
        84
    );

    doc.text(
        "Sector: " + _cot.sector,
        20,
        96
    );

    doc.setDrawColor(0,229,255);

    doc.line(20,110,190,110);

    doc.setTextColor(0,229,255);
    doc.setFontSize(16);

    doc.text(
        "TOTAL ESTIMADO",
        20,
        132
    );

    doc.setTextColor(255,255,255);
    doc.setFontSize(28);

    doc.text(
        money(_cot.total),
        20,
        150
    );

    doc.setFontSize(10);

    doc.text(
        "Modelo financiero operativo mensual",
        20,
        165
    );

    doc.setTextColor(120,120,120);

    doc.text(
        "MESAN Servicios © 2026",
        20,
        280
    );

    doc.save(
        "Propuesta_MESAN.pdf"
    );

}
