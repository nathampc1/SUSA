const selectWrappers = document.querySelectorAll('.custom-select-wrapper');

selectWrappers.forEach(function (selectWrapper) {
    const selectTrigger = selectWrapper.querySelector('.custom-select-trigger');
    const customOptions = selectWrapper.querySelector('.custom-options');
    const hiddenSelect = selectWrapper.querySelector('select');

    selectTrigger.addEventListener('click', function () {
        customOptions.classList.toggle('open');
    });

    customOptions.addEventListener('click', function (event) {
        if (event.target.classList.contains('custom-option')) {
            const option = event.target;
            selectTrigger.textContent = option.textContent;
            hiddenSelect.value = option.getAttribute('data-value');
            customOptions.querySelectorAll('.custom-option').forEach(opt => opt.classList.remove('selected'));
            option.classList.add('selected');
            customOptions.classList.remove('open');
        }
    });

    document.addEventListener('click', function (e) {
        if (!selectWrapper.contains(e.target)) {
            customOptions.classList.remove('open');
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {

    const selectWrapper = document.querySelector(".custom-select-wrapper");
    const options = document.querySelectorAll(".custom-option");
    const trigger = document.querySelector(".custom-select-trigger");
    const clinicaForm = document.getElementById("clinicaForm");
    const tutorForm = document.getElementById("tutorForm");

    document.addEventListener("click", function (e) {
        if (!selectWrapper.contains(e.target)) {
            selectWrapper.classList.remove("open");
        }
    });

    trigger.addEventListener("click", function () {
        selectWrapper.classList.toggle("open");
    });

    options.forEach(option => {
        option.addEventListener("click", function () {
            const selectedValue = this.getAttribute("data-value");
            trigger.textContent = this.textContent; 

            if (selectedValue === "clinica") {
                clinicaForm.style.display = "block";
                tutorForm.style.display = "none";
            } else if (selectedValue === "tutor") {
                tutorForm.style.display = "block";
                clinicaForm.style.display = "none";
            } else {
                clinicaForm.style.display = "none";
                tutorForm.style.display = "none";
            }

            selectWrapper.classList.remove("open");
        });
    });
});

$(document).ready(function () {

    $('#cep').mask('00000-000');
    $('#cnpjClinica').mask('00.000.000/0000-00');
    $('#cpfTutor').mask('000.000.000-00', { reverse: true });

    var telefoneMascara = function (val) {

        return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00000';
    };

    var telefoneOptions = {
        onKeyPress: function (val, e, field, options) {

            field.mask(telefoneMascara.apply({}, arguments), options);
        }
    };

    $('#telClinica, #telTutor').mask(telefoneMascara, telefoneOptions);

    $('#buscarEndereco').on('click', function (event) {
        event.preventDefault(); 

        let cep = $('#cep').val().replace('-', ''); 

        if (cep.length !== 8) {
            alert('Por favor, insira um CEP válido.');
            return;
        }

        $.ajax({
            url: `https://viacep.com.br/ws/${cep}/json/`,
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                if (!response.erro) {

                    $('#rua').val(response.logradouro);
                    $('#bairro').val(response.bairro);
                    $('#cidade').val(response.localidade);
                    $('#estado').val(response.uf);
                } else {
                    alert('CEP não encontrado. Por favor, tente novamente.');
                }
            },
            error: function () {
                alert('Erro ao buscar o CEP. Verifique sua conexão ou tente novamente mais tarde.');
            }
        });
    });
});

document.getElementById('senha-clinica').addEventListener('click', function () {
    const senhaInput = document.getElementById('senhaClinica');
    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        this.textContent = 'Ocultar';
    } else {
        senhaInput.type = 'password';
        this.textContent = 'Mostrar';
    }
});

document.getElementById('confirm-senha-clinica').addEventListener('click', function () {
    const senhaInput = document.getElementById('confirm-senhaCli');
    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        this.textContent = 'Ocultar';
    } else {
        senhaInput.type = 'password';
        this.textContent = 'Mostrar';
    }
});

document.getElementById('senha-tutor').addEventListener('click', function () {
    const senhaInput = document.getElementById('senhaTutor');
    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        this.textContent = 'Ocultar';
    } else {
        senhaInput.type = 'password';
        this.textContent = 'Mostrar';
    }
});

document.getElementById('confirm-senha-tutor').addEventListener('click', function () {
    const senhaInput = document.getElementById('confirm-senhaTutor');
    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        this.textContent = 'Ocultar';
    } else {
        senhaInput.type = 'password';
        this.textContent = 'Mostrar';
    }
});

function validarFormulario() {
    var selecionado = document.getElementById('tipoUsuario').value;

    if (selecionado == 'tutor') {
        var nome = document.getElementById("nomeTutor").value;
        var telefone = document.getElementById("telTutor").value;
        var email = document.getElementById("emailTutor").value;
        var cpf = document.getElementById("cpfTutor").value;
        var nasc = document.getElementById("nascTutor").value;
        var senha = document.getElementById("senhaTutor").value;
        var confirmSenha = document.getElementById("confirm-senhaTutor").value;

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

        if (!cpf || !/^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(cpf)) {
            erros.push("O campo CPF deve estar no formato 000.000.000-00.");
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
        var nome = document.getElementById("nomeClinica").value;
        var telefone = document.getElementById("telClinica").value;
        var email = document.getElementById("emailClinica").value;
        var cnpj = document.getElementById("cnpjClinica").value;
        var senha = document.getElementById("senhaClinica").value;
        var confirmSenha = document.getElementById("confirm-senhaCli").value;

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

        if (!cnpj || !/^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/.test(cnpj)) {
            erros.push("O campo CNPJ deve estar no formato 00.000.000/0000-00.");
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
}
