# Create your views here.
# coding=utf-8
import json
from time import gmtime
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.redirects.models import Redirect
from django.core.exceptions import FieldError, ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import loader, Context
from qsstats import QuerySetStats
from ask.models import Question, Answer, AnswerForm, QuestionForm, CommentQuest, CommentQForm, CommentAForm, CommentAns, LikeQuest, LikeAns, UserProfile, Tag

User.profile = property(lambda u : UserProfile.objects.get_or_create(user=u)[0])

def questions(request):
    object_list = Question.objects.all().order_by('-date')
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page_date')
    try:
        quest = paginator.page(page)
    except PageNotAnInteger:
        quest = paginator.page(1)
    except EmptyPage:
        quest = paginator.page(paginator.num_pages)
    object_rating = Question.objects.all().order_by('-rating')
    paginator_pop = Paginator(object_rating,10)
    page_pop = request.GET.get('page_popular')
    try:
        quest_pop = paginator_pop.page(page_pop)
    except PageNotAnInteger:
        quest_pop = paginator_pop.page(1)
    except EmptyPage:
         quest_pop = paginator_pop.page(paginator_pop.num_pages)
    new_users = User.objects.all().order_by('-date_joined')[0:10]
    tab = request.GET.get('tab')
    tags = Tag.objects.all();
    pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
    return render(request,'templates.html', {'date_list': quest , 'rating_list' : quest_pop , 'user_list' : new_users , 'page_date' : page , 'page_popular' : page_pop , 'tab' : tab , 'tags':tags , 'pop_tags' : pop_tags})

def look_answers(request):
    id = request.GET.get("id")
    err = ''
    try:
        answer = Answer.objects.all().filter(question_id = id).order_by("-date").order_by('-rating')
        quest = Question.objects.get(id=id)
        paginator = Paginator(answer, 10)
        page = request.GET.get('page')
        ans = paginator.page(page)
    except PageNotAnInteger:
        ans = paginator.page(1)
    except EmptyPage:
         ans = paginator.page(paginator.num_pages)
    except Answer.DoesNotExist:
        raise Http404
    except Question.DoesNotExist:
        raise Http404
    except ValueError:
        raise Http404
    if ans.object_list.__len__() == 0:
        err = 'У вопроса нет ответов'
    new_users = User.objects.all().order_by('-date_joined')[0:10]
    comment_q = CommentQuest.objects.order_by('-date').filter(main = quest.id)
    quest.counter = quest.counter + 1
    quest.save()
    pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
    return render(request,'template_q.html', {'answers': ans, 'question': quest,  'user_list' : new_users , 'page' : page , 'comments': comment_q, 'error': err , 'pop_tags' : pop_tags})

def user_info(request):
    try:
        ID = request.GET.get("id")
        user = User.objects.get(id=ID)
    except User.DoesNotExist:
        raise Http404
    except ValueError:
        raise Http404
    answers = Answer.objects.all().filter(author_id = ID)
    errAns = ''
    paginator = Paginator(answers, 10)
    page = request.GET.get('page_ans')
    try:
        ans = paginator.page(page)
    except PageNotAnInteger:
        ans = paginator.page(1)
    except EmptyPage:
        ans = paginator.page(paginator.num_pages)
    if ans.object_list.__len__() == 0:
            errAns= 'У пользователя нет ответов'
    quest = Question.objects.all().filter(author_id = ID)
    errQuest =''
    paginator_pop = Paginator(quest,10)
    page_pop = request.GET.get('page_quest')
    try:
        quest_pop = paginator_pop.page(page_pop)
    except PageNotAnInteger:
        quest_pop = paginator_pop.page(1)
    except EmptyPage:
         quest_pop = paginator_pop.page(paginator_pop.num_pages)
    if quest_pop.object_list.__len__() == 0:
        errQuest='У пользователя нет вопросов'
    new_users = User.objects.all().order_by('-date_joined')[0:10]
    tab=request.GET.get('tab')
    pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
    return render(request,'templates_u.html', {'answers': ans,'u': user, 'rating_list': quest_pop,   'user_list' : new_users, 'tab':tab , 'page_a':page, 'page_q' : page_pop , 'errAns':errAns , 'errQuest':errQuest , 'pop_tags': pop_tags })

def Quest_form(request):
    if request.user.is_authenticated() :
        if request.method == "POST":
            form = QuestionForm(request.POST,request.FILES)
            if form.is_valid():
                author = request.user
                title = form.cleaned_data['title']
                body = form.cleaned_data['body']
                try:
                    file = request.FILES['file']
                except:
                    file = None
                try:
                    q = Question.objects.create(title=title , body=body , rating=0 , author_id=author.id , date=datetime.datetime.now(), counter = 0, file=file )
                except UnicodeEncodeError:
                    u = User.objects.all().order_by('-date_joined')[0:10]
                    pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
                    c = {'error': 'ошибка в названии файла', 'user_list':u , 'pop_tags': pop_tags}
                    return render(request,'error.html',c)
                q.save()
                tags = request.POST.get("tags")
                if tags != '':
                    count = 0
                    for tag in tags.split(" "):
                        try:
                            t = Tag.objects.get(text=tag)
                        except:
                            t =  Tag.objects.create(text=tag)
                        count +=1
                        if count == 4 :
                            break;
                        q.tags.add(t)
                profile = author.profile
                profile.rating += 1
                profile.save()
                redir = request.META['HTTP_REFERER']
                return HttpResponseRedirect(redir)
            else:
                u = User.objects.all().order_by('-date_joined')[0:10]
                pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
                c = {'error': 'вы должны заполнить все поля', 'user_list':u , 'pop_tags': pop_tags }
                return render(request,'error.html',c)
        return HttpResponseRedirect('/index')
    else:
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        c = {'error': 'вы должны зайти от имени пользователя', 'user_list':u , 'pop_tags':pop_tags }
        return render(request,'error.html',c)

def Answer_form(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                author = form.cleaned_data['author']
                id = form.cleaned_data['question']
                body = form.cleaned_data['body']
                q = Answer.objects.create( body=body , rating=0 , author_id=author.id , question_id = id.id,  date=datetime.datetime.now() , correct = 0)
                q.save()
                redir = request.META['HTTP_REFERER']
                return HttpResponseRedirect(redir)
            else:
                u = User.objects.all().order_by('-date_joined')[0:10]
                pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
                c = {'error': 'вы должны заполнить все поля' , 'user_list' : u, 'pop_tags':pop_tags}
                return render(request,'error.html',c)
        return HttpResponseRedirect('/index')
    else:
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        c = {'error': 'вы должны зайти от имени пользователя', 'user_list':u , 'pop_tags' : pop_tags }
        return render(request,'error.html',c)

def make_correct(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            ID = request.POST.get("id")
            try:
                ans = Answer.objects.get(id=ID)
                if ans.correct==1:
                    ans.correct=0
                else:
                    ans.correct=1
                ans.save()
                if ans.correct == 1:
                    response_data = {'type' : ans.correct,'msg' : 'Ответ был помечен как правильный' }
                else:
                    response_data = {
                        'type' : ans.correct,
                        'msg' : "Ответ был помечен как неправильный"
                    }
            except ValueError:
                 response_data = { 'error': "Некорретный ответ" }
                 return HttpResponse(json.dumps(response_data), content_type="application/json")
            except Answer.DoesNotExist:
                 response_data = { 'error': "Ответ не найден" }
                 return HttpResponse(json.dumps(response_data), content_type="application/json")
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        return HttpResponseRedirect("/index")
    else:
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        c = {'error': 'вы должны зайти от имени пользователя', 'user_list':u , 'pop_tags':pop_tags }
        return render(request,'error.html',c)

def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        auto_login = request.POST.get('auto_login')
        if username == '' or password == '' or email == '':
            error = 'вы должны заполнить все поля'
            u = User.objects.all().order_by('-date_joined')[0:10]
            pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
            return render(request,'error.html',{'error':error , 'user_list' : u , 'pop_tags': pop_tags})
        try:
            u = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            u = User.objects.create_user( username=username , password=password , email = email)
            u.save()
            profile = UserProfile.objects.create(user = u , rating = 0)
            profile.save()
            if auto_login == 'on':
               login_view(request)
            return HttpResponseRedirect('index')
        error = 'пользователь уже существует, выберите другой никнейм'
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        return render(request,'error.html',{'error':error , 'user_list' : u , 'pop_tags':pop_tags})
    return HttpResponseRedirect("/index")

def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    last_users = User.objects.all().order_by('-date_joined')[0:10]
    pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
    if user is not None:
        if user.is_active:
            login(request,user)
            return HttpResponseRedirect('index')
        else:
            c={'error' : 'отключенный аккаунт', 'user_list': last_users, 'pop_tags':pop_tags}
            return render(request,'error.html', c)
    else:
        c={'error' : 'неправильные имя или пароль','user_list': last_users , 'pop_tags':pop_tags}
        return render(request,'error.html', c)


def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        redir = request.META['HTTP_REFERER']
        return HttpResponseRedirect(redir)
    else:
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        c = {'error': 'вы должны зайти от имени пользователя', 'user_list':u , 'pop_tags':pop_tags }
        return render(request,'error.html',c)

def change(request):
    if request.user.is_authenticated():
        if request.method=="POST":
            ID = request.POST.get('id')
            try:
                u = User.objects.get(id=ID)
            except ValueError:
                raise Http404
            except User.DoesNotExist:
                raise Http404
            username = request.POST.get('username')
            email = request.POST.get('email')
            firstname = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            if username == '':
                error = 'вы должны заполнить поле никнейма'
                u = User.objects.all().order_by('-date_joined')[0:10]
                pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
                return render(request,'error.html',{'error':error , 'user_list':u , 'pop_tags':pop_tags})
            try:
                u2 = User.objects.get_by_natural_key(username)
            except User.DoesNotExist:
                u.username = username
                u.email = email
                u.first_name = firstname
                u.last_name = last_name
                u.save()
                redir = request.META['HTTP_REFERER']
                return HttpResponseRedirect(redir)
            if u == u2:
                u.username = username
                u.email = email
                u.first_name = firstname
                u.last_name = last_name
                u.save()
                redir = request.META['HTTP_REFERER']
                return HttpResponseRedirect(redir)
            error = 'пользователь уже существует, измените никнейм'
            u = User.objects.all().order_by('-date_joined')[0:10]
            pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
            return render(request,'error.html',{'error':error , 'user_list': u , 'pop_tags':pop_tags})
        return HttpResponseRedirect("/index")
    else:
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        c = {'error': 'вы должны зайти от имени пользователя', 'user_list':u , 'pop_tags': pop_tags }
        return render(request,'error.html',c)

def search(request):
    query = request.GET.get('query')
    type = request.GET.get('type')
    if query == '':
        redir = request.META['HTTP_REFERER']
        return HttpResponseRedirect(redir)
    last_users = User.objects.order_by('-date_joined')[0:10]
    pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
    if type == 'answers':
         results = Answer.search.query(query).order_by('@weight')
    else:
        if type == 'questions':
             results = Question.search.query(query).order_by('@weight')
        else:
            if type == 'tags':
             results = Question.objects.all().filter(tags__text = query)
            else:
                return render(request,'error.html', {'error':'неизвестный тип поиска' , 'user_list': last_users , 'pop_tags': pop_tags})
    paginator = Paginator(results, 10)
    page = request.GET.get('page')
    err=''
    if paginator.object_list.__len__() == 0 :
        err='Пустой поиск'
    try:
        result_pag = paginator.page(page)
    except PageNotAnInteger:
        result_pag = paginator.page(1)
    except EmptyPage:
        result_pag = paginator.page(paginator.num_pages)
    return render(request,'search.html',{'s_result': result_pag , 'tab':type , 'user_list': last_users, 'query':query ,'error':err, 'pop_tags':pop_tags})

def comment_q(request):
    if request.user.is_authenticated():
         if request.method == "POST":
            form = CommentQForm(request.POST)
            if form.is_valid():
                author = form.cleaned_data['author']
                id = form.cleaned_data['main']
                body = form.cleaned_data['body']
                tab=request.POST.get("tab")
                comment = CommentQuest.objects.create( body=body , author=author , main = id,  date=datetime.datetime.now())
                comment.save()
                redir = request.META['HTTP_REFERER']
                return HttpResponseRedirect(redir)
            else:
                u = User.objects.all().order_by('-date_joined')[0:10]
                pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
                c = {'error': 'вы должны заполнить все поля' , 'user_list' : u , 'pop_tags':pop_tags}
                return render(request,'error.html',c)
         return HttpResponseRedirect('/index')
    else:
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        c = {'error': 'вы должны зайти от имени пользователя', 'user_list':u , 'pop_tags':pop_tags }
        return render(request,'error.html',c)

def comment_a(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = CommentAForm(request.POST)
            if form.is_valid():
                author = form.cleaned_data['author']
                tab=request.POST.get("tab")
                id = form.cleaned_data['main']
                body = form.cleaned_data['body']
                comment = CommentAns.objects.create( body=body , author=author , main = id,  date=datetime.datetime.now())
                comment.save()
                redir = request.META['HTTP_REFERER']
                return HttpResponseRedirect(redir)
            else:
                u = User.objects.all().order_by('-date_joined')[0:10]
                pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
                c = {'error': 'вы должны заполнить все поля' , 'user_list' : u , 'pop_tags':pop_tags}
                return render(request,'error.html',c)
        return HttpResponseRedirect('/index')
    else:
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        c = {'error': 'вы должны зайти от имени пользователя', 'user_list':u , 'pop_tags':pop_tags }
        return render(request,'error.html',c)

def rating(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            id = request.POST.get('id')
            type = request.POST.get('type')
            on = request.POST.get('on')

            if on == 'question':
                try:
                    question = Question.objects.get(id=id)
                    profile = question.author.profile
                except ValueError:
                    response_data = { 'error': "Некорретный тип голосования" }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                except Question.DoesNotExist:
                    response_data = { 'error': "Не найден вопрос" }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")

                try:
                    like=LikeQuest.objects.get(author = request.user.id , main = question.id)
                    if type == 'up':
                        if like.type == True:
                            response_data = { 'error': "Вы уже проголосовали так" }
                            return HttpResponse(json.dumps(response_data), content_type="application/json")
                        if like.type == False:
                            question.rating += 2
                            like.type = True
                            like.save()
                            profile.rating += 5
                    if type == 'down':
                        if like.type == False:
                            response_data = { 'error': "Вы уже проголосовали так" }
                            return HttpResponse(json.dumps(response_data), content_type="application/json")
                        else:
                            question.rating -= 2
                            like.type = False
                            like.save()
                            profile.rating -= 5
                except LikeQuest.DoesNotExist:
                    if type == 'up':
                        question.rating +=1
                        likeC = LikeQuest.objects.create(author = request.user , main = question , type = True)
                        likeC.save()
                        profile.rating += 3
                    if type == 'down':
                        question.rating -=1
                        likeC = LikeQuest.objects.create(author = request.user , main = question , type = False)
                        likeC.save()
                        profile.rating -= 2
                question.save()
                profile.save()
                response_data = {
                                    'msg': 'Ваш голос принят',
                                    'rating': question.rating
                                }
            elif on == 'answer':
                try:
                    answer = Answer.objects.get(id=id)
                    profile = answer.author.profile
                except ValueError:
                    response_data = { 'error': "Некорретный тип голосования" }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                except Answer.DoesNotExist:
                    response_data = { 'error': "Нет такого ответа" }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                try:
                    like=LikeAns.objects.get(author = request.user.id , main = answer.id)
                    if type == 'up':
                        if like.type == True:
                            response_data = { 'error': "Вы уже так проголосовали" }
                            return HttpResponse(json.dumps(response_data), content_type="application/json")
                        if like.type == False:
                            answer.rating += 2
                            like.type = True
                            profile.rating += 7
                    if type == 'down':
                        if like.type == False:
                            response_data = { 'error': "Вы уже так проголосовали" }
                            return HttpResponse(json.dumps(response_data), content_type="application/json")
                        if like.type == True:
                            answer.rating -= 2
                            like.type = False
                            profile.rating -= 7
                    like.save()
                except LikeAns.DoesNotExist:
                    if type == 'up':
                        answer.rating +=1
                        likeC = LikeAns.objects.create(author = request.user , main = answer , type = True)
                        likeC.save()
                        profile.rating += 5
                    if type == 'down':
                        answer.rating -=1
                        likeC = LikeAns.objects.create(author = request.user , main = answer , type = False)
                        likeC.save()
                        profile.rating -= 2
                answer.save()
                profile.save()
                response_data = {
                                'msg': 'Ваш голос принят',
                                'rating': answer.rating
                            }
            else:
                response_data = { 'error': "Неправильный тип голосования" }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        return HttpResponseRedirect('/index')
    else:
        u = User.objects.all().order_by('-date_joined')[0:10]
        pop_tags = Tag.objects.all().annotate(questions_count=Count('question')).order_by('-questions_count')[:10]
        c = {'error': 'вы должны зайти от имени пользователя', 'user_list':u , 'pop_tags':pop_tags }
        return render(request,'error.html',c)

def graph(request):
    start = datetime.datetime(2013, 11, 21, 00, 00).date()
    end = datetime.datetime.now().date()
    users = User.objects.all()
    qsstats = QuerySetStats(users, date_field='last_login', aggregate=Count('id'))
    values = qsstats.time_series(start , end , interval='days' )

    staff = User.objects.all().filter(is_staff = '1').count()
    other = User.objects.all().count() - staff
    type_of_user = [['Суперпользователи',staff],['Пользователи',other]]
    start = datetime.datetime(2013, 12, 3, 00, 00).date()
    answer = Answer.objects.all()
    qsstats2 = QuerySetStats(answer, date_field='date', aggregate=Count('id'))
    ans = qsstats2.time_series(start,end, interval="days")
    return render(request,'graph.html', { 'ans':ans , 'users': values , 'type' : type_of_user })


def dynamic_graph(request):
    quest = Question.objects.all().count()
    ans = Answer.objects.all().count()
    commentA = CommentAns.objects.all().count()
    commentQ = CommentQuest.objects.all().count()

    response_data = {
        'quest':quest,
        'ans': ans,
        'commentA': commentA,
        'commentQ': commentQ
    }

    return HttpResponse(json.dumps(response_data), content_type='application/json')