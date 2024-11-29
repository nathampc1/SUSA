function ValidarFormulario() {
    
    var nome = document.getElementById("nome").value;
    var nascimento = document.getElementById("nasc").value;
    var sexo = document.getElementById("sexo").value;
    var peso = document.getElementById("peso").value;
    
    var erros = [];

    if (!nome) erros.push("O campo Nome é obrigatório.");
    if (!nascimento) erros.push("O campo Data de Nascimento é obrigatório.");
    if (!sexo) erros.push("O campo Sexo é obrigatório.");

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