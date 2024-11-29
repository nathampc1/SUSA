
//modulo_colaborador.hmtl ...............................................
function menuMove() {
    var sidebar = document.getElementById("sidebar");
    var mainContent = document.getElementById("main-content");
    if (sidebar.style.left == "-200px") {
        sidebar.style.left = "0";
        mainContent.style.marginLeft = "25%";
        document.addEventListener('click', handleClickOutside, true);
    } else {
        sidebar.style.left = "-200px";
        mainContent.style.marginLeft = "25%";
        document.removeEventListener('click', handleClickOutside, true);
    }
}

function altIframe(){
    var iframe = document.getElementById('main-iframe');
    iframe.src = "perfil.html";
}

//perfil.html ............................................................
function clickFILE() {
    document.getElementById('fileInput').click();
}

function editarPerfil() {
    document.getElementById('btnEditar').style.display = 'none';
    document.getElementById('btnCancelar').style.display = 'block';
    document.getElementById('btnSalvar').style.display = 'block';
    document.getElementById('email').disabled = false;
    document.getElementById('opcoes').disabled = false;
    document.getElementById('senha').disabled = false;
    document.getElementById('confirmSenha').disabled = false;
    document.getElementById('icone').style.cursor = 'pointer'

    var fotoPerfil = document.getElementById('foto-perfil');
    fotoPerfil.style.cursor = 'default';
}

function desabilitarBtn() {
    document.getElementById('btnEditar').style.display = 'block';
    document.getElementById('btnCancelar').style.display = 'none';
    document.getElementById('btnSalvar').style.display = 'none';
    document.getElementById('email').disabled = true;
    document.getElementById('opcoes').disabled = true;
    document.getElementById('senha').disabled = true;
    document.getElementById('confirmSenha').disabled = true;
    document.getElementById('icone').style.cursor = 'default'

    var fotoPerfil = document.getElementById('foto-perfil');
    fotoPerfil.style.cursor = 'default';
}
