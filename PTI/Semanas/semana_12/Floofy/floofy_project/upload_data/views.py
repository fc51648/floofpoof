from django.shortcuts import render
from login.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from django.db import transaction
from django.db import IntegrityError
from login.models import User, Group, Subject, Task, Meeting, Feedback, Score, Degree
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_admin





@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
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

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
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

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
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
                    Yearname = str(line[6]).strip()
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



@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
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
                    s = Block(subject=Subject.objects.get(code=Code),day=int(line[1]),From=line[2],To=line[3],room=line[4].strip())
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



@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
@transaction.atomic
def upload_students(request):
    context = {}
    context['subtext'] = 'alunos'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: EMAIL;PASSWORD;DATANASCIMENTO;CADEIRAS;TURNOS;CURSOS;PRIMEIRONOME;ULTIMONOME\nExemplo: "andre@gmail.com;FculPass999;1998-07-07;PRO1-ASTI;1-2-3;IT-IT2;Andre;Mota"'
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
                    student = User(email=line[0],date_of_birth=line[2],firstname=line[6],surname=line[7].strip())
                    student.set_password(line[1])
                    student.save()
                    subjects = line[3].split("-")
                    for sub in subjects:
                        s = Subject.objects.get(code=sub)
                        student.subjects.add(s)
                    blocks = line[4].split("-")
                    for sub in blocks:
                        s = Block.objects.get(pk=sub)
                        student.blocks.add(s)
                    degrees = line[5].split("-")
                    for sub in degrees:
                        s = Degree.objects.get(code=sub)
                        student.degree.add(s)
                    student.is_active = True
                    student.is_admin = False
                    student.is_teacher = False
                    student.is_student = True
                    student.save()


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
        
        context['data_saved'] = 'Dados de alunos guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
@transaction.atomic
def upload_teachers(request):
    context = {}
    context['subtext'] = 'professores'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: EMAIL;PASSWORD;DATANASCIMENTO;CADEIRAS;TURNOS;CURSOS;PRIMEIRONOME;ULTIMONOME\nExemplo: "andre@gmail.com;FculPass999;1998-07-07;PRO1-ASTI;1-2-3;IT-IT2;Andre;Mota"'
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
                    student = User(email=line[0],date_of_birth=line[2],firstname=line[6],surname=line[7].strip())
                    student.set_password(line[1])
                    student.save()
                    subjects = line[3].split("-")
                    for sub in subjects:
                        s = Subject.objects.get(code=sub)
                        student.subjects.add(s)
                    blocks = line[4].split("-")
                    for sub in blocks:
                        s = Block.objects.get(pk=sub)
                        student.blocks.add(s)
                    degrees = line[5].split("-")
                    for sub in degrees:
                        s = Degree.objects.get(code=sub)
                        student.degree.add(s)
                    student.is_active = True
                    student.is_admin = False
                    student.is_teacher = True
                    student.is_student = False
                    student.save()


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
        
        context['data_saved'] = 'Dados de professores guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
@transaction.atomic
def upload_groups(request):
    context = {}
    context['subtext'] = 'grupos'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: CODIGOCADEIRA;MEMBROSDOGRUPO;NOME\nExemplo: "PRO1;1-2-3;Novogrupoteste"'
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
                    s = Group(subject=Subject.objects.get(code=Code),name=line[2].strip())
                    s.save()
                    for member in line[1].split("-"):
                        m = User.objects.get(pk=int(member))
                        s.members.add(m)
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
        
        context['data_saved'] = 'Dados de grupos guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
@transaction.atomic
def upload_tasks(request):
    context = {}
    context['subtext'] = 'tarefas'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: IDGRUPO;DONODATAREFA;NOME;DESCRIÇÃO;HORAS_DEDICADAS;MIN_DEDICADOS;PRAZO;CONCLUIDA\nExemplo: "1;2;TAREFAMA;MAMA;20;2;2020-08-09;True"'
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
                    gid = line[0]
                    oid = line[1]
                    o = User.objects.get(pk=oid)
                    s = Task(group=g,owner=o,name=line[2],description=line[3],hours_dedicated=int(line[4]),minutes_dedicated=int(line[5]),deadline=line[6],finished=line[7].strip())
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
        
        context['data_saved'] = 'Dados de tarefas guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)


@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
@transaction.atomic
def upload_stages(request):
    context = {}
    context['subtext'] = 'etapas'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: CODIGOCADEIRA;NUMERO;NOME;DESCRIÇÃO;PRAZO\nExemplo: "ASTI;99;ESTAGIO1;muitascoisasparafazer;2020-08-09"'
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
                    Code = line[0]
                    s = Subject.objects.get(code=Code)
                    stage = Stage(subject=s,number=int(line[1]),name=line[2],description=line[3],deadline=line[4])
                    stage.save()

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
        
        context['data_saved'] = 'Dados de etapas guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
@transaction.atomic
def upload_meetings(request):
    context = {}
    context['subtext'] = 'reuniões de grupo'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: IDGRUPO;IDOWNER;IDs_de_quem_vai;IDs_de_quem_não_vai;NOME;LOCAL;DESCRIÇÃO;DATA\nExemplo: "8;1;1-2-3;4;reuniaodeteste;Via zoom;temosquetrabalhar;2020-05-05"'
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
                    idg = str(line[0])
                    g = Group.objects.get(pk = idg)
                    ido = str(line[1])
                   
                    o = User.objects.get(pk = ido)
                    meet = Meeting(group=g,owner=o,name=line[4],location=line[5],description=line[6],date=line[7].strip())
                    meet.save()
                    for member in line[2].split("-"):
                        m = User.objects.get(pk=int(member))
                        meet.willgo.add(m)
                    
                    for member in line[3].split("-"):
                        
                        m = User.objects.get(pk=int(member))
                        meet.wontgo.add(m)
                    meet.save()

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
        
        context['data_saved'] = 'Dados de reuniões de grupos guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
@transaction.atomic
def upload_feedback(request):
    context = {}
    context['subtext'] = 'comentários e feedback de professores'
    context['guide'] = 'Envie um ficheiro do tipo .TXT ou .CSV\nEstrutura das linhas: IDGRUPO;IDOWNER;IDETAPA;DESCRIÇÃO\nExemplo: "8;2;3;Etapanova"'
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
                    idg = str(line[0])
                    g = Group.objects.get(pk = idg)
                    ido = str(line[1])
                    o = User.objects.get(pk = ido)
                    ids = str(line[2])
                    s = Stage.objects.get(pk = ids)
                    f = Feedback(group=g,owner=o,stage=s,description=line[3])
                    f.save()

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
        
        context['data_saved'] = 'Dados de feedback de professores guardados com sucesso!'
        return render(request, 'upload_data/upload-data.html', context)
    return render(request, 'upload_data/upload-data.html', context)

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
def upload_area(request):
    return render(request, 'upload_data/upload-area.html')