
$(document).ready(function() {
    
    $('#valVacina').mask('000.000,00', { reverse: true });
    $('#valConsulta').mask('000.000,00', { reverse: true });
    $('#edit-valor').mask('000.000,00', { reverse: true });
});

function ValidarFormulario(tipo) {

    if(tipo == "vacina")
    {
        const desc = document.getElementById("descVacina").value;
        const val = document.getElementById("valVacina").value;
    
        if (!desc) {
            alert("Erro: O campo 'Nome' não pode estar vazio.");
            return false; 
        }
        
        if (!val) {
            alert("Erro: O campo 'Valor' não pode estar vazio.");
            return false;  
        }
        return true;
    }
    else if(tipo == "consulta")
    {
        const desc = document.getElementById("descConsulta").value;
        const val = document.getElementById("valConsulta").value;
    
        if (!desc) {
            alert("Erro: O campo 'Nome' não pode estar vazio.");
            return false; 
        }
        
        if (!val) {
            alert("Erro: O campo 'Valor' não pode estar vazio.");
            return false; 
        }
        return true;
    }
    else if (tipo == "editar")
    {
        const desc = document.getElementById("edit-desc").value;
        const val = document.getElementById("edit-valor").value;

        if (!desc) {
            alert("Erro: O campo 'Descricão' não pode estar vazio.");
            return false; 
        }
        
        if (!val) {
            alert("Erro: O campo 'Valor' não pode estar vazio.");
            return false;  
        }
        return true;
    }
}

function mostrarEdit(id, descricao, preco, tipo) {

    document.getElementById('edit-id').value = id;
    document.getElementById('edit-desc').value = descricao;
    document.getElementById('edit-valor').value = preco;
    document.getElementById('edit-tipo').value = tipo;

    document.getElementById('edit-form').style.display = 'block';
}

function openPopup() {
    document.getElementById('popupOverlay').style.display = 'flex';
}

function closePopup() {
    document.getElementById('popupOverlay').style.display = 'none';
}

document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', openPopup);
});