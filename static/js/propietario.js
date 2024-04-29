document.addEventListener('DOMContentLoaded', function() {
    console.log("Hola");
    const selectElement = document.getElementById('id_registro_inicio');

    // propietario(selectElement.value);
    
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
                console.log(data); 
                // Comprobaciones antes de asignar valores
                if (!document.getElementById('id_propietario').value) {
                    document.getElementById('id_propietario').value = data.propietario_nombre_apellido;
                }
                if (!document.getElementById('id_propietario_telf').value) {
                    document.getElementById('id_propietario_telf').value = data.propietario_telf;
                }
                if (!document.getElementById('id_propietario_direccion').value) {
                    document.getElementById('id_propietario_direccion').value = data.propietario_direccion;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Limpiar los campos solo si la petición falla y los campos están vacíos
                if (!document.getElementById('id_propietario').value) {
                    document.getElementById('id_propietario').value = "";
                }
                if (!document.getElementById('id_propietario_telf').value) {
                    document.getElementById('id_propietario_telf').value = "";
                }
                if (!document.getElementById('id_propietario_direccion').value) {
                    document.getElementById('id_propietario_direccion').value = "";
                }
            });
    }
});