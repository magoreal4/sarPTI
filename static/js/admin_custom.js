document.addEventListener('DOMContentLoaded', function() {
    // Configuración de un retraso para asegurar que se ejecuta después de que todo esté completamente renderizado
    setTimeout(function() {
      // Seleccionar el elemento con clase 'title active' que contiene la palabra 'Registros'
      const titleElement = document.querySelector('div.title.active[href="/admin/registros/"]');
  
      // Verificar que el elemento existe y modificar su contenido
      if (titleElement) {
        // Usando innerHTML para preservar el contenido HTML interno como íconos, si los hay
        titleElement.innerHTML = titleElement.innerHTML.replace('Registros', 'Archivos');
        console.log('Texto cambiado a:', titleElement.textContent.trim());
      } else {
        console.log('Elemento con la palabra "Registros" no encontrado.');
      }
    }, 2000); // Retraso de 2 segundos
  });
  