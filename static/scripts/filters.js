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

  // Inicialización: enlazar eventos y establecer estado inicial en todos los formularios de filtros
  function init() {
    const forms = document.querySelectorAll('.filters-form');
    if (!forms || forms.length === 0) return;

    // Obtener valor actual de 'activa' desde la URL para inicializar switches
    const params = new URLSearchParams(window.location.search);
    const currentActiva = params.get('activa');

    forms.forEach(function (form) {
      // Helper para submit del formulario (preserva comportamiento por defecto de GET)
      function submitForm() {
        form.submit();
      }

      // Selects que realizan submit al cambiar
      const categoriaSelect = form.querySelector('select[name="categoria"]');
      const ubicacionSelect = form.querySelector('select[name="ubicacion"]');
      if (categoriaSelect) categoriaSelect.addEventListener('change', submitForm);
      if (ubicacionSelect) ubicacionSelect.addEventListener('change', submitForm);

      // Inputs de fecha que hacen submit al cambiar
      form.querySelectorAll('input[type="date"]').forEach(function (el) {
        el.addEventListener('change', submitForm);
      });

      // Switch de 'activa' junto a input oculto que contiene el valor enviado
      const switchActiva = form.querySelector('.form-check-input');
      const activaInput = form.querySelector('input[name="activa"]');
      if (switchActiva && activaInput) {
        // Inicializar el estado del switch según query param
        if (currentActiva === 'true') {
          switchActiva.checked = true;
          activaInput.value = 'true';
        } else if (currentActiva === 'false') {
          switchActiva.checked = false;
          activaInput.value = 'false';
        } else {
          switchActiva.checked = false;
          activaInput.value = '';
        }

        // Cambios en el switch actualizan el input y envían el formulario
        switchActiva.addEventListener('change', function () {
          if (this.checked) activaInput.value = 'true';
          else activaInput.value = '';
          submitForm();
        });
      }
    });

    // Opcional: links con data-param (si existieran) para navegación rápida
    document.querySelectorAll('[data-param]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const p = link.getAttribute('data-param');
        const v = link.getAttribute('data-value');
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
