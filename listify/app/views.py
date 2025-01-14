from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from django.core.paginator import Paginator
from django.http import JsonResponse

#Basic version
# def task_list(request):
#     tasks = Task.objects.order_by('-created_at')
#     return render(request, 'app/task_list.html', {'tasks': tasks})

#Post pagination feature
def task_list(request):
    tasks = Task.objects.order_by('-created_at')
    paginator = Paginator(tasks, 5)  # Show 5 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/task_list.html', {'page_obj': page_obj})

# def add_task(request):
#     if request.method == 'POST':
#         title = request.POST.get('title', '')
#         if title.strip():
#             Task.objects.create(title=title)
#     return redirect('task_list')

# Ajax
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            task = Task.objects.create(title=title)
            return JsonResponse({'id': task.id, 'title': task.title, 'completed': task.completed})
    return JsonResponse({'error': 'Invalid task title'}, status=400)

# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     task.delete()
#     return redirect('task_list')

# Ajax
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
