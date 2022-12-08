from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", views.admin, name="admin"),
    path("admin/add/", views.admin_add, name="admin_add"),
    path("admin/hire/<int:id>/", views.hire, name="hire"),
    path("job_details/<int:myid>/", views.job_details, name="job_details"),
    path("apply_job/<int:myid>/", views.apply_job, name="apply_job"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("question/", views.question_edit_home, name="question_edit_home"),
    path("question/add/<int:myid>/", views.question_edit_add, name="question_edit_add"),
    path("question/delete/<int:myid>/", views.question_edit_delete, name="question_edit_delete"),
    path("question/delete/<int:myid>/<int:delid>/", views.question_edit_delete_main, name="question_edit_delete_main"),
    path("question/update/<int:myid>/", views.question_edit_update, name="question_edit_update"),
    path("question/update/<int:myid>/<int:delid>/", views.question_edit_update_main, name="question_edit_update_main"),
]