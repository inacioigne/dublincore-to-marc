import csv
from pymarc import Record, Field

#EXTRAIR METADADOS DO CSV
with open(input('CSV: '), encoding='utf-8') as arquivo:
    ler = csv.DictReader(arquivo)
    for i in ler:
        metadados = i

if i['dc.type[por]'] == 'Dissertação':
    tipo = 'Dissertação'
    tipo_code = 'D'
    grau = '(mestre) -'
elif i['dc.type[por]'] == 'Tese':
    tipo = 'Tese'
    tipo_code = 'T'
    grau = '(Doutor(a)) -'
else:
    print('Tipo Desconhecido')
    
cdd = input('CDD: ')
cutter = input('Cutter: ')
autor = metadados['dc.creator']
tmp = autor.split(',')
responsabilidade = tmp[1].strip()+' '+tmp[0]
titulo = metadados['dc.title[por]']
ano = metadados['dc.date.issued'][0:4]
resumo = metadados['dc.description.resumo[por]']
try:
    assunto = metadados['dc.subject[por]'].split('||')
except KeyError:
    assunto = metadados['dc.subject'].split('||')
orientador = metadados['dc.contributor.advisor1']

if 'dc.contributor.advisor-co1' in metadados.keys():
    coorientador = metadados['dc.contributor.advisor-co1']

link = metadados['dc.identifier.uri']

#GRAVAR ARQUIVO MARC

marc = Record(force_utf8=True)
marc.add_field(
    Field(tag ='003', data='BR-MnINPA'),
    Field(tag ='008', data='190731b'+ano+'       ||||| |||| 00| 0 por d'),
    Field(
        tag ='082',
        indicators = ['0','#'],
        subfields = ['2','23', 'a', cdd]),
    Field(
        tag ='090',
        indicators = ['#','#'],
        subfields = ['a', 'T '+cdd,
                     'b', cutter]),     
    Field(
        tag = '100',
        indicators = ['1','#'],
        subfields = [
            'a', autor]),
    Field(
        tag = '245',
        indicators = ['0','#'],
        subfields = [
            'a', titulo+' /',
            'c', responsabilidade+'.']),
    Field(
        tag ='260',
        indicators = ['#','#'],
        subfields = [
            'a', 'Manaus: ',
            'b', 'Sem editor,',
            'c', ano+'.']),
    Field(
        tag = '502',
        indicators = ['#','#'],
        subfields = [
            'a', tipo,
            'b', grau,
            'c', 'INPA,',
            'd', ano+'.']),
    Field(
        tag = '520',
        indicators = ['#','#'],
        subfields = ['a', resumo]),
    Field(
        tag = '650',
        indicators = ['0','#'],
        subfields = ['a', assunto[0]]),
    Field(
        tag = '650',
        indicators = ['0','#'],
        subfields = ['a', assunto[1]]),
    Field(
        tag = '650',
        indicators = ['0','#'],
        subfields = ['a', assunto[2]]),
    Field(
        tag = '700',
        indicators = ['1','#'],
        subfields = [
            'a', orientador,
            'e', 'Orientador']),
    Field(
        tag = '856',
        indicators = ['#','#'],
        subfields = ['u', link]),
    Field(
        tag = '942',
        indicators = ['#','#'],
        subfields = ['c', tipo_code]))

if 'dc.contributor.advisor-co1' in metadados.keys():
    marc.add_field(
        Field(
            tag = '700',
            indicators = ['0','#'],
            subfields = ['a', coorientador, 'e', 'Coorientador']))
    
with open('marc.dat', 'wb') as tese:
    tese.write(marc.as_marc())


        


    



    
