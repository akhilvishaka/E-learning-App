from django.shortcuts import render

# Import necessary classes
from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic, Course, Student, Order
from django.http import Http404
from django.shortcuts import get_object_or_404,render,redirect, reverse
from .forms import  OrderForm, InterestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

@login_required
def myaccount(request):
    user = request.user
    try:
        student = Student.objects.get(username=user.username)
        first_name = student.first_name
        last_name= student.last_name
        ordered_courses = Order.objects.filter(student=student)
        topics_interested_in = student.interested_in.all()
        return render(request,'myapp/myaccount.html',{'first_name': first_name,
                                                      'last_name': last_name,
                                                      'ordered_courses':ordered_courses,
                                                      'topics_interested_in':topics_interested_in})
    except Exception:
        return HttpResponse("You are not a registered student!")


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
    return render(request, 'myapp/about.html')


def detail(request, top_no):
    try:
        topic = Topic.objects.get(id=top_no)
        topic_category = topic.category
        courses_of_topic = Course.objects.filter(topic_id=top_no)

    except Topic.DoesNotExist:
        raise Http404("Page not found(404)")

    heading1 = '<p>' + 'Category of ' + str(top_no) + ' is: ' + str(topic_category) + '</p>'

    heading2 = '<p>' + 'List of Courses for the topic: ' + str(topic.name) + '</p>'

    for course in courses_of_topic:
        para = '<p>' + str(course.id) + ': ' + str(course) + '</p>'
        return render(request, 'myapp/detail.html', {'topic': topic, 'topic_category': topic_category, 'courses_of_topic': courses_of_topic})

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    ''' courlist = Course.objects.all()
    return HttpResponse('You can place an order here.')
    '''
    msg = ''
    discount = 0
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
                if order.course.price > 150:
                    discount = order.course.discount()
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg, 'discount':discount})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})


def coursedetail(request, cour_id):
    course = get_object_or_404(Course, pk=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['interested'] == 1:
                course.interested += 1
            course.save()
            return redirect('myapp:index')
    elif request.method == 'GET':
        form = InterestForm()
        return render(request, 'myapp/coursedetail.html/', {'form': form, 'course': course})


'''def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of Topics: ' + '</p>'
    response.write(heading1)
    for topic in top_list:
        para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
        response.write(para)

    top_courses = Course.objects.all().order_by('-price')[:5]
    heading2 = '<p>' + 'List of top 5 Courses with highest to lowest price: ' + '</p>'
    response.write(heading2)
    for course in top_courses:
        if course.for_everyone == 1:
            addLine = str('This Course is For Everyone!')
            para1 = '<p>' + str(course.id) + ': ' + str(course) + ': ' + str(course.price) + ': ' + addLine + '</p>'
        else:
            addLine = str('This Course is Not For Everyone!')
            para1 = '<p>' + str(course.id) + ': ' + str(course) + ': ' + str(course.price) + ': ' + addLine + '</p>'
        response.write(para1)
    return response


def about(request):
    response = HttpResponse()
    response.writelines('This is an E-learning Website! Search our Topics to find all available Courses.')
    return response


def detail(request, top_no):
    response = HttpResponse()

# for displaying the category of topic and list of courses for that topic

    try:
        topic = Topic.objects.get(id=top_no)
        topic_category = topic.category
        courses_of_topic = Course.objects.filter(topic_id=top_no)
    except Topic.DoesNotExist:
        raise Http404("Page not found (404)")

    heading1 = '<p>' + 'Category of ' + str(top_no) + ' is ' + str(topic_category) + '</p>'
    response.write(heading1)

    heading2 = '<p>' + 'List of Courses for the topic: ' + str(topic.name) + '</p>'
    response.write(heading2)

    for course in courses_of_topic:
        para = '<p>' + str(course.id) + ': ' + str(course) + '</p>'
        response.write(para)
    return response
'''
