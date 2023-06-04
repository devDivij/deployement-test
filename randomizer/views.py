from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Decision, Option, ImageSet, Category, Vote
from .forms import DecisionForm
import random
from django.urls import reverse
from django.db.models import Q
import time

def home(request):
    if request.user.is_authenticated:
        decisions = Decision.objects.filter(Q(user=request.user) & Q(is_daily_decision=True))
        context = {'decisions': decisions}
    else:
        context = {}
    return render(request, 'randomizer/home.html', context) 
# end def

def filter_decisions(request):
    category_ids = request.GET.getlist('category')
    categories = Category.objects.all()
    filtered_decisions = Decision.objects.filter(categories__in=category_ids).distinct()
    context = {
        'decisions': filtered_decisions,
        'categories': categories,
        'selected_categories': category_ids,
    }
    return render(request, 'randomizer/filter_decisions.html', context)
# end def

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    decisions = user.decision_set.all()
    context = {}
    return render(request, 'randomizer/profile.html', context)    
# end def

def capitalize_transform_text(text):
    words = text.split()
    for i, word in enumerate(words):
        if i == 0 or word == 'i':
            words[i] = word.capitalize()
    #   # to small case the text
    #     elif word.isalpha():
    #         words[i] = word.lower()
    return ' '.join(words)
# end def

def quickDecision(request, pk):

    decision = Decision.objects.get(id=pk)
    image_set = decision.image_set
    options = decision.option_set.all()

    if request.method == 'POST':
        # check if the button to toggle daily decision was clicked
        if 'toggle_daily_decision' in request.POST:
            decision.is_daily_decision = not decision.is_daily_decision
            decision.save()
        else:
            # check if option count is less than 4 before adding new option
            if options.count() < 4:
                option = Option.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    decision=decision,
                    content=capitalize_transform_text(request.POST.get('content')),
                )
                # messages.success(request, 'Option added successfully.')
            else:
                messages.error(request, 'Cannot add more than 4 options.')
            return redirect('decision', pk=decision.id)

    context = {'decision': decision, 'options': options}
    return render(request, 'randomizer/quick_decision.html', context)
# end def

def createQuickDecision(request):
    if request.method == 'POST':
        form = DecisionForm(request.POST)
        if form.is_valid():
            decision = form.save(commit=False)
            decision.user = request.user if request.user.is_authenticated else None
            
            if decision.title:
                decision.title = capitalize_transform_text(decision.title)
            else:
                decision.title = str('Untitled Decision')
            
            image_sets = ImageSet.objects.all()
            decision.image_set = mega_random(image_sets) or None
            decision.is_quick_decision = True

            decision.save()

            messages.success(request, 'Decision created successfully!')
            return redirect('quick-decision', pk=decision.pk)
    else:
        form = DecisionForm()

    context = {'form': form}
    return render(request, 'randomizer/quick_create_decision.html', context)
# end def

@login_required(login_url='login')
def updateQuickDecision(request, pk):
    decision = Decision.objects.get(id=pk)

    if decision.is_quick_decision == True:

        if request.user != decision.user:
            messages.error(request, 'You are not allowed here!')
            return redirect('home')

        if request.method == 'POST':
            form = DecisionForm(request.POST, instance=decision)
            if form.is_valid():
                decision = form.save(commit=False)
                decision.title = capitalize_transform_text(decision.title)
                decision.is_quick_decision = True

                decision.save()

                messages.success(request, 'Decision updated successfully!')
                return redirect('decision', pk=decision.id)

            messages.error(request, 'Please correct the errors below.')
        else:
            form = DecisionForm(instance=decision)
    else:
        return redirect('updatePublicDecision')

    context = {'form': form, 'decision': decision}
    return render(request, 'randomizer/quick_update_decision.html', context)
# end def

def publicDecision(request, pk):

    decision = Decision.objects.get(id=pk)
    image_set = decision.image_set
    options = decision.option_set.all()
    situation = decision.situation
    categories = Category.objects.all()

    if request.method == 'POST':
        if 'toggle_daily_decision' in request.POST:
            decision.is_daily_decision = not decision.is_daily_decision
            decision.save()
        elif 'select_categories' in request.POST:
            selected_categories = request.POST.getlist('categories', [])
            decision.categories.set(selected_categories)
        else:
            if options.count() < 4:
                option = Option.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    decision=decision,
                    content=capitalize_transform_text(request.POST.get('content')),
                )
                # messages.success(request, 'Option added successfully.')
            else:
                messages.error(request, 'Cannot add more than 4 options.')
            return redirect('public-decision', pk=decision.id)

    context = {
        'decision': decision,
        'image_set': image_set,
        'options': options,
        'situation': situation,
        'categories': categories,
    }
    return render(request, 'randomizer/quick_decision.html', context)
# end def

@login_required(login_url='login')
def createPublicDecision(request):
    decision = Decision.objects.create(user=request.user)
    decision.is_public_decision = True
    decision.is_quick_decision = False
    decision.is_daily_decision = False
    decision.title = ''
    decision.situation = ''
    decision.save()
    return redirect(updatePublicDecision, pk=decision.id)
# end def

@login_required(login_url='login')
def updatePublicDecision(request, pk):
    decision = Decision.objects.get(id=pk)

    if request.user != decision.user:
        messages.error(request, 'You are not allowed here!')
        return redirect('home')

    if request.method == 'POST':
        form = DecisionForm(request.POST, instance=decision)
        if form.is_valid():
            decision = form.save(commit=False)

            if decision.title:
                decision.title = capitalize_transform_text(decision.title)
            else:
                decision.title = str('Untitled Decision')

            decision.is_public_decision = True

            decision.situation = form.cleaned_data['situation']

            selected_categories = form.cleaned_data['categories']
            decision.categories.set(selected_categories)

            decision.save()

            # Handle preferred option selection
            preferred_option_id = request.POST.get('preferred_option')
            if preferred_option_id:
                decision.option_set.update(is_preferred=False)  # Reset all options to not preferred
                preferred_option = decision.option_set.get(id=preferred_option_id)
                preferred_option.is_preferred = True
                preferred_option.save()

            messages.success(request, 'Decision updated successfully!')
            return redirect('public-decision', pk=decision.id)

        messages.error(request, 'Please correct the errors below.')
    else:
        form = DecisionForm(instance=decision)

    context = {'form': form, 'decision': decision}
    return render(request, 'randomizer/public_update_decision.html', context)
# end def

@login_required(login_url='login')
def deleteDecision(request, pk):
    decision = Decision.objects.get(id=pk)

    if request.user != decision.user:
        # Add a warning message
        messages.warning(request, 'You are not allowed to delete this decision!')
        return redirect('home')
    
    if request.method == 'POST':
        decision.delete()

        # Add a success message
        messages.success(request, 'Decision deleted successfully!')
        
        return redirect('home')
    
    return render(request, 'randomizer/delete.html', {'obj': decision})
# end def

@login_required(login_url='login')
def deleteOption(request, pk):
    option = Option.objects.get(id=pk)

    if request.user != option.user:
        return HttpResponse('You are not allowed here!')

    option.delete()
    return redirect('decision', pk=option.decision.id)    
# end def

def mega_random(objects):

    if objects:
        # Returns a 'mega random' value based on 10 randomizations of the given objects.
        random_values = []
        for i in range(64):
            random_values.append(random.choice(objects))

        mega_random_value = random.choice(random_values)

        return mega_random_value
    return None
# end def

def randomOption(request, pk):
    decision = Decision.objects.get(id=pk)
    options = decision.option_set.all()
    random_option = mega_random(options)
    random_option_text = random_option.content
    random_option_text = random_option_transform_text(random_option_text)
    context = {'decision': decision, 'random_option': random_option_text}
    return render(request, 'randomizer/random_option.html', context)
# end def

def random_option_transform_text(text):
    words = text.split()
    for i, word in enumerate(words):
        if word.lower() == 'i':
            words[i] = 'you'
        elif word.lower() == 'my':
            words[i] = 'your'
        elif word.lower() == 'mine':
            words[i] = 'yours'
        elif word.lower() == 'me':
            words[i] = 'you'
    return ' '.join(words).capitalize()

def daily_decisions(request):
    decisions = Decision.objects.filter(Q(user=request.user if request.user.is_authenticated else None) & Q(is_daily_decision=True))
    context = {'decisions': decisions}
    return render(request, 'randomizer/daily_decisions.html', context)
# end def

@login_required(login_url='login')
def set_daily_decision(request, pk):
    decision = Decision.objects.get(id=pk)
    decision.is_daily_decision = True
    decision.save()

    # Add a success message
    messages.success(request, 'Decision set as daily decision!')

    return redirect('quick-decision', pk=decision.id)
# end def

@login_required(login_url='login')
def unset_daily_decision(request, pk):
    decision = Decision.objects.get(id=pk)
    decision.is_daily_decision = False
    decision.save()

    # Add a success message
    messages.success(request, 'Decision unset as daily decision!')

    return redirect('decision', pk=decision.id)
# end def

def vote_option(request, pk):
    decision = Decision.objects.get(id=pk)
    options = decision.option_set.all()

    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = Option.objects.get(id=option_id)

        message = request.POST.get('message')
        pros = request.POST.get('pros')
        cons = request.POST.get('cons')

        vote = Vote(option=option, voted_by=request.user, message=message, pros=pros, cons=cons)
        vote.save()

        return redirect('decision', pk=decision.id)
    
    context = {'decision': decision, 'options': options}
    return render(request, 'randomizer/vote_option.html', context)
# end def

def filter_option_messages(request, pk, option_id):
    decision = Decision.objects.get(id=pk)
    option = Option.objects.get(id=option_id)

    messages = Vote.objects.filter(option=option)
    pros = [vote.pros for vote in messages if vote.pros]
    cons = [vote.cons for vote in messages if vote.cons]

    context = {
        'decision': decision,
        'option': option,
        'messages': messages,
        'pros': pros,
        'cons': cons,
    }
    return render(request, 'randomizer/filter_option_messages.html', context)