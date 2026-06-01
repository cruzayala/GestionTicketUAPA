const pagina = document.body.dataset.page;

function obtenerTicketsBase() {
    return [
        {
            numero: "GT-2026-001",
            nombre: "Carlos Mejia",
            correo: "carlos@correo.com",
            categoria: "Soporte tecnico",
            prioridad: "Alta",
            asunto: "Problema con acceso al portal",
            descripcion: "No puedo entrar al portal academico.",
            estado: "Abierto",
            fecha: "hace 2h"
        },
        {
            numero: "GT-2026-002",
            nombre: "Ana Perez",
            correo: "ana@correo.com",
            categoria: "Administrativa",
            prioridad: "Media",
            asunto: "Solicitud de equipo nuevo",
            descripcion: "Solicitud para validar equipo de trabajo.",
            estado: "En proceso",
            fecha: "hace 5h"
        },
        {
            numero: "GT-2026-003",
            nombre: "Luis Ramos",
            correo: "luis@correo.com",
            categoria: "Plataforma virtual",
            prioridad: "Baja",
            asunto: "Consulta sobre plataforma virtual",
            descripcion: "Consulta sobre acceso a materiales.",
            estado: "En proceso",
            fecha: "ayer"
        }
    ];
}

function obtenerTickets() {
    const guardados = JSON.parse(localStorage.getItem("tickets")) || [];
    return [...guardados, ...obtenerTicketsBase()];
}

function guardarTickets(tickets) {
    localStorage.setItem("tickets", JSON.stringify(tickets));
}

function crearMensaje(formulario) {
    let mensaje = formulario.querySelector(".mensaje-form");
    if (!mensaje) {
        mensaje = document.createElement("div");
        mensaje.className = "mensaje-form";
        formulario.insertBefore(mensaje, formulario.firstElementChild.nextElementSibling);
    }
    return mensaje;
}

function mostrarMensaje(formulario, texto, tipo) {
    const mensaje = crearMensaje(formulario);
    mensaje.innerHTML = texto;
    mensaje.classList.remove("mensaje-error", "mensaje-exito");
    mensaje.classList.add(tipo === "exito" ? "mensaje-exito" : "mensaje-error");
}

function iniciarAplicacion() {
    if (pagina === "login") {
        iniciarLogin();
    }

    if (pagina === "inicio") {
        iniciarBusquedaInicio();
    }

    if (pagina === "crear-ticket") {
        iniciarDatosTicket();
    }

    if (pagina === "ticket-detalle") {
        iniciarDetalleTicket();
    }

    if (pagina === "ticket-confirmacion") {
        mostrarTicketCreado();
    }

    if (pagina === "estado-ticket") {
        mostrarEstadoTicket();
    }

    if (pagina === "tickets") {
        mostrarListadoTickets();
    }

    if (pagina === "panel") {
        mostrarResumenPanel();
    }
}

document.addEventListener("DOMContentLoaded", iniciarAplicacion);
