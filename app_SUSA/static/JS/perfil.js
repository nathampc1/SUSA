function clickFILE() {
    document.getElementById('fileInput').click();
}

function editarPerfil() {
    document.getElementById('btnEditar').style.display = 'none';
    document.getElementById('btnCancelar').style.display = 'block';
    document.getElementById('btnSalvar').style.display = 'block';
    document.getElementById('alterar-senha').style.display = 'block';
    document.getElementById('email').disabled = false;
    document.getElementById('telefone').disabled = false;
    document.getElementById('nome').disabled = false;
    document.getElementById('senha').disabled = false;
    document.getElementById('confirmSenha').disabled = false;
    document.getElementById('icone').style.cursor = 'pointer'

    var fotoPerfil = document.getElementById('foto-perfil');
    fotoPerfil.style.cursor = 'default';


    try{
        document.getElementById('crmv').disabled = false;
    }
    catch{
        console.log('Tutor')
    }

    try{
        document.getElementById('nasc').disabled = false;
    }
    catch{
        console.log('Clinica')
    }
}

function desabilitarBtn() {
    
    setTimeout(function() {
        document.getElementById('btnEditar').style.display = 'block';
        document.getElementById('btnCancelar').style.display = 'none';
        document.getElementById('btnSalvar').style.display = 'none';
        document.getElementById('alterar-senha').style.display = 'none';
        document.getElementById('email').disabled = true;
        document.getElementById('telefone').disabled = true;
        document.getElementById('nome').disabled = true;
        document.getElementById('senha').disabled = true;
        document.getElementById('confirmSenha').disabled = true;
        document.getElementById('icone').style.cursor = 'default';

        var fotoPerfil = document.getElementById('foto-perfil');
        fotoPerfil.style.cursor = 'default';

        try{
            document.getElementById('crmv').disabled = true;
        }
        catch{
            console.log('Tutor')
        }

        try{
            document.getElementById('nasc').disabled = true;
        }
        catch{
            console.log('Clinica')
        }

    }, 500);
}

const AlterarSenhaButton = document.getElementById('alterar-senha');
const senha = document.getElementById('senha');
const confirmSenha = document.getElementById('confirmSenha');

AlterarSenhaButton.addEventListener('click', function () {
    console.log('entrou novamente')
    if (senha.type == 'password') {
        senha.type = 'text';
        confirmSenha.type = 'text';

        AlterarSenhaButton.textContent = 'Ocultar'; 
    } else {
        senha.type = 'password';
        confirmSenha.type = 'password';

        AlterarSenhaButton.textContent = 'Mostrar'; 
    }
});

$(document).ready(function () {

    var telefoneMascara = function (val) {

        return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00000';
    };

    var telefoneOptions = {
        onKeyPress: function (val, e, field, options) {
            
            field.mask(telefoneMascara.apply({}, arguments), options);
        }
    };
    $('#telefone').mask(telefoneMascara, telefoneOptions);
});


function validarFormulario(selecionado) {

    if (selecionado == 'tutor') {
        var nome = document.getElementById("nome").value;
        var telefone = document.getElementById("telefone").value;
        var email = document.getElementById("email").value;
        var nasc = document.getElementById("nasc").value;
        var senha = document.getElementById("senha").value;
        var confirmSenha = document.getElementById("confirmSenha").value;

        var erros = [];

        if (!nome) {
            erros.push("O campo Nome é obrigatório.");
        }
        if (!telefone || !/^\(\d{2}\) \d{4,5}-\d{4}$/.test(telefone)) {
            erros.push("O campo Telefone deve estar no formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX.");
        }
        if (!email) {
            erros.push("O campo E-mail é obrigatório.");
        }
        if (!nasc) {
            erros.push("O campo Nascimento é obrigatório.");
        }
    
        if (!senha || !/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(senha)) {
            erros.push("A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.");
        }
        if (senha !== confirmSenha) {
            erros.push("As senhas não coincidem.");
        }

        if (erros.length > 0) {
            var errosDiv = document.getElementById("erros");
            errosDiv.innerHTML = erros.join("<br>");
            return false; 
        }
        return true;
    }
    else if (selecionado == 'clinica') {
        var nome = document.getElementById("nome").value;
        var telefone = document.getElementById("telefone").value;
        var email = document.getElementById("email").value;
        var crmv = document.getElementById("crmv").value;
        var senha = document.getElementById("senha").value;
        var confirmSenha = document.getElementById("confirmSenha").value;

        var erros = [];

        if (!nome) {
            erros.push("O campo Nome da Clínica é obrigatório.");
        }
        if (!telefone || !/^\(\d{2}\) \d{4,5}-\d{4}$/.test(telefone)) {
            erros.push("O campo Telefone deve estar no formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX.");
        }
        if (!email) {
            erros.push("O campo E-mail é obrigatório.");
        }

        if (!senha || !/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(senha)) {
            erros.push("A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.");
        }
        if (!crmv) {
            erros.push("O campo CRMV é obrigatório.");
        }
        if (senha !== confirmSenha) {
            erros.push("As senhas não coincidem.");
        }

        if (erros.length > 0) {
            var errosDiv = document.getElementById("erros");
            errosDiv.innerHTML = erros.join("<br>");
            return false; 
        }
        return true;
    }
}