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

function buscarCampo(id) {
    return document.getElementById(id);
}

function obtenerGrupo(campo) {
    return campo.closest(".campo") || campo.closest(".busqueda-form") || campo.parentElement;
}

function obtenerError(campo) {
    const grupo = obtenerGrupo(campo);
    let error = grupo.querySelector(".error-campo");
    if (!error) {
        error = document.createElement("small");
        error.className = "error-campo";
        grupo.appendChild(error);
    }
    return error;
}

function marcarCampo(campo, mensaje) {
    const grupo = obtenerGrupo(campo);
    const error = obtenerError(campo);
    grupo.classList.remove("campo-ok", "campo-error");

    if (mensaje) {
        error.innerHTML = mensaje;
        grupo.classList.add("campo-error");
        return false;
    }

    error.innerHTML = "";
    grupo.classList.add("campo-ok");
    return true;
}

function valor(campo) {
    return campo.value.trim();
}

function correoValido(correo) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);
}

function validarTexto(campo, minimo, nombre) {
    if (!valor(campo)) {
        return marcarCampo(campo, `${nombre} es obligatorio.`);
    }

    if (valor(campo).length < minimo) {
        return marcarCampo(campo, `${nombre} debe tener al menos ${minimo} caracteres.`);
    }

    return marcarCampo(campo, "");
}

function validarCorreo(campo) {
    if (!valor(campo)) {
        return marcarCampo(campo, "El correo es obligatorio.");
    }

    if (!correoValido(valor(campo))) {
        return marcarCampo(campo, "Escriba un correo valido.");
    }

    return marcarCampo(campo, "");
}

function validarTicket(campo) {
    if (!valor(campo)) {
        return marcarCampo(campo, "El numero de ticket es obligatorio.");
    }

    if (!/^GT-\d{4}-\d{3}$/i.test(valor(campo))) {
        return marcarCampo(campo, "Use el formato GT-2026-001.");
    }

    return marcarCampo(campo, "");
}

function escucharCampo(campo, validar) {
    campo.addEventListener("input", validar);
    campo.addEventListener("blur", validar);
}

function iniciarLogin() {
    const formulario = document.querySelector(".ticket-form");
    const usuario = buscarCampo("usuario");
    const clave = buscarCampo("clave");

    if (!formulario || !usuario || !clave) {
        return;
    }

    const validarUsuario = () => validarTexto(usuario, 3, "El usuario");
    const validarClave = () => validarTexto(clave, 4, "La contrasena");

    escucharCampo(usuario, validarUsuario);
    escucharCampo(clave, validarClave);

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();
        const correcto = validarUsuario() & validarClave();

        if (!correcto) {
            mostrarMensaje(formulario, "Revise los campos marcados antes de continuar.", "error");
            return;
        }

        localStorage.setItem("usuarioActivo", valor(usuario));
        mostrarMensaje(formulario, "Acceso correcto. Redirigiendo al panel...", "exito");
        setTimeout(() => {
            window.location.href = "panel.html";
        }, 600);
    });
}

function iniciarBusquedaInicio() {
    const formulario = document.querySelector(".busqueda-form");
    const numero = buscarCampo("numero-ticket");

    if (!formulario || !numero) {
        return;
    }

    const validarNumero = () => validarTicket(numero);
    escucharCampo(numero, validarNumero);

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();

        if (!validarNumero()) {
            mostrarMensaje(formulario, "Ingrese un numero de ticket valido para buscar.", "error");
            return;
        }

        localStorage.setItem("ticketConsultado", valor(numero).toUpperCase());
        mostrarMensaje(formulario, "Ticket encontrado. Mostrando estado...", "exito");
        setTimeout(() => {
            window.location.href = "estado-ticket.html";
        }, 600);
    });
}

function iniciarDatosTicket() {
    const formulario = document.querySelector(".ticket-form");
    const nombre = buscarCampo("nombre");
    const correo = buscarCampo("correo");

    if (!formulario || !nombre || !correo) {
        return;
    }

    const validarNombre = () => validarTexto(nombre, 3, "El nombre");
    const validarCorreoContacto = () => validarCorreo(correo);

    escucharCampo(nombre, validarNombre);
    escucharCampo(correo, validarCorreoContacto);

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();
        const correcto = validarNombre() & validarCorreoContacto();

        if (!correcto) {
            mostrarMensaje(formulario, "Complete sus datos para continuar.", "error");
            return;
        }

        mostrarMensaje(formulario, "Datos correctos. Puede continuar con el detalle.", "exito");
        setTimeout(() => {
            window.location.href = "ticket-detalle.html";
        }, 600);
    });
}

function iniciarDetalleTicket() {
    const formulario = document.querySelector(".ticket-form");
    const asunto = buscarCampo("asunto");
    const descripcion = buscarCampo("descripcion");

    if (!formulario || !asunto || !descripcion) {
        return;
    }

    const validarAsunto = () => validarTexto(asunto, 5, "El asunto");
    const validarDescripcion = () => validarTexto(descripcion, 15, "La descripcion");

    escucharCampo(asunto, validarAsunto);
    escucharCampo(descripcion, validarDescripcion);

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();
        const correcto = validarAsunto() & validarDescripcion();

        if (!correcto) {
            mostrarMensaje(formulario, "Revise el detalle del caso antes de crear el ticket.", "error");
            return;
        }

        mostrarMensaje(formulario, "Ticket validado correctamente.", "exito");
        setTimeout(() => {
            window.location.href = "ticket-confirmacion.html";
        }, 600);
    });
}

function mostrarTicketCreado() {}

function mostrarEstadoTicket() {}

function mostrarListadoTickets() {}

function mostrarResumenPanel() {}

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
