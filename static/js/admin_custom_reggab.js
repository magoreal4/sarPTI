var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;


document.addEventListener('DOMContentLoaded', function() {
  // Casmbia el titulo de la pagina Registro Campo
  var h1Element = document.querySelector('#content > h1');
  
  var sitioIDDiv = document.querySelector('.field-sitio_ID .readonly');

  var CellID = sitioIDDiv.textContent.trim();
  
  var candidato = document.getElementById('id_candidato_letra').value
  

   if (h1Element) {
    h1Element.innerHTML = "REGISTRO DE GABINETE<br>" + CellID + ' Candidato ' + candidato;
    
    }

    // Coloca las imagenes en dos columnas
    // Encuentra el contenedor principal donde están todos los elementos
    var mainContainer = document.querySelector('#imagenes_set-group .module');

    // Crea un nuevo div que actuará como el contenedor de la grid
    var gridContainer = document.createElement('div');
      gridContainer.className = 'imagenes-grid';
      gridContainer.style.display = 'grid';
      gridContainer.style.gridTemplateColumns = 'repeat(2, 1fr)'; // Dos columnas de igual ancho
      
      gridContainer.style.width = '100%'; // Ajusta el ancho del contenedor al 100%
    

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
  