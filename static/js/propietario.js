document.addEventListener('DOMContentLoaded', function() {

    const selectElement = document.getElementById('id_candidato_registro');
    candidato = selectElement.value;
    
    
    setTimeout(function(){
    const selectElement = document.querySelector('#informaciongeneral-group > fieldset > .add-row > a');
    selectElement.addEventListener('click', function(event) {
        propietario(candidato);
    });

    // var addRow = selectElement.getElementsByClassName('.add-row');
    
}, 1500);
    // var a = addRow.getElementsByTagName('a');
    // console.log(addRow.length);
    
    selectElement.addEventListener('change', function() {
        const selectedValue = this.value;
        console.log('Valor seleccionado:', selectedValue);
        propietario(selectedValue);

    });

    function propietario (id) {
        fetch(`/api/propietario/${id}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('No se pudo obtener el registro');
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos:', data);
                // Comprobaciones antes de asignar valores
                if (!document.getElementById('id_informaciongeneral-0-propietario').value) {
                    document.getElementById('id_informaciongeneral-0-propietario').value = data.propietario_nombre_apellido;
                }
                if (!document.getElementById('id_informaciongeneral-0-propietario_telf').value) {
                    document.getElementById('id_informaciongeneral-0-propietario_telf').value = data.propietario_telf;
                }
                if (!document.getElementById('id_informaciongeneral-0-propietario_direccion').value) {
                    document.getElementById('id_informaciongeneral-0-propietario_direccion').value = data.propietario_direccion;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Limpiar los campos solo si la petición falla y los campos están vacíos
                if (!document.getElementById('id_informaciongeneral-0-propietario').value) {
                    document.getElementById('id_informaciongeneral-0-propietario').value = "";
                }
                if (!document.getElementById('id_informaciongeneral-0-propietario_telf').value) {
                    document.getElementById('id_informaciongeneral-0-propietario_telf').value = "";
                }
                if (!document.getElementById('id_informaciongeneral-0-propietario_direccion').value) {
                    document.getElementById('id_informaciongeneral-0-propietario_direccion').value = "";
                }
            });
    }
});