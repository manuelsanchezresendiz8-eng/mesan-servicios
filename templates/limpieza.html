// ======================================================
// MESAN SERVICIOS — COTIZADOR LIMPIEZA
// ======================================================

const SERVICIOS = {

    postmudanza: {
        nombre: "Post-Construcción",
        unidad: "m²",
        rendimiento: 120
    },

    techclean: {
        nombre: "Tech-Clean",
        unidad: "equipos",
        rendimiento: 25
    },

    outdoor: {
        nombre: "Outdoor Refresh",
        unidad: "m²",
        rendimiento: 100
    }

};

// ======================================================
// ESTADO
// ======================================================

let servicioActual = null;

// ======================================================
// ABRIR
// ======================================================

function abrirCotLimp(servicio){

    servicioActual = servicio;

    const cantidad = prompt("Ingrese cantidad de servicio:");

    if(!cantidad) return;

    const conInsumos = confirm(
        "¿La cotización incluye insumos?"
    );

    calcularCotizacion(
        servicio,
        parseInt(cantidad),
        conInsumos
    );

}

// ======================================================
// CALCULO
// ======================================================

function calcularCotizacion(
    servicio,
    cantidad,
    conInsumos
){

    const srv = SERVICIOS[servicio];

    // COSTOS BASE REALES

    let costoBase = 0;

    if(servicio === "postmudanza"){
        costoBase = cantidad * 38;
    }

    if(servicio === "techclean"){
        costoBase = cantidad * 120;
    }

    if(servicio === "outdoor"){
        costoBase = cantidad * 42;
    }

    // INSUMOS

    let insumos = 0;

    if(conInsumos){
        insumos = costoBase * 0.18;
    }

    // IVA

    const subtotal = costoBase + insumos;
    const iva = subtotal * 0.16;
    const total = subtotal + iva;

    mostrarResultado({
        servicio: srv.nombre,
        cantidad,
        unidad: srv.unidad,
        costoBase,
        insumos,
        total,
        conInsumos
    });

}

// ======================================================
// RESULTADO
// ======================================================

function mostrarResultado(data){

    const mensaje = `

MESAN SERVICIOS

Servicio:
${data.servicio}

Cantidad:
${data.cantidad} ${data.unidad}

Servicio base:
$${Math.round(data.costoBase).toLocaleString("es-MX")} MXN

Insumos:
${data.conInsumos ? "INCLUIDOS" : "NO INCLUIDOS"}

Costo insumos:
$${Math.round(data.insumos).toLocaleString("es-MX")} MXN

TOTAL:
$${Math.round(data.total).toLocaleString("es-MX")} MXN

`;

    alert(mensaje);

    guardarLead(data);

}

// ======================================================
// GUARDAR LEAD
// ======================================================

async function guardarLead(data){

    const nombre = prompt(
        "Nombre de la empresa:"
    );

    if(!nombre) return;

    await fetch("/leads", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            nombre: nombre,

            servicio: data.servicio,

            total_estimado: data.total,

            fecha: new Date().toLocaleDateString(),

            estado: "nuevo"

        })

    });

    generarPDF(data, nombre);

}

// ======================================================
// PDF
// ======================================================

function generarPDF(data, cliente){

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    // FONDO

    doc.setFillColor(2,6,23);
    doc.rect(0,0,220,300,"F");

    // HEADER

    doc.setFontSize(24);
    doc.setTextColor(0,229,255);
    doc.text("MESAN SERVICIOS", 105, 25, {
        align: "center"
    });

    doc.setFontSize(12);
    doc.setTextColor(255,255,255);

    doc.text(
        "PROPUESTA OPERATIVA",
        105,
        35,
        { align:"center" }
    );

    // CLIENTE

    doc.setFontSize(11);

    doc.text(
        `Cliente: ${cliente}`,
        20,
        60
    );

    doc.text(
        `Servicio: ${data.servicio}`,
        20,
        72
    );

    doc.text(
        `Cantidad: ${data.cantidad} ${data.unidad}`,
        20,
        84
    );

    // BOX

    doc.setFillColor(15,23,42);
    doc.roundedRect(
        20,
        100,
