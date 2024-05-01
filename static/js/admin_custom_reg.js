var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

document.addEventListener('DOMContentLoaded', function() {
  // Casmbia el titulo de la pagina Registro Campo
  var h1Element = document.querySelector('#content > h1');
  
  var sitioIDDiv = document.querySelector('.field-sitio_ID > .readonly');
  var CellID = sitioIDDiv.textContent.trim();
  
  var sitioNombreDiv = document.querySelector('.field-sitio_nombre > .readonly');
  var nombre = sitioNombreDiv.textContent.trim();
  

   if (h1Element) {
    h1Element.innerHTML = "REGISTRO DE CAMPO<br>" + CellID + '  ' + nombre;


    }


 

    // Coloca las imagenes en dos columnas
    // Encuentra el contenedor principal donde están todos los elementos
    var mainContainer = document.querySelector('#registrositioimagenes_set-group .module');

    // Crea un nuevo div que actuará como el contenedor de la grid
    var gridContainer = document.createElement('div');
    gridContainer.className = 'imagenes-grid';
        // Aplica estilo CSS Grid al contenedor
        gridContainer.style.display = 'grid';
        gridContainer.style.gridTemplateColumns = '1fr 1fr'; // Dos columnas de igual ancho
        gridContainer.style.gridGap = '10px'; // Espacio entre columnas y filas
        gridContainer.style.padding = '10px'; // Padding alrededor del contenido interno del grid
    
    // Encuentra todos los elementos que necesitas agrupar
    var contenedores = mainContainer.querySelectorAll('div.inline-related.has_original');

    // Mueve cada elemento seleccionado al nuevo contenedor
      Array.from(contenedores).forEach(function(element) {
        gridContainer.appendChild(element);
    });

// Calcula la posición donde insertar el nuevo contenedor
var insertPosition = mainContainer.children[3]; // Esto asume que el índice 3 existe, es decir, hay al menos 4 elementos

if (insertPosition) {
    mainContainer.insertBefore(gridContainer, insertPosition.nextSibling);
} else {
    // Si no hay suficientes elementos, simplemente añade al final
    mainContainer.appendChild(gridContainer);
}
  





  

  });
  