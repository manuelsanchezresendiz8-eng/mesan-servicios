// ======================================================
// MESAN SERVICIOS — LIMPIEZA
// ======================================================

const SERVICIOS = {

    postmudanza: {
        nombre: "Post-Construcción",
        unidad: "m²",
        costo: 38
    },

    techclean: {
        nombre: "Tech-Clean",
        unidad: "equipos",
        costo: 120
    },

    outdoor: {
        nombre: "Outdoor Refresh",
        unidad: "m²",
        costo: 42
    }

};

// ======================================================
// ESTADO
// ======================================================

let servicioActivo = null;

// ======================================================
// ABRIR MODAL
// ======================================================

function abrirCotLimp(servicio){

    servicioActivo = servicio;

    document.getElementById(
        "modal-cotizador"
    ).style.display = "flex";

    document.getElementById(
        "titulo-servicio"
    ).innerText =
        SERVICIOS[servicio].nombre;

}

// ======================================================
// CERRAR
// ======================================================

function cerrarModal(){

    document.getElementById(
        "modal-cotizador"
    ).style.display = "none";

}

// ======================================================
// PROCESAR
// ======================================================

function procesarCotizacion(){

    const empresa =
        document.getElementById("empresa").value;

    const cantidad =
        parseInt(
            document.getElementById("cantidad").value
        );

    const zona =
        document.getElementById("zona").value;

    const insumos =
        document.getElementById("insumos").value;

    if(!empresa){

        alert("Ingrese empresa");

        return;
    }

    const srv =
        SERVICIOS[servicioActivo];

    // =========================================
    // COSTO BASE
    // =========================================

    let subtotal =
        cantidad * srv.costo;

    // =========================================
    // INSUMOS
    // =========================================

    let costoInsumos = 0;

    if(insumos === "si"){

        costoInsumos =
            subtotal * 0.18;
    }

    subtotal += costoInsumos;

    // =========================================
    // IVA
    // =========================================

    const iva =
        zona === "frontera"
        ? subtotal * 0.08
        : subtotal * 0.16;

    const total =
        subtotal + iva;

    // =========================================
    // GUARDAR
    // =========================================

    guardarLead({

        nombre: empresa,

        servicio: srv.nombre,

        total_estimado: total,

        fecha: new Date().toLocaleDateString(),

        estado: "nuevo"

    });

    // =========================================
    // PDF
    // =========================================

    generarPDF({

        empresa,
        servicio: srv.nombre,
        cantidad,
        unidad: srv.unidad,
        subtotal,
        costoInsumos,
        total,
        insumos

    });

}

// ======================================================
// GUARDAR LEAD
// ======================================================

async function guardarLead(data){

    await fetch("/leads", {

        method: "POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify(data)

    });

}

// ======================================================
// PDF PREMIUM
// ======================================================

function generarPDF(data){

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    // =========================================
    // FONDO
    // =========================================

    doc.setFillColor(2,6,23);

    doc.rect(
        0,
        0,
        220,
        300,
        "F"
    );

    // =========================================
    // HEADER
    // =========================================

    doc.setTextColor(0,229,255);

    doc.setFontSize(24);

    doc.text(
        "MESAN SERVICIOS",
        105,
        24,
        { align:"center" }
    );

    doc.setTextColor(255,255,255);

    doc.setFontSize(11);

    doc.text(
        "PROPUESTA OPERATIVA",
        105,
        34,
        { align:"center" }
    );

    // =========================================
    // CLIENTE
    // =========================================

    doc.setFontSize(10);

    doc.text(
        `Cliente: ${data.empresa}`,
        20,
        58
    );

    doc.text(
        `Servicio: ${data.servicio}`,
        20,
        70
    );

    doc.text(
        `Cantidad: ${data.cantidad} ${data.unidad}`,
        20,
        82
    );

    // =========================================
    // CONTEXTO
    // =========================================

    doc.setTextColor(0,229,255);

    doc.text(
        "CONTEXTO OPERATIVO",
        20,
        105
    );

    doc.setTextColor(200,200,200);

    doc.setFontSize(9);

    doc.text(
        "MESAN Servicios proporciona continuidad operativa",
        20,
        118
    );

    doc.text(
        "mediante protocolos de limpieza profesional,",
        20,
        128
    );

    doc.text(
        "supervision y cumplimiento operativo.",
        20,
        138
    );

    // =========================================
    // BOX
    // =========================================

    doc.setFillColor(15,23,42);

    doc.roundedRect(
        20,
        155,
        170,
        60,
        6,
        6,
        "F"
    );

    doc.setTextColor(0,229,255);

    doc.setFontSize(11);

    doc.text(
        "MODELO FINANCIERO",
        30,
        172
    );

    doc.setTextColor(255,255,255);

    doc.setFontSize(10);

    doc.text(
        `Servicio Base: $${Math.round(data.subtotal).toLocaleString("es-MX")}`,
        30,
        188
    );

    doc.text(
        `Insumos: ${data.insumos === "si" ? "INCLUIDOS" : "NO INCLUIDOS"}`,
        30,
        200
    );

    doc.setFontSize(13);

    doc.text(
        `TOTAL: $${Math.round(data.total).toLocaleString("es-MX")} MXN`,
        30,
        214
    );

    // =========================================
    // FOOTER
    // =========================================

    doc.setFontSize(8);

    doc.setTextColor(120,120,120);

    doc.text(
        "MESAN Servicios © 2026",
        105,
        280,
        { align:"center" }
    );

    doc.save(
        `MESAN_${data.empresa}.pdf`
    );

}
