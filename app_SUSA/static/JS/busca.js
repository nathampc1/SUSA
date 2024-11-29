function filtro_distancia() {
    const filtro = document.getElementById("filtro-animacao").value;

    fetch(`/listar_distancia?filter=${filtro}`)
        .then(response => response.json())
        .then(data => {

            const clinicList = document.getElementById("clinica-lista");
            clinicList.innerHTML = "";

            data.clinicas.forEach(clinica => {
                const clinicItem = document.createElement("div");
                clinicItem.classList.add("clinica-item");

                let cnpjFormatado = clinica.cnpj.replace(/\D/g, '');

                clinicItem.innerHTML = `
                <a href="/perfil_clinica/${cnpjFormatado}" target="main-iframe">
                    <div class="clinica-info">
                        <p class="clinica-name">${clinica.nome}</p>
                        <p class="clinica-distancia">${clinica.distancia.toFixed(2) + ' KM'}</p>
                    </div>
                </a>
                `;

                clinicList.appendChild(clinicItem);
            });
        })
        .catch(error => console.error("Erro ao buscar clínicas:", error));
}
