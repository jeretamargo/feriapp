// filters.js
// Gestiona filtros dinámicos en la página de lista de ferias.
// - Convierte selects/fechas en auto-submit
// - Controla el switch `activa` mediante un input oculto
// - Actualiza la query string de forma sencilla

(function () {
  'use strict';

  // Navega a la URL con los parámetros proporcionados en 'params' (URLSearchParams)
  function navigateWithParams(params) {
    const url = new URL(window.location.href);
    url.search = params.toString();
    window.location.href = url.pathname + (url.search ? '?' + url.search.slice(1) : '');
  }

  // Establece/borra un parámetro y navega
  function setParam(name, value) {
    const params = new URLSearchParams(window.location.search);
    if (value === null) {
      params.delete(name);
    } else {
      params.set(name, value);
    }
    navigateWithParams(params);
  }

  // Inicialización: enlazar eventos y establecer estado inicial
  function init() {
    const form = document.getElementById('filters-form');
    if (!form) return;

    // Helper para submit del formulario (preserva comportamiento por defecto de GET)
    function submitForm() {
      form.submit();
    }

    // Selects que realizan submit al cambiar
    const categoriaSelect = document.getElementById('categoria-select');
    const ubicacionSelect = document.getElementById('ubicacion-select');
    if (categoriaSelect) categoriaSelect.addEventListener('change', submitForm);
    if (ubicacionSelect) ubicacionSelect.addEventListener('change', submitForm);

    // Inputs de fecha que hacen submit al cambiar
    document.querySelectorAll('#filters-form input[type="date"]').forEach(function (el) {
      el.addEventListener('change', submitForm);
    });

    // Switch de 'activa' junto a input oculto que contiene el valor enviado
    const switchActiva = document.getElementById('switchActiva');
    const activaInput = document.getElementById('activa-input');
    if (switchActiva && activaInput) {
      const params = new URLSearchParams(window.location.search);
      const current = params.get('activa');

      // Por especificación: por defecto mostrar todas (switch OFF)
      // Switch marcado sólo cuando `activa=true` en la URL.
      if (current === 'true') {
        switchActiva.checked = true;
        activaInput.value = 'true';
      } else if (current === 'false') {
        switchActiva.checked = false;
        activaInput.value = 'false';
      } else {
        switchActiva.checked = false;
        activaInput.value = ''; // vacío = mostrar todas
      }

      // Cambios en el switch actualizan el input y envían el formulario
      switchActiva.addEventListener('change', function () {
        if (this.checked) activaInput.value = 'true';
        else activaInput.value = '';
        submitForm();
      });
    }

    // Opcional: links con data-param (si existieran) para navegación rápida
    document.querySelectorAll('[data-param]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const p = link.getAttribute('data-param');
        const v = link.getAttribute('data-value');
        // v puede estar vacío para indicar 'todas'
        setParam(p, v === '' ? '' : v);
      });
    });
  }

  // Ejecutar al cargar DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
