const API_EVENTS_URL = 'http://localhost:5000/api/events';

const initCalendar = (elementId) => {
    const calendarEl = document.getElementById(elementId);
    if (!calendarEl) {
        console.error(`Error en calendar.js: Elemento con ID '${elementId}' no encontrado. No se puede inicializar el calendario.`);
        return;
    }
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        editable: false,
        dayMaxEvents: true,
        events: (fetchInfo, successCallback, failureCallback) => {
            fetch(API_EVENTS_URL)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Error HTTP! estado: ${response.status} al cargar eventos.`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("calendar.js: Eventos recibidos del API:", data);
                    successCallback(data);
                })
                .catch(error => {
                    console.error('calendar.js: Error al cargar los eventos del calendario:', error);
                    failureCallback(error);
                });
        },
        eventDidMount: function(info) {
            info.el.title = info.event.extendedProps.description || info.event.title;
        },
        eventClick: function(info) {
            const description = info.event.extendedProps.description || 'Sin descripción';
            alert(`Evento: ${info.event.title}\nFecha: ${info.event.start.toLocaleString()}\nDetalles: ${description}`);
        }
    });
    calendar.render();
    console.log("calendar.js: Calendario renderizado para el elemento:", elementId);
};

export { initCalendar as init };