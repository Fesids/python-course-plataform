from django.urls import path
from . import views

urlpatterns = [
    path("course_list/", views.CourseSearchList.as_view(), name='course_list_search'),
    path("search/", views.SearchCourse.as_view(), name='search'),
    path("detail/<int:pk>/", views.CourseDetail.as_view(), name='detail_course'),
    path("update/<int:pk>/", views.CourseUpdate.as_view(), name='update_course'),
    path("delete/<int:id>/", views.CourseDelete.as_view(), name='delete_course'),
    path("new/", views.CreateCourse.as_view(), name="new_course"),
    path("own_course_list/", views.OwnCourseList.as_view(), name="own_course_list"),

    path("enroll/<int:id>/", views.EnrollStudent.as_view(), name='enroll_to_course'),
    path("courses_you_are_enroll/", views.CourseYouAreEnroll.as_view(), name='courses_you_are_enroll'),
    path("unroll/<int:id>/", views.UnrollStudents.as_view(), name="unroll_course"),

    # comments paths

    path("detail/<int:course_id>/comments/<int:comment_id>/update/", views.UpdateComment.as_view(),name="update_course_comment"),
    path("detail/<int:course_id>/comments/<int:comment_id>/delete/", views.DeleteComment.as_view(),name="delete_course_comment")
]