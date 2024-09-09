from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice


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
