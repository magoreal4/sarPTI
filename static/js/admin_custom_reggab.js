var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;


document.addEventListener('DOMContentLoaded', function() {
  // Casmbia el titulo de la pagina Registro Campo
  var h1Element = document.querySelector('h1.ui.header');
  
  var sitioIDDiv = document.querySelector('.field-sitio_ID .readonly');
  var CellID = sitioIDDiv.textContent.trim();
  
  var candidato = document.getElementById('id_candidato_letra').value
  

   if (h1Element) {
    h1Element.innerText = CellID+'- Candidato '+candidato;
    }


  

  });
  