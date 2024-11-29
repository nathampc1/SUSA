function formatarCpfCnpj(campo) {
    let valor = campo.value.replace(/\D/g, ''); 
    let tamanho = valor.length;

    if (tamanho <= 11) { 
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
        valor = valor.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    } else if (tamanho <= 14) { 
        valor = valor.replace(/^(\d{2})(\d)/, '$1.$2');
        valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
        valor = valor.replace(/\.(\d{3})(\d)/, '.$1/$2');
        valor = valor.replace(/(\d{4})(\d{1,2})$/, '$1-$2');
    }

    campo.value = valor; 
}

const AlterarSenhaButton = document.getElementById('alterar-senha');
const senhaInput = document.getElementById('senha-input');

AlterarSenhaButton.addEventListener('click', function() {
    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        AlterarSenhaButton.textContent = 'Ocultar'; 
    } else {
        senhaInput.type = 'password';
        AlterarSenhaButton.textContent = 'Mostrar'; 
    }
});

function validarFormulario() {
    console.log('Iniciando validação do formulário...');

    var cpfCnpj = document.getElementById('cpf_cnpj').value;
    var senha = document.getElementById('senha-input').value;
    var erros = [];
    
    var cpfRegex = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
    var cnpjRegex = /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/;

    if (!cpfCnpj) {
        erros.push("O campo CPF ou CNPJ é obrigatório.");
    } else if (!cpfRegex.test(cpfCnpj) && !cnpjRegex.test(cpfCnpj)) {
        erros.push("CPF ou CNPJ inválido. Use o formato 000.000.000-00 ou 00.000.000/0000-00.");
    }

    var senhaRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!senha) {
        erros.push("O campo senha é obrigatório.");
    } else if (!senhaRegex.test(senha)) {
        erros.push("A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.");
    }

    var mensagemErro = document.getElementById("mensagemErro");
    if (erros.length > 0) { 
        mensagemErro.innerHTML = erros.join("<br>");
        return false; 
    }
    return true; 
}