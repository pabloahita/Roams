/*async function crearCliente(columna){
    return fetch(`/meterFicha/${columna}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify()
    })
    .then(response=>{
        if (!response.ok) {
            return response.text().then(errorMessage => {
                alert(errorMessage);
                throw new Error(errorMessage); // Detiene la ejecución
            });
        }
        return response.json();
    }
        
    )
    .then(data=>{
        if (data) {
            console.log('Datos recibidos:', data);
        }
        return data;
    })
    .catch(error=>{
        alert(error)
        throw error;
    })
}*/