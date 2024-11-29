function openPopup() {
    document.getElementById("popupForm").style.display = "flex";
}

function closePopup() {
    document.getElementById("popupForm").style.display = "none";
}

function ValidarFormulario() {
    
    var nome = document.getElementById("nome").value;
    var nascimento = document.getElementById("nascimento").value;
    var sexo = document.getElementById("sexo").value;
    var peso = document.getElementById("peso").value;
    var idade = document.getElementById("idade").value;
    var raca = document.getElementById("raca").value;
    
    var erros = [];

    
    if (!nome) erros.push("O campo Nome é obrigatório.");
    if (!nascimento) erros.push("O campo Data de Nascimento é obrigatório.");
    if (!sexo) erros.push("O campo Sexo é obrigatório.");
    if (!idade) erros.push("O campo Idade é obrigatório.");
    if (!raca) erros.push("O campo Raça é obrigatório.");

    if (erros.length > 0) {
        alert(erros.join("\n"));
        return false; 
    }
    return true; 
}
$(document).ready(function () {
    $('#peso').on('focus', function () {
        $(this).mask('##0.00', {reverse: true});
    });
});

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function excluirPet(petId) {
    if (confirm("Tem certeza que deseja excluir este pet?")) {
        fetch(`/excluir_pet/${petId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {

                console.log("Elementos de pet no DOM antes da exclusão:");
                document.querySelectorAll(".pet-item").forEach(item => console.log(item.id));

                const petElement = document.getElementById(`pet-${petId}`);
                if (petElement) {
                    petElement.remove();
                } else {
                    location.reload();
                    console.error(`Elemento com id pet-${petId} não encontrado no DOM.`);
                }
            } else {
                alert("Erro ao excluir o pet: " + data.error);
            }
        })
        .catch(error => {
            console.error("Erro ao excluir o pet:", error);
        });
    }
}


