function RetornoCampos() {
    console.log('Função RetornoCampos chamada'); 
    const statusSelect = document.getElementById('status_animal');
    const camposRetorno = document.querySelector('.campos-retorno');

    if (statusSelect && camposRetorno) {
        if (statusSelect.value === 'Retorno') {
            camposRetorno.style.display = 'block';
        } else {
            camposRetorno.style.display = 'none';
        }
    } else {
        console.error("Elemento não encontrado: verifique os IDs ou classes no HTML");
    }
}

document.querySelector('form').addEventListener('submit', function(event) {
    const novaObservacao = document.querySelector('.nova-observacao');
    const statusSelect = document.getElementById('status_animal');
    const dataRetorno = document.getElementById('data-retorno');
    const horaRetorno = document.getElementById('hora-retorno');
    let valid = true;

    if (!novaObservacao.value.trim()) {
        alert('Por favor, preencha o campo de observação.');
        novaObservacao.focus();
        valid = false;
    }

    if (statusSelect.value === 'Retorno') {
        if (!dataRetorno.value) {
            alert('Por favor, preencha a data de retorno.');
            dataRetorno.focus();
            valid = false;
        } else if (!horaRetorno.value) {
            alert('Por favor, preencha o horário de retorno.');
            horaRetorno.focus();
            valid = false;
        }
    }

    if (!valid) {
        event.preventDefault();
    }
});