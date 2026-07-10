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

function obtenerTicketsGuardados() {
    return JSON.parse(localStorage.getItem("tickets")) || [];
}

function crearNumeroTicket() {
    const total = obtenerTicketsGuardados().length + obtenerTicketsBase().length + 1;
    return `GT-2026-${String(total).padStart(3, "0")}`;
}

function clasePrioridad(prioridad) {
    return `prioridad-${prioridad.toLowerCase()}`;
}

function claseEstado(estado) {
    if (estado === "Cerrado") {
        return "estado-cerrado";
    }

    if (estado === "En proceso") {
        return "estado-proceso";
    }

    return "estado-abierto";
}

function iconoCategoria(categoria) {
    if (categoria === "Administrativa") {
        return "&#128209; Admin";
    }

    if (categoria === "Plataforma virtual") {
        return "&#127760; Virtual";
    }

    if (categoria === "Otro") {
        return "&#10067; Otro";
    }

    return "&#128187; Tecnico";
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

        if (!buscarTicket(valor(numero).toUpperCase())) {
            mostrarMensaje(formulario, "No encontramos un ticket con ese numero.", "error");
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

    const matricula = buscarCampo("matricula");
    const borrador = JSON.parse(localStorage.getItem("ticketBorrador")) || {};
    nombre.value = borrador.nombre || "";
    correo.value = borrador.correo || "";
    if (matricula) {
        matricula.value = borrador.matricula || "";
    }

    const guardarBorrador = () => {
        localStorage.setItem("ticketBorrador", JSON.stringify({
            nombre: valor(nombre),
            correo: valor(correo),
            matricula: matricula ? valor(matricula) : ""
        }));
    };

    nombre.addEventListener("input", guardarBorrador);
    correo.addEventListener("input", guardarBorrador);
    if (matricula) {
        matricula.addEventListener("input", guardarBorrador);
    }

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();
        const correcto = validarNombre() & validarCorreoContacto();

        if (!correcto) {
            mostrarMensaje(formulario, "Complete sus datos para continuar.", "error");
            return;
        }

        guardarBorrador();
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

        const datos = JSON.parse(localStorage.getItem("ticketBorrador")) || {};
        const prioridad = buscarCampo("prioridad");
        const tipo = document.querySelector("input[name='tipo']:checked");
        const ticket = {
            numero: crearNumeroTicket(),
            nombre: datos.nombre || "Usuario externo",
            correo: datos.correo || "sin-correo@correo.com",
            matricula: datos.matricula || "",
            categoria: tipo ? tipo.value : "Soporte tecnico",
            prioridad: prioridad ? prioridad.value : "Media",
            asunto: valor(asunto),
            descripcion: valor(descripcion),
            estado: "Abierto",
            fecha: "ahora"
        };
        const guardados = obtenerTicketsGuardados();
        guardados.unshift(ticket);
        guardarTickets(guardados);
        localStorage.setItem("ultimoTicket", ticket.numero);
        localStorage.setItem("ticketConsultado", ticket.numero);
        localStorage.removeItem("ticketBorrador");
        mostrarMensaje(formulario, "Ticket creado correctamente.", "exito");
        setTimeout(() => {
            window.location.href = "ticket-confirmacion.html";
        }, 600);
    });
}

function buscarTicket(numero) {
    return obtenerTickets().find((ticket) => ticket.numero.toUpperCase() === numero.toUpperCase());
}

function mostrarTicketCreado() {
    const numero = localStorage.getItem("ultimoTicket") || "GT-2026-001";
    const ticket = buscarTicket(numero);

    if (!ticket) {
        return;
    }

    const numeroElemento = document.querySelector(".ticket-numero-card strong");
    const datos = document.querySelectorAll(".resumen-confirmacion article strong");

    if (numeroElemento) {
        numeroElemento.innerHTML = ticket.numero;
    }

    if (datos.length >= 3) {
        datos[0].innerHTML = ticket.categoria;
        datos[1].innerHTML = ticket.prioridad;
        datos[1].className = `prioridad-badge ${clasePrioridad(ticket.prioridad)}`;
        datos[2].innerHTML = ticket.estado;
        datos[2].className = claseEstado(ticket.estado);
    }

    iniciarCopiadoTicket(ticket.numero);
}

function mostrarEstadoTicket() {
    const numero = localStorage.getItem("ticketConsultado") || localStorage.getItem("ultimoTicket") || "GT-2026-001";
    const ticket = buscarTicket(numero);
    const seccion = document.querySelector(".ticket-form");

    if (!ticket || !seccion) {
        return;
    }

    const numeroElemento = seccion.querySelector(".ticket-numero-card strong");
    const datos = seccion.querySelectorAll(".resumen-confirmacion article strong");

    if (numeroElemento) {
        numeroElemento.innerHTML = ticket.numero;
    }

    if (datos.length >= 3) {
        datos[0].innerHTML = ticket.categoria;
        datos[1].innerHTML = ticket.prioridad;
        datos[1].className = `prioridad-badge ${clasePrioridad(ticket.prioridad)}`;
        datos[2].innerHTML = ticket.estado;
        datos[2].className = claseEstado(ticket.estado);
    }

    iniciarCopiadoTicket(ticket.numero);
}

function iniciarCopiadoTicket(numero) {
    const boton = document.querySelector(".copiar-boton");

    if (!boton) {
        return;
    }

    boton.addEventListener("click", () => {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(numero);
        }
        boton.innerHTML = "Copiado";
        boton.classList.add("copiado");
    });
}

function plantillaTicket(ticket) {
    return `
        <li>
            <span class="tabla-id">${ticket.numero}</span>
            <div class="tabla-asunto">
                <strong>${ticket.asunto}</strong>
                <small>${ticket.categoria} - ${ticket.fecha}</small>
            </div>
            <span class="cat-badge">${iconoCategoria(ticket.categoria)}</span>
            <span class="prioridad-badge ${clasePrioridad(ticket.prioridad)}">${ticket.prioridad}</span>
            <span class="estado-badge ${claseEstado(ticket.estado)}">${ticket.estado}</span>
            <a class="boton-ver" href="estado-ticket.html" data-ticket="${ticket.numero}">Ver</a>
        </li>
    `;
}

function mostrarListadoTickets() {
    const lista = document.querySelector(".tickets-tabla");
    const buscador = document.querySelector(".busqueda-bar input");
    const prioridad = document.querySelector(".busqueda-bar select");
    const chips = document.querySelectorAll(".chip");
    const contador = document.querySelector(".panel-titulo span");

    if (!lista) {
        return;
    }

    let estadoActual = "Todos";

    const pintar = () => {
        const texto = buscador ? valor(buscador).toLowerCase() : "";
        const prioridadActual = prioridad ? prioridad.value : "Cualquier prioridad";
        const filtrados = obtenerTickets().filter((ticket) => {
            const coincideTexto = ticket.numero.toLowerCase().includes(texto) || ticket.asunto.toLowerCase().includes(texto) || ticket.nombre.toLowerCase().includes(texto);
            const coincideEstado = estadoActual === "Todos" || ticket.estado === estadoActual;
            const coincidePrioridad = prioridadActual === "Cualquier prioridad" || ticket.prioridad === prioridadActual;
            return coincideTexto && coincideEstado && coincidePrioridad;
        });

        lista.innerHTML = filtrados.map(plantillaTicket).join("");
        if (contador) {
            contador.innerHTML = `${filtrados.length} resultados`;
        }

        lista.querySelectorAll(".boton-ver").forEach((boton) => {
            boton.addEventListener("click", () => {
                localStorage.setItem("ticketConsultado", boton.dataset.ticket);
            });
        });
    };

    if (buscador) {
        buscador.addEventListener("input", pintar);
    }

    if (prioridad) {
        prioridad.addEventListener("change", pintar);
    }

    chips.forEach((chip) => {
        chip.addEventListener("click", () => {
            chips.forEach((item) => item.classList.remove("activo"));
            chip.classList.add("activo");
            const texto = chip.innerHTML.trim();
            estadoActual = texto === "Abiertos" ? "Abierto" : texto === "Cerrados" ? "Cerrado" : texto;
            pintar();
        });
    });

    pintar();
}

function mostrarResumenPanel() {
    const tickets = obtenerTickets();
    const numeros = document.querySelectorAll(".stat-numero");
    const lista = document.querySelector(".panel .tickets-tabla");
    const abiertos = tickets.filter((ticket) => ticket.estado === "Abierto").length;
    const proceso = tickets.filter((ticket) => ticket.estado === "En proceso").length;
    const cerrados = tickets.filter((ticket) => ticket.estado === "Cerrado").length;

    if (numeros.length >= 4) {
        numeros[0].innerHTML = abiertos;
        numeros[1].innerHTML = proceso;
        numeros[2].innerHTML = cerrados;
        numeros[3].innerHTML = "2.4h";
    }

    if (lista) {
        lista.innerHTML = tickets.slice(0, 3).map((ticket) => `
            <li>
                <span class="tabla-id">${ticket.numero}</span>
                <div class="tabla-asunto">
                    <strong>${ticket.asunto}</strong>
                    <small>${ticket.categoria} - ${ticket.fecha}</small>
                </div>
                <span class="cat-badge">${iconoCategoria(ticket.categoria)}</span>
                <span class="prioridad-badge ${clasePrioridad(ticket.prioridad)}">${ticket.prioridad}</span>
                <a class="boton-ver" href="estado-ticket.html" data-ticket="${ticket.numero}">Ver</a>
            </li>
        `).join("");

        lista.querySelectorAll(".boton-ver").forEach((boton) => {
            boton.addEventListener("click", () => {
                localStorage.setItem("ticketConsultado", boton.dataset.ticket);
            });
        });
    }
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
