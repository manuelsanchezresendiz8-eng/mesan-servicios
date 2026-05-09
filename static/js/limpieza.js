function generarCotizacionMaster() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const cliente = document.getElementById('cliente').value || "CLIENTE POTENCIAL";
    const aceptoPrivacidad = document.getElementById('accept-privacy').checked;

    if (!aceptoPrivacidad) {
        alert("Por favor, acepte el aviso de privacidad para continuar.");
        return;
    }

    // Estética Realismo Radical (Fondo Negro / Texto Cyan)
    doc.setFillColor(5, 10, 18);
    doc.rect(0, 0, 210, 297, 'F');
    
    doc.setTextColor(34, 211, 238);
    doc.setFontSize(22);
    doc.text("MESAN SERVICIOS", 20, 30);
    
    doc.setFontSize(12);
    doc.setTextColor(148, 163, 184);
    doc.text("Continuidad Operativa Industrial", 20, 38);

    doc.setTextColor(34, 211, 238);
    doc.text("CONTEXTO ESTRATÉGICO", 20, 60);
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(10);
    const texto = "Entendemos que la limpieza industrial no es un gasto, sino un factor crítico de continuidad. La ausencia de control genera riesgos STPS y pérdida de productividad.";
    doc.text(doc.splitTextToSize(texto, 170), 20, 70);

    doc.setTextColor(34, 211, 238);
    doc.text("PROPUESTA PARA:", 20, 100);
    doc.setTextColor(255, 255, 255);
    doc.text(cliente.toUpperCase(), 20, 110);

    doc.setTextColor(34, 211, 238);
    doc.text("DIFERENCIAL MESAN:", 20, 140);
    doc.setTextColor(255, 255, 255);
    doc.text("¡No vendemos limpieza! Vendemos CONTINUIDAD operativa.", 20, 150);

    doc.save(`Propuesta_MESAN_${cliente}.pdf`);
}





 Gerente Regional zona Pacifico
 SERVICIOS MESAN S.A.S
Tel 5548722116 
686 21 7307

Manuel Sanchez <serviciosmesanmexicali@gmail.com>
7:17 p.m. (hace 1 minuto)
para mí

Limpia

function generarCotizacionMaster() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Captura el nombre de la empresa del formulario
    const cliente = document.getElementById('cliente').value || "CLIENTE POTENCIAL";
    const aceptoPrivacidad = document.getElementById('accept-privacy').checked;

    // Validación de seguridad
    if (!aceptoPrivacidad) {
        alert("Por favor, acepte el aviso de privacidad para continuar.");
        return;
    }

    // --- DISEÑO VISUAL ---
    // Fondo oscuro institucional
    doc.setFillColor(5, 10, 18);
    doc.rect(0, 0, 210, 297, 'F');
    
    // Encabezado MESAN Ω
    doc.setTextColor(34, 211, 238);
    doc.setFontSize(22);
    doc.text("MESAN SERVICIOS", 20, 30);
    
    doc.setFontSize(12);
    doc.setTextColor(148, 163, 184);
    doc.text("Continuidad Operativa Industrial", 20, 38);

    // Cuerpo de la Propuesta
    doc.setTextColor(34, 211, 238);
    doc.text("CONTEXTO ESTRATÉGICO", 20, 60);
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(10);
    const texto = "Entendemos que la limpieza industrial no es un gasto, sino un factor crítico de continuidad. La ausencia de control genera riesgos STPS y pérdida de productividad.";
    doc.text(doc.splitTextToSize(texto, 170), 20, 70);

    doc.setTextColor(34, 211, 238);
    doc.text("DIRIGIDO A:", 20, 100);
    doc.setTextColor(255, 255, 255);
    doc.text(cliente.toUpperCase(), 20, 110);

    // Diferencial Estratégico
    doc.setTextColor(34, 211, 238);
    doc.text("DIFERENCIAL MESAN:", 20, 140);
    doc.setTextColor(255, 255, 255);
    doc.text("¡No vendemos limpieza! Vendemos CONTINUIDAD operativa.", 20, 150);

    // Guardar archivo
    doc.save(`Propuesta_MESAN_${cliente}.pdf`);
}
