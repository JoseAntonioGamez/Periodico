// Script para prueba y ejemplo funcional en todas las páginas

window.addEventListener('DOMContentLoaded', function() {
    console.log('El archivo JS se ha cargado correctamente');
    // Ejemplo: destacar el enlace activo si corresponde
    let links = document.querySelectorAll('nav ul li a');
    let current = window.location.pathname;
    links.forEach(link => {
        if (link.href.includes(current) && current !== "/") {
            link.style.background = '#0074d9';
        }
    });
});
