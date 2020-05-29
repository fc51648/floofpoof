from django.shortcuts import render
from login.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from django.db import transaction
from django.db import IntegrityError
from login.models import User, Group, Subject, Task, Meeting, Feedback, Score, Degree

@transaction.atomic
def upload_years(request):
    context = {}
    context['subtext'] = 'anos letivos'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: NOME;DATADEINICIO;DATADEFIM\nExemplo:"2020-2021;2020-09-15;2021-07-15"'
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            with open(os.path.join(settings.MEDIA_ROOT, myfile.name), 'r') as f:
                myfile = File(f)
                for line in myfile.readlines():
                    line = line.split(';')
                    year = Year(name=line[0],beginning=line[1], end=line[2])
                    year.save()
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)
        except IntegrityError:
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)
            context['data_saved'] = 'Erro ao inserir os dados. Existem dados redundantes ou com parâmetros errados no ficheiro.'
            return render(request, 'upload_data/upload-data.html', context)

        except:
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)
            context['data_saved'] = 'Uma das linhas do ficheiro tem a estrutura dos parâmetros errada.'
            return render(request, 'upload_data/upload-data.html', context)


        context['data_saved'] = 'Dados de anos letivos guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)

@transaction.atomic
def upload_degrees(request):
    context = {}
    context['subtext'] = 'cursos'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: NOME;CICLO;ANOSDECURSO\nExemplo:"Tecnologias de Informação;1;3"'
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            with open(os.path.join(settings.MEDIA_ROOT, myfile.name), 'r') as f:
                myfile = File(f)
                for line in myfile.readlines():
                    line = line.split(';')
                    degree = Degree(name=line[0],grade=int(line[1]),years=int(line[2]))
                    degree.save()

            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)

        except IntegrityError:
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)

            context['data_saved'] = 'Erro ao inserir os dados. Existem dados redundantes com a base de dados no ficheiro.'
            return render(request, 'upload_data/upload-data.html', context)

        except:
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)

            context['data_saved'] = 'Uma das linhas do ficheiro tem a estrutura dos parâmetros errada.'
            return render(request, 'upload_data/upload-data.html', context)

        context['data_saved'] = 'Dados de cursos guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)


@transaction.atomic
def upload_subjects(request):
    context = {}
    context['subtext'] = 'cadeiras'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: NOME;CODIGO;MAXELEMENTOSPORGRUPO;PRAZOFORMARGRUPO;GRUPOSABERTOS;CURSO;ANOLETIVO\nExemplo:"Programação 1;PRO1;4;2020-09-30;True;IT;2020-2021"'
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            with open(os.path.join(settings.MEDIA_ROOT, myfile.name), 'r') as f:
                myfile = File(f)
                for line in myfile.readlines():
                    line = line.split(';')
                    Code = str(line[5])
                    Yearname = str(line[6])
                    print(Yearname)
                    s = Subject(name=line[0],code=line[1],groups_max=int(line[2]),groups_deadline=line[3],groups_on=line[4],degree=Degree.objects.get(code=Code),year=Year.objects.get(name=Yearname))
                    s.save()

            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)

        
        except IntegrityError:
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)


            context['data_saved'] = 'Erro ao inserir os dados. Existem dados redundantes com a base de dados no ficheiro.'
            return render(request, 'upload_data/upload-data.html', context)
        
        except:
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)

            context['data_saved'] = 'Uma das linhas do ficheiro tem a estrutura dos parâmetros errada.'
            return render(request, 'upload_data/upload-data.html', context)

        context['data_saved'] = 'Dados de cadeiras guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)




@transaction.atomic
def upload_blocks(request):
    context = {}
    context['subtext'] = 'turnos'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: CODIGOCADEIRA;DIADASEMANA;HORAINICIO;HORAFIM;SALA\nExemplo: "PRO1;2;09:30:00;10:30:00;C.2.23"'
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            with open(os.path.join(settings.MEDIA_ROOT, myfile.name), 'r') as f:
                myfile = File(f)
                for line in myfile.readlines():
                    line = line.split(';')
                    Code = str(line[0])
                    s = Block(subject=Subject.objects.get(code=Code),day=int(line[1]),From=line[2],To=line[3],room=line[4])
                    s.save()

            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)

        
        except IntegrityError:
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)


            context['data_saved'] = 'Erro ao inserir os dados. Existem dados redundantes com a base de dados no ficheiro.'
            return render(request, 'upload_data/upload-data.html', context)
        
        except:
            file_path = os.path.join(settings.MEDIA_ROOT, myfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)

            context['data_saved'] = 'Uma das linhas do ficheiro tem a estrutura dos parâmetros errada.'
            return render(request, 'upload_data/upload-data.html', context)
        
        context['data_saved'] = 'Dados de turnos guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)








def upload_area(request):
    return render(request, 'upload_data/upload-area.html')