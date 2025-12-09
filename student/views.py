from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer # основный сериализатор

    @action(detail=True, methods=['post']) # чтобы изменить статус учеников
    def set_status(self, request, pk=None):
   
        student = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["present", "absent", "none"]:
            return Response({"error": "Неверный статус"}, status=400)

        student.status = new_status
        student.save()

        return Response({"success": True, "status": student.status})
    @action(detail=False, methods=['get']) # получает список всех которые есть учеников
    def present(self, request):

        present_students = Student.objects.filter(status="a")
        serializer = self.get_serializer(present_students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get']) # получает список всех которые отсутствуют учеников
    def absent(self, request):

        no_students = Student.objects.filter(status="b") # список учеников которые нету в классе
        serializer = self.get_serializer(no_students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get']) # получает список всех неотмеченных учеников
    def none(self, request):

        none_students = Student.objects.filter(status="c") # список учеников которые не отмечены
        serializer = self.get_serializer(none_students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post']) # сброс статусов всех учеников
    def reset_statuses(self, request):

        Student.objects.all().update(status="c") # сброс статусов всех учеников на "не отмечен"
        return Response({"success": True, "message": "Статусы всех учеников сброшены."})