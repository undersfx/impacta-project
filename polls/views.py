from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice, QuestionForm


class IndexView(generic.ListView):
    """Renders index template for the queryset result."""
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """Renders details template for the question got from pk param."""
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    """Renders results template for the question got from pk param."""
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        context = {"question": question, "error_message": "You didn't select a choice."}
        return render(request,"polls/detail.html", context)
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def create(request):
    if request.method == "POST":
        question_text = request.POST.get('questionText')
        choices = request.POST.getlist('choices[]')

        if question_text and choices:
            question = Question(question_text=question_text)
            question.save()
            for choice in choices:
                question.choice_set.create(choice_text=choice)
            return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))

    # form = QuestionForm()
    return render(request, "polls/create.html")