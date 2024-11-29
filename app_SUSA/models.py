from django.db import models


class Agendamento(models.Model):
    id_agendamento = models.AutoField(primary_key=True)  
    tipo = models.CharField(max_length=20)
    data = models.DateField()
    obs = models.TextField()
    horario = models.CharField(max_length=5)
    status = models.CharField(max_length=15)
    pet_id = models.ForeignKey('Pet', on_delete=models.DO_NOTHING, db_column='pet_id')
    clinica_cnpj = models.ForeignKey('Clinica', on_delete=models.DO_NOTHING, db_column='clinica_cnpj')
    tutor_cpf = models.ForeignKey('Tutor', on_delete=models.DO_NOTHING, db_column='tutor_cpf')

    class Meta:
        managed = False
        db_table = 'agendamento'
        unique_together = (('id_agendamento', 'clinica_cnpj', 'tutor_cpf', 'pet_id'),)


class Clinica(models.Model):
    cnpj = models.CharField(primary_key=True, max_length=18)
    crmv = models.CharField(max_length=20)
    nome = models.CharField(max_length=45)
    tel = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=100)
    senha = models.CharField(max_length=45)

    class Meta:
        db_table = 'clinica'


class ConsultaRealizada(models.Model):
    id_consulta = models.AutoField(primary_key=True) 
    data = models.DateField() 
    tipo_nota = models.CharField(max_length=1) 
    nota = models.TextField()  
    statuspet = models.CharField(db_column='statusPet', max_length=20)  
    pet_id_pet = models.ForeignKey(  
        'Pet',
        on_delete=models.DO_NOTHING,
        db_column='pet_id_pet'
    )

    class Meta:
        db_table = 'consulta_realizada' 


class Pet(models.Model):
    id_pet = models.AutoField(primary_key=True)
    tutor_cpf = models.ForeignKey('Tutor', on_delete=models.DO_NOTHING, db_column='tutor_cpf')  
    nasc = models.DateField()
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1)
    peso = models.FloatField()
    idade = models.IntegerField()
    raca = models.CharField(max_length=45)

    class Meta:
        db_table = 'pet'


class Servico(models.Model):
    id_servico = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15)
    preco = models.FloatField()
    clinica_cnpj = models.ForeignKey('Clinica', on_delete=models.DO_NOTHING, db_column='clinica_cnpj')

    class Meta:
        managed = False
        db_table = 'servico'
        unique_together = (('id_servico', 'clinica_cnpj'),)


class Tutor(models.Model):
    cpf = models.CharField(primary_key=True, max_length=14)
    nome = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    nasc = models.DateField()
    senha = models.CharField(max_length=45)

    class Meta:
        db_table = 'tutor'


class Endereco(models.Model):
    id_endereco = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    clinica_cnpj = models.ForeignKey(Clinica, models.DO_NOTHING, db_column='clinica_cnpj', null=True, blank=True)
    tutor_cpf = models.ForeignKey(Tutor, models.DO_NOTHING, db_column='tutor_cpf', null=True, blank=True)

    class Meta:
        db_table = 'endereco'


class Vacina(models.Model):
    id_vacina = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45)
    validade = models.DateField()
    lote = models.CharField(max_length=45)
    fab = models.DateField()
    pet = models.ForeignKey('Pet', on_delete=models.DO_NOTHING, db_column='pet_id') 

    class Meta:
        managed = False
        db_table = 'vacina'
