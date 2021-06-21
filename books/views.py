from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import Education, Work, Projects, Profile, Preference, SampleLink
from users.forms import EducationForm, WorkForm, ProjectForm, ProfileForm, PreferenceForm, SampleLinkForm
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def resume_list(request):
    educations = Education.objects.filter(user=request.user).order_by('-id')
    works=Work.objects.filter(users=request.user).order_by('-id')
    projects=Projects.objects.filter(user=request.user).order_by('-id')
    profiles=Profile.objects.filter(user=request.user).order_by('-id')
    preferences=Preference.objects.filter(user=request.user)
    links=SampleLink.objects.filter(user=request.user)

    context={
        'educations':educations,
        'works':works,
        'projects':projects,
        'profiles':profiles,
        'preferences':preferences,
        'links':links
    }
    return render(request, 'books/education_list.html',context)


########################################################################################################################################


#EDUCATION
@login_required    
def save_education_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            data['form_is_valid'] = True
            educations = Education.objects.filter(user=request.user).order_by('-id')
            data['html_book_list'] = render_to_string('books/includes/partial_education_list.html', {
                'educations': educations
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def education_create(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
    else:
        form = EducationForm()
    return save_education_form(request, form, 'books/includes/partial_education_create.html')

@login_required
def education_update(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
    else:
        form = EducationForm(instance=education)
    return save_education_form(request, form, 'books/includes/partial_education_update.html')

@login_required    
def education_delete(request, pk):
    education = get_object_or_404(Education, pk=pk)
    data = dict()
    if request.method == 'POST':
        education.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        educations = Education.objects.filter(user=request.user)
        data['html_book_list'] = render_to_string('books/includes/partial_education_list.html', {
            'educations': educations
        })
    else:
        context = {'education': education}
        data['html_form'] = render_to_string('books/includes/partial_education_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)


########################################################################################################################################3

#Work


@login_required    
def save_work_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.instance.users=request.user
            form.save()
            data['form_is_valid'] = True
            works = Work.objects.filter(users=request.user).order_by('-id')
            data['html_work_list'] = render_to_string('books/work/partial_work_list.html', {
                'works': works
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def work_create(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
    else:
        form = WorkForm()
    return save_work_form(request, form, 'books/work/partial_work_create.html')

@login_required
def work_update(request, pk):
    works = get_object_or_404(Work, pk=pk)
    if request.method == 'POST':
        form = WorkForm(request.POST, instance=works)
    else:
        form = WorkForm(instance=works)
    return save_work_form(request, form, 'books/work/partial_work_update.html')

@login_required    
def work_delete(request, pk):
    work = get_object_or_404(Work, pk=pk)
    data = dict()
    if request.method == 'POST':
        work.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        works = Work.objects.filter(users=request.user)
        data['html_work_list'] = render_to_string('books/work/partial_work_list.html', {
            'works': works
        })
    else:
        context = {'work': work}
        data['html_form'] = render_to_string('books/work/partial_work_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)



########################################################################################################################################


#Portfolio Projects


def save_project_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            data['form_is_valid'] = True
            projects = Projects.objects.filter(user=request.user).order_by('-id')
            data['html_project_list'] = render_to_string('books/project/partial_project_list.html', {
                'projects': projects
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
    else:
        form = ProjectForm()
    return save_project_form(request, form, 'books/project/partial_project_create.html')


@login_required
def project_update(request, pk):
    projects = get_object_or_404(Projects, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES,instance=projects)
    else:
        form = ProjectForm(instance=projects)
    return save_project_form(request, form, 'books/project/partial_project_update.html')


@login_required    
def project_delete(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    data = dict()
    if request.method == 'POST':
        project.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        projects = Projects.objects.filter(user=request.user)
        data['html_project_list'] = render_to_string('books/project/partial_project_list.html', {
            'projects': projects
        })
    else:
        context = {'project': project}
        data['html_form'] = render_to_string('books/project/partial_project_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)




########################################################################################################################################


#Profile

def save_profile_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            data['form_is_valid'] = True
            profiles = Profile.objects.filter(user=request.user).order_by('-id')
            data['html_profile_list'] = render_to_string('books/profile/partial_profile_list.html', {
                'profiles': profiles
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
    else:
        form = ProfileForm()
    return save_profile_form(request, form, 'books/profile/partial_profile_create.html')

@login_required
def profile_update(request, pk):
    profiles = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profiles)
    else:
        form = ProfileForm(instance=profiles)
    return save_profile_form(request, form, 'books/profile/partial_profile_update.html')

@login_required    
def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    data = dict()
    if request.method == 'POST':
        profile.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        profiles = Profile.objects.filter(user=request.user)
        data['html_profile_list'] = render_to_string('books/profile/partial_profile_list.html', {
            'profiles': profiles
        })
    else:
        context = {'profile': profile}
        data['html_form'] = render_to_string('books/profile/partial_profile_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)





######################################################################################################



#Preference
def save_preference_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            #form.save_m2m()
            data['form_is_valid'] = True
            preferences = Preference.objects.filter(user=request.user)
            data['html_preference_list'] = render_to_string('books/preference/partial_preference_list.html', {
                'preferences': preferences
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def preference_create(request):
    
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
    else:
        form = PreferenceForm()
    return save_preference_form(request, form, 'books/preference/partial_preference_create.html')

@login_required
def preference_update(request, pk):
    preferences = get_object_or_404(Preference, pk=pk)
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=preferences)
    else:
        form = PreferenceForm(instance=preferences)
    return save_preference_form(request, form, 'books/preference/partial_preference_update.html')

@login_required    
def preference_delete(request, pk):
    preference = get_object_or_404(Preference, pk=pk)
    data = dict()
    if request.method == 'POST':
        preference.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        preferences = Preference.objects.filter(user=request.user)
        data['html_preference_list'] = render_to_string('books/preference/partial_preference_list.html', {
            'preferences': preferences
        })
    else:
        context = {'preference': preference}
        data['html_form'] = render_to_string('books/preference/partial_preference_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)









######################################################################################################



#SampleLinks

def save_link_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            #form.save_m2m()
            data['form_is_valid'] = True
            links = SampleLink.objects.filter(user=request.user)
            data['html_link_list'] = render_to_string('books/link/partial_link_list.html', {
                'links': links
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def link_create(request):
    
    if request.method == 'POST':
        form = SampleLinkForm(request.POST)
    else:
        form = SampleLinkForm()
    return save_link_form(request, form, 'books/link/partial_link_create.html')

@login_required
def link_update(request, pk):
    links = get_object_or_404(SampleLink, pk=pk)
    if request.method == 'POST':
        form = SampleLinkForm(request.POST, instance=links)
    else:
        form = SampleLinkForm(instance=links)
    return save_link_form(request, form, 'books/link/partial_link_update.html')

@login_required    
def link_delete(request, pk):
    link = get_object_or_404(SampleLink, pk=pk)
    data = dict()
    if request.method == 'POST':
        link.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        links = SampleLink.objects.filter(user=request.user)
        data['html_link_list'] = render_to_string('books/link/partial_link_list.html', {
            'links': links
        })
    else:
        context = {'link': link}
        data['html_form'] = render_to_string('books/link/partial_link_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
