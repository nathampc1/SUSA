function validarFormulario() {
    
    const servicosSelecionados = document.querySelectorAll('input[type="checkbox"]:checked').length;
    
    const data = document.getElementById('data').value;
    const horario = document.getElementById('horario').value;
    const pet = document.getElementById('filtro-animacao').value
    const obsAgendamento = document.getElementById('obs-agendamento').value.trim();

    
    if (servicosSelecionados === 0) {
        alert("Por favor, selecione pelo menos um serviço.");
        return false; 
    }
    if (!data) {
        alert("Por favor, selecione uma data.");
        return false;
    }
    if (!horario) {
        alert("Por favor, selecione um horário.");
        return false;
    }
    if(pet === ""){
        alert("Por favor, selecione um pet.");
        return false;
    }
    if (!obsAgendamento) {
        alert("Por favor, descreva o ocorrido no campo de observação.");
        return false;
    }
    
    return true;
}