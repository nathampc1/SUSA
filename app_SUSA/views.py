from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from app_SUSA.models import Clinica, Tutor, Endereco, Servico, Pet, Agendamento, Vacina, ConsultaRealizada
from django.http import JsonResponse
import re
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from django.utils.timezone import now


def login(request):
    return render(request, 'publico/login.html')

def cadastro(request):
    return render(request, 'publico/cadastro.html')

@xframe_options_exempt
def finalizar_consulta(request, agendamento_id):
    if request.method == 'POST':

        agendamento = get_object_or_404(Agendamento, id_agendamento=agendamento_id)


        tipo_nota = request.POST.get('nota_acompanhamento', '').strip()
        nova_observacao = request.POST.get('nova_observacao', '').strip()
        status_pet = request.POST.get('status_animal', '').strip()


        ConsultaRealizada.objects.create(
            data=now().date(),
            tipo_nota=tipo_nota,
            nota=nova_observacao,
            statuspet=status_pet,
            pet_id_pet=agendamento.pet_id,
        )


        vacinas_selecionadas = [
            key for key in request.POST if key.startswith('vacina_selecionada')
        ]


        if vacinas_selecionadas:
            for key in vacinas_selecionadas:
                vacina_id = request.POST[key]
                lote = request.POST.get(f'lote_{vacina_id}', '').strip()
                reaplicacao = request.POST.get(f'reaplicacao_{vacina_id}', None)


                vacina_servico = Servico.objects.filter(id_servico=vacina_id).first()
                if vacina_servico:
                    Vacina.objects.create(
                        nome=vacina_servico.descricao,
                        validade=reaplicacao or now().date(),
                        lote=lote,
                        fab=now().date(),  
                        pet=agendamento.pet_id  
                    )

        if status_pet == 'Retorno':
            data_retorno = request.POST.get('data_retorno')
            hora_retorno = request.POST.get('hora_retorno')

            print('Entrou retorno')

            if data_retorno and hora_retorno:
                Agendamento.objects.create(
                    tipo="Consulta",
                    data=data_retorno,
                    horario=hora_retorno,
                    obs="Retorno solicitado pela clínica",
                    status="Confirmado",
                    pet_id=agendamento.pet_id,
                    clinica_cnpj=agendamento.clinica_cnpj,
                    tutor_cpf=agendamento.tutor_cpf,
                )
                messages.success(request, "Consulta finalizada e retorno agendado com sucesso!")
            else:
                messages.error(request, "Preencha a data e horário para o retorno.")


        agendamento.status = "Concluído"
        agendamento.save()

        messages.success(request, "Consulta finalizada com sucesso!")
        return redirect('/agendamentos')

    messages.error(request, "Método inválido para finalizar a consulta.")
    return redirect('/agendamentos')

@xframe_options_exempt
def abrir_prontuario(request, agendamento_id):
    cnpj_clinica = request.session.get('cnpj')

    if not cnpj_clinica:
        return render(request, 'clinica/erro.html', {'mensagem': 'Clínica não encontrada na sessão.'})


    vacinas = Servico.objects.filter(tipo="vacina", clinica_cnpj=cnpj_clinica)


    agendamento = get_object_or_404(Agendamento, id_agendamento=agendamento_id)


    consultas_realizadas = ConsultaRealizada.objects.filter(pet_id_pet=agendamento.pet_id).order_by('-data')


    historico_observacoes = [
        f"{consulta.data.strftime('%d/%m/%Y')} | {consulta.nota}"
        for consulta in consultas_realizadas
    ]

    context = {
        'vacinas': vacinas,
        'agendamento': agendamento,
        'historico_observacoes': historico_observacoes  
    }

    return render(request, 'clinica/prontuario.html', context)

@xframe_options_exempt
def confirmacao(request, agendamento_id):

    agendamento = get_object_or_404(Agendamento, id_agendamento=agendamento_id)

    if request.method == "POST":

        status = request.POST.get("status")

        if status in ["Confirmado", "Cancelado"]:

            agendamento.status = status
            agendamento.save()


            messages.success(
                request,
                f"Consulta marcada como {status} com sucesso!"
            )
        else:

            messages.error(
                request,
                "Ocorreu um erro ao tentar atualizar o status da consulta."
            )


    context = {
        "agendamento": agendamento,
    }

    return render(request, "clinica/confirmacao_consulta.html", context)

@xframe_options_exempt
def confirmar_consulta(request, id_agendamento):

    agendamento = get_object_or_404(Agendamento, id_agendamento=id_agendamento)


    context = {
        'agendamento': agendamento
    }


    return render(request, 'clinica/confirmacao_consulta.html', context)

@xframe_options_exempt
def excluir_servico(request):
    if request.method == 'POST':
        id_servico = request.POST.get('id_servico')

        try:

            servico = Servico.objects.get(id_servico=id_servico)
            servico.delete()
            messages.success(request, 'Serviço excluído com sucesso!')
        except Servico.DoesNotExist:
            messages.error(request, 'Serviço não encontrado.')


    return redirect('/servico')


@xframe_options_exempt
def filtrar_agendamentos(request):
    cnpj_clinica = request.session.get('cnpj')
    agendamentos = Agendamento.objects.filter(clinica_cnpj=cnpj_clinica)


    nome = request.GET.get('nome_solicitante', '').strip()
    data = request.GET.get('data_agendamento', '').strip()
    status = request.GET.get('status_agendamento', '').strip()
    tipo = request.GET.get('tipo_consulta', '').strip()


    if nome:
        agendamentos = agendamentos.filter(tutor_cpf__nome__icontains=nome)
    if data:
        try:

            data_formatada = datetime.strptime(data, '%Y-%m-%d').date()
            agendamentos = agendamentos.filter(data=data_formatada)
        except ValueError:
            print("Erro ao converter a data. Certifique-se de que está no formato correto.")
    if status:
        agendamentos = agendamentos.filter(status=status)
    if tipo:
        agendamentos = agendamentos.filter(tipo=tipo)


    context = {
        'agendamentos': agendamentos,
        'filtros': {
            'nome': nome,
            'data': data,
            'status': status,
            'tipo': tipo,
        }
    }
    return render(request, 'clinica/agendamentos.html', context)

@xframe_options_exempt
def agendamentos(request):

    cnpj_clinica = request.session.get('cnpj')


    if not cnpj_clinica:
        return render(request, 'clinica/agendamentos.html', {'erro': 'CNPJ não encontrado na sessão.'})


    nome_solicitante = request.GET.get('nome_solicitante', '').strip()
    data_agendamento = request.GET.get('data_agendamento', '').strip()
    status_agendamento = request.GET.get('status_agendamento', '').strip()
    tipo_consulta = request.GET.get('tipo_consulta', '').strip()


    agendamentos = Agendamento.objects.filter(clinica_cnpj__cnpj=cnpj_clinica)


    if nome_solicitante:
        agendamentos = agendamentos.filter(tutor_cpf__nome__icontains=nome_solicitante)

    if data_agendamento:
        agendamentos = agendamentos.filter(data=data_agendamento)

    if status_agendamento:
        agendamentos = agendamentos.filter(status=status_agendamento)

    if tipo_consulta:
        agendamentos = agendamentos.filter(tipo=tipo_consulta)


    filtros = {
        'nome': nome_solicitante,
        'data': data_agendamento,
        'status': status_agendamento,
        'tipo': tipo_consulta
    }

    return render(request, 'clinica/agendamentos.html', {
        'agendamentos': agendamentos,
        'filtros': filtros
    })


@xframe_options_exempt
def realizar_agendamento(request, cnpj):
    cnpj_formatado = formatar_cnpj(cnpj)  
    clinica = get_object_or_404(Clinica, cnpj=cnpj_formatado)
    cpf = request.session.get('cpf')
    pets = Pet.objects.filter(tutor_cpf=cpf)


    vacinas = Servico.objects.filter(clinica_cnpj=cnpj_formatado, tipo="vacina")
    consultas = Servico.objects.filter(clinica_cnpj=cnpj_formatado, tipo="consulta")

    if request.method == 'POST':
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        obs = request.POST.get('obs_agendamento')
        pet_id = request.POST.get('filtro-animacao')


        vacinas_selecionadas = []
        consultas_selecionadas = []


        for key, value in request.POST.items():
            if key.startswith("vacina --"):
                vacina_id = key.split(" -- ")[1]
                vacinas_selecionadas.append(vacina_id)
            elif key.startswith("consulta --"):
                consulta_id = key.split(" -- ")[1]
                consultas_selecionadas.append(consulta_id)


        if vacinas_selecionadas and consultas_selecionadas:
            tipo_agendamento = "Vacina e Consulta"
        elif vacinas_selecionadas:
            tipo_agendamento = "Vacina"
        elif consultas_selecionadas:
            tipo_agendamento = "Consulta"
        else:
            tipo_agendamento = "Agendamento Geral"

        if data and horario and pet_id:

            pet = get_object_or_404(Pet, id_pet=pet_id)


            servicos_descricao = []
            for vacina_id in vacinas_selecionadas:
                vacina = vacinas.filter(id_servico=vacina_id).first()
                if vacina:
                    servicos_descricao.append(vacina.descricao)

            for consulta_id in consultas_selecionadas:
                consulta = consultas.filter(id_servico=consulta_id).first()
                if consulta:
                    servicos_descricao.append(consulta.descricao)

            servicos_texto = "\n".join(servicos_descricao)
            obs_completa = f"Serviços solicitados:\n{servicos_texto}\n\n{obs}"


            agendamento = Agendamento.objects.create(
                tipo=tipo_agendamento,
                data=data,
                horario=horario,
                obs=obs_completa,
                status="Pendente",
                pet_id=pet,
                clinica_cnpj=clinica,
                tutor_cpf=pet.tutor_cpf
            )

            messages.success(request, "Agendamento realizado com sucesso!")
            return redirect('perfil_clinica', cnpj=cnpj.replace(".", "").replace("/", "").replace("-", ""))
        else:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")

    return render(request, 'tutor/perfil_clinica.html', {
        'clinica': clinica,
        'vacina': vacinas,
        'consulta': consultas,
        'pets': pets
    })




def formatar_cnpj(cnpj):

    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

@xframe_options_exempt
def perfil_clinica(request, cnpj):
    cnpj = formatar_cnpj(cnpj)
    cpf = request.session.get('cpf')

    vacinas = Servico.objects.filter(clinica_cnpj=cnpj, tipo="vacina")
    consultas = Servico.objects.filter(clinica_cnpj=cnpj, tipo="consulta")

    for vacina in vacinas:
        vacina.preco = f"{float(vacina.preco):,.2f}".replace(".", ",")

    for consulta in consultas:
        consulta.preco = f"{float(consulta.preco):,.2f}".replace(".", ",")

    clinica = get_object_or_404(Clinica, cnpj=cnpj)
    pets = Pet.objects.filter(tutor_cpf=cpf)  
    
    return render(request, 'tutor/perfil_clinica.html', {'clinica': clinica, 'vacina': vacinas, 'consulta': consultas, 'pets': pets})

def geocode_tentativa(geolocator, address, retries=3, timeout=2):
    """Função para tentar geocodificar várias vezes em caso de timeout."""
    for i in range(retries):
        try:
            return geolocator.geocode(address, timeout=timeout)
        except GeocoderTimedOut:
            print(f"Tentativa {i+1} falhou. Tentando novamente...")
            time.sleep(1)  
    return None

def listar_distancia(request):
    print('Entrou na distancia')
    filter_type = request.GET.get('filter')
    print(filter_type)
    cpf_tutor = request.session.get('cpf')
    endereco_tutor = Endereco.objects.filter(tutor_cpf=cpf_tutor).first()
    
    if not endereco_tutor:
        return JsonResponse({'clinicas': []})
    
    geolocator = Nominatim(user_agent="sua_aplicacao")
    endereco_completo_tutor = f"{endereco_tutor.rua}, {endereco_tutor.cidade}, {endereco_tutor.estado}"
    location_tutor = geocode_tentativa(geolocator, endereco_completo_tutor)

    if not location_tutor:
        return JsonResponse({'clinicas': []})

    tutor_coords = (location_tutor.latitude, location_tutor.longitude)
    
    clinicas_distancias = []
    clinicas = Clinica.objects.all()

    for clinica in clinicas:
        endereco_clinica = Endereco.objects.filter(clinica_cnpj=clinica.cnpj).first()
        if endereco_clinica:
            endereco_completo_clinica = f"{endereco_clinica.rua}, {endereco_clinica.cidade}, {endereco_clinica.estado}"
            location_clinica = geocode_tentativa(geolocator, endereco_completo_clinica)
            if location_clinica:
                clinica_coords = (location_clinica.latitude, location_clinica.longitude)
                distancia = geodesic(tutor_coords, clinica_coords).kilometers
                clinica_info = {
                    'nome': clinica.nome,
                    'distancia': distancia,
                    'cnpj': clinica.cnpj,
                    'preco': clinica.preco if hasattr(clinica, 'preco') else 0  
                }
                

                clinicas_distancias.append(clinica_info)
    

    if filter_type == 'decrescente':
        clinicas_ordenadas = sorted(clinicas_distancias, key=lambda x: x['distancia'])
    elif filter_type == 'crescente':
        clinicas_ordenadas = sorted(clinicas_distancias, key=lambda x: x['distancia'], reverse=True)
        print('entrou na organização decrescente de distância')
    elif filter_type == 'preco':
        clinicas_ordenadas = sorted(clinicas_distancias, key=lambda x: x['preco'])
    else:
        clinicas_ordenadas = clinicas_distancias  

    return JsonResponse({'clinicas': clinicas_ordenadas})

@xframe_options_exempt
def Busca(request):
    clinicas = Clinica.objects.all()
    return render(request, 'tutor/busca.html', {'clinicas': clinicas})

@xframe_options_exempt
def atualizar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id_pet=pet_id)

    if request.method == "POST":
        pet.nome = request.POST.get("nome")
        pet.nasc = request.POST.get("nasc")
        pet.peso = request.POST.get("peso")
        pet.sexo = request.POST.get("sexo")
        
        pet.save()
        return redirect('/meupet')  

    return redirect('/meupet')

@xframe_options_exempt
def perfilPet(request, pet_id):

    pet = get_object_or_404(Pet, id_pet=pet_id)


    consultas_agendadas = Agendamento.objects.filter(pet_id=pet).order_by('data', 'horario')


    consultas_realizadas = ConsultaRealizada.objects.filter(pet_id_pet=pet).order_by('-data')


    vacinas_aplicadas = Vacina.objects.filter(pet=pet).order_by('-validade')

    context = {
        'pet': pet,
        'consultas_agendadas': consultas_agendadas,
        'consultas_realizadas': consultas_realizadas,
        'vacinas_aplicadas': vacinas_aplicadas,
    }

    return render(request, 'tutor/perfilpet.html', context)

logger = logging.getLogger(__name__)

@csrf_exempt
def excluir_pet(request, pet_id):
    print('entrou na função')
    if request.method == 'POST':
        try:

            pet = Pet.objects.get(id_pet=pet_id)
            pet.delete()
            return JsonResponse({"success": True, "message": "Pet excluído com sucesso"}, status=200)
        except Pet.DoesNotExist:

            return JsonResponse({"success": False, "error": "Pet não encontrado"}, status=404)
        except Exception as e:

            logger.error(f"Erro ao excluir o pet: {e}")
            return JsonResponse({"success": False, "error": f"Erro ao excluir o pet: {str(e)}"}, status=500)
    else:
        return JsonResponse({"success": False, "error": "Método não permitido"}, status=405)

@xframe_options_exempt
def addPet(request):
    if request.method == "POST":

        nome = request.POST.get("nome")
        nascimento = request.POST.get("nascimento")
        sexo = request.POST.get("sexo")
        peso = request.POST.get("peso")
        idade = request.POST.get("idade")
        raca = request.POST.get("raca")
        cpf = request.session.get('cpf')
        tutor = Tutor.objects.get(cpf=cpf)
        

        try:
            novo_pet = Pet(
                nome=nome,
                nasc=nascimento,
                sexo=sexo,
                peso=peso,
                idade=idade,
                raca=raca,
                tutor_cpf=tutor
            )
            novo_pet.save()
            return redirect('/meupet')
        except Exception as e:
            print("Erro ao salvar o pet:", e)
            return redirect('/meupet')
    else:
        print('não entrou no post')
        return redirect('/meupet')

@xframe_options_exempt
def meuPet(request):

    cpf_tutor = request.session.get('cpf')
    tutor = Tutor.objects.get(cpf=cpf_tutor)
    

    pets = Pet.objects.filter(tutor_cpf=tutor)


    return render(request, 'tutor/meupet.html', {'pets': pets})

def clinica(request):

    clinica_cnpj = request.session.get('cnpj')
    

    if not clinica_cnpj:
        return redirect('/login')
    

    clinica = Clinica.objects.get(cnpj=clinica_cnpj)
    

    context = {
        'nome': clinica.nome,
    }
    return render(request, 'clinica/clinica.html', context)

def tutor(request):

    tutor_cpf = request.session.get('cpf')
    

    if not tutor_cpf:
        return redirect('/login')
    

    tutor = Tutor.objects.get(cpf=tutor_cpf)
    

    context = {
        'nome': tutor.nome,
    }
    
    return render(request, 'tutor/tutor.html', context)

@xframe_options_exempt
def msgInicial(request):
     return render(request, 'publico/msg-inicial.html')

@xframe_options_exempt
def perfilClinica(request):

    clinica_cnpj = request.session.get('cnpj')
    

    if not clinica_cnpj:
        return redirect('/login')
    

    clinica = Clinica.objects.get(cnpj=clinica_cnpj)
    

    context = {
        'nome': clinica.nome,
        'email': clinica.email,
        'telefone': clinica.tel,
        'crmv': clinica.crmv,
    }
    
    return render(request, 'clinica/perfil.html', context)

@xframe_options_exempt
def perfilTutor(request):

    tutor_cpf = request.session.get('cpf')
    

    if not tutor_cpf:
        return redirect('/login')
    

    tutor = Tutor.objects.get(cpf=tutor_cpf)
    

    context = {
        'nome': tutor.nome,
        'email': tutor.email,
        'telefone': tutor.tel,
        'nascimento': tutor.nasc
    }
    
    return render(request, 'tutor/perfil.html', context)

def atualizarDadosC(request):
    print('entrou no atualizar dados')

    if request.method == "POST":
        clinica_cnpj = request.session.get('cnpj')
        if not clinica_cnpj:
            return redirect('/login')  

        clinica = Clinica.objects.get(cnpj=clinica_cnpj)


        clinica.nome = request.POST.get('nome')
        clinica.email = request.POST.get('email')
        clinica.tel = request.POST.get('telefone')
        clinica.crmv = request.POST.get('crmv')


        senha = request.POST.get('senha')
        confirm_senha = request.POST.get('confirmSenha')
        if senha and senha == confirm_senha:
            clinica.senha = make_password(senha)
        
        clinica.save()


        return redirect('/perfilC')
    else:
        return redirect('/login')
    
def atualizarDadosT(request):
    print('entrou no atualizar dados')

    if request.method == "POST":
        tutor_cpf = request.session.get('cpf')
        if not tutor_cpf:
            return redirect('/login')  

        tutor = Tutor.objects.get(cpf=tutor_cpf)


        senha = request.POST.get('senha')
        confirm_senha = request.POST.get('confirmSenha')
        if senha and senha == confirm_senha:
            tutor.senha = make_password(senha)
        
        tutor.save()


        return redirect('/perfilT')
    else:
        return redirect('/login')

@xframe_options_exempt
def cadServico(request):

    clinica_cnpj = request.session.get('cnpj')

    if not clinica_cnpj:

        return redirect('/login')  
    

    vacinas = Servico.objects.filter(tipo="vacina", clinica_cnpj=clinica_cnpj)
    consultas = Servico.objects.filter(tipo="consulta", clinica_cnpj=clinica_cnpj)


    return render(request, 'clinica/servico.html', {'vacinas': vacinas, 'consultas': consultas})

def atualizar_servico(request):
    if request.method == 'POST':
        id_servico = request.POST.get('id_servico')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        preco = preco.replace(',', '.')
        tipo_servico = request.POST.get('tipo_servico')

        try:

            servico = Servico.objects.get(id_servico=id_servico)
            servico.descricao = descricao
            servico.preco = preco
            servico.tipo = tipo_servico
            servico.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
        except Servico.DoesNotExist:
            messages.error(request, 'Serviço não encontrado.')


    return redirect('/servico')

def CadastrarServicoV(request):
     
     if request.method == "POST":
        desc = request.POST.get('descVacina')
        val = request.POST.get('valVacina')
        val = val.replace(',', '.')
        cnpj = request.session.get('cnpj')
        clinica = Clinica.objects.get(cnpj=cnpj)
        
        nova_vacina = Servico (
             descricao=desc,
             preco=val,
             tipo='vacina',
             clinica_cnpj=clinica
        )
        nova_vacina.save()
        return redirect('/servico')
     
def CadastrarServicoC(request):
     
     if request.method == "POST":
        desc = request.POST.get('descConsulta')
        val = request.POST.get('valConsulta')
        val = val.replace(',', '.')
        cnpj = request.session.get('cnpj')
        clinica = Clinica.objects.get(cnpj=cnpj)
        
        nova_consulta = Servico (
             descricao=desc,
             preco=val,
             tipo='consulta',
             clinica_cnpj=clinica
        )
        nova_consulta.save()
        return redirect('/servico')

def RealizarLogin(request):
    
    if request.method == "POST":

        login = request.POST.get('cpf_cnpj')
        senha = request.POST.get('senha')


        verifica_cnpj = re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', login)
        verifica_cpf = re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', login)

        if verifica_cnpj:
            try:
                clinica = Clinica.objects.get(cnpj=login)
                if check_password(senha, clinica.senha):
                    request.session['cnpj'] = clinica.cnpj
                    request.session['nome'] = clinica.nome
                    request.session['email'] = clinica.email
                    request.session['tel'] = clinica.tel
                    request.session['crmv'] = clinica.crmv

                    return redirect('/clinica')
                else:
                    return render(request, 'publico/login.html', {'erro': 'Senha incorreta ou usuário incorretos!'})
            except Clinica.DoesNotExist:
                return render(request, 'publico/login.html', {'erro': 'Clínica não encontrada!'})
        
        if verifica_cpf:
            try:
                tutor = Tutor.objects.get(cpf=login)
                if check_password(senha, tutor.senha):
                    request.session['cpf'] = tutor.cpf
                    request.session['nome'] = tutor.nome
                    request.session['email'] = tutor.email
                    request.session['tel'] = tutor.tel
                    data_nascimento = tutor.nasc.strftime('%Y-%m-%d')
                    request.session['nasc'] = data_nascimento

                    return redirect('/tutor')
                else:
                    return render(request, 'publico/login.html', {'erro': 'Senha incorreta ou usuário incorretos!'})
            except Tutor.DoesNotExist:
                return render(request, 'publico/login.html', {'erro': 'Tutor não encontrada!'})
            
def RealizarLogout(request):
    request.session.flush()
    return redirect('/')

def cadastrarUser(request):
    if request.method == "POST":

        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        tipo_usuario = request.POST.get('Usuario')
        nome = request.POST.get('nomeTutor')

        if tipo_usuario == 'clinica':

            nome = request.POST.get('nomeClinica')
            telefone = request.POST.get('telClinica')
            email = request.POST.get('emailClinica')
            cnpj = request.POST.get('cnpjClinica')
            senha = request.POST.get('senhaClinica')
            crmv = request.POST.get('CRMV')


            email = request.POST.get('emailClinica') if tipo_usuario == 'clinica' else request.POST.get('emailTutor')
            if Tutor.objects.filter(email=email).exists() or Clinica.objects.filter(email=email).exists():
                        return render(request, 'publico/cadastro.html', {'erro': 'O email já está em uso.'})

            elif tipo_usuario == 'clinica':
                cnpj = request.POST.get('cnpjClinica')
                if Clinica.objects.filter(cnpj=cnpj).exists():
                    return render(request, 'publico/cadastro.html', {'erro': 'O CNPJ já está cadastrado.'})



            senha_criptografada = make_password(senha)

            nova_clinica = Clinica(
                crmv=crmv,
                nome=nome,
                tel=telefone,
                email=email,
                cnpj=cnpj,
                senha=senha_criptografada
            )
            nova_clinica.save()

            novo_endereco = Endereco(
                cep=cep,
                rua=rua,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                clinica_cnpj=nova_clinica,
                tutor_cpf=None
            )
            novo_endereco.save()
            return render(request, 'publico/login.html')

        elif tipo_usuario == 'tutor':

            nome = request.POST.get('nomeTutor')
            telefone = request.POST.get('telTutor')
            email = request.POST.get('emailTutor')
            cpf = request.POST.get('cpfTutor')
            nasc = request.POST.get('nascTutor')
            senha = request.POST.get('senhaTutor')

            email = request.POST.get('emailClinica') if tipo_usuario == 'clinica' else request.POST.get('emailTutor')
            if Tutor.objects.filter(email=email).exists() or Clinica.objects.filter(email=email).exists():
                        return render(request, 'publico/cadastro.html', {'erro': 'O email já está em uso.'})


            if tipo_usuario == 'tutor':
                cpf = request.POST.get('cpfTutor')
                if Tutor.objects.filter(cpf=cpf).exists():
                    return render(request, 'publico/cadastro.html', {'erro': 'O CPF já está cadastrado.'})
                

            senha_criptografada = make_password(senha)
            novo_tutor = Tutor(
                nome=nome,
                tel=telefone,
                email=email,
                cpf=cpf,
                nasc=nasc,
                senha=senha_criptografada
            )
            novo_tutor.save()

            novo_endereco = Endereco(
                cep=cep,
                rua=rua,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                clinica_cnpj=None,
                tutor_cpf=novo_tutor
            )
            novo_endereco.save()
            return render(request, 'publico/login.html')