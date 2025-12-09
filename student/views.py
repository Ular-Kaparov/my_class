from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        student = self.get_object()
        new_status = request.data.get("status")

        if not new_status:
            return Response({"error": "Статус не указан"}, status=400)

        if new_status not in ["present", "absent", "none"]:
            return Response({"error": "Неверный статус"}, status=400)

        student.status = new_status
        student.save()
        return Response({"success": True, "status": student.status})

    @action(detail=False, methods=['get'])
    def present(self, request):
        present_students = Student.objects.filter(status="present")
        serializer = self.get_serializer(present_students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def absent(self, request):
        absent_students = Student.objects.filter(status="absent")
        serializer = self.get_serializer(absent_students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def none(self, request):
        none_students = Student.objects.filter(status="none")
        serializer = self.get_serializer(none_students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def reset_statuses(self, request):
        Student.objects.all().update(status="none")
        return Response({"success": True, "message": "Статусы всех учеников сброшены."})
