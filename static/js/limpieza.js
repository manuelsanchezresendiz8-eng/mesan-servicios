// =========================================
    // GUARDAR
    // =========================================

    const leadData = {

        nombre: empresa || "CLIENTE",

        servicio: srv.nombre || "SERVICIO",

        total_estimado: Number(total) || 0,

        fecha: new Date().toLocaleDateString(),

        estado: "nuevo"

    };

    guardarLead(leadData);

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
