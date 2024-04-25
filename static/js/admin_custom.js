document.addEventListener('DOMContentLoaded', function() {
  // Casmbia el titulo de la pagina Registro Campo
  var h1Element = document.querySelector('h1.ui.header');
  var sitioIDDiv = document.querySelector('.field-sitio_ID .readonly');
  var sitioNombreDiv = document.querySelector('.field-sitio_nombre .readonly');

  var CellID = sitioIDDiv.textContent.trim();
  var nombre = sitioNombreDiv.textContent.trim();

   if (h1Element) {
    h1Element.innerText = CellID+'  '+nombre;
    }


  });
  