"""
URL configuration for spray_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from spray_backend.views import auth, boulder, circuit, gym, profile, spraywall, activity

urlpatterns = [
    path('admin/', admin.site.urls),
    path('temp_csrf_token/', auth.temp_csrf_token), # auth
    path('login/', auth.login_user), # auth
    path('signup/', auth.signup_user), # auth
    path('logout/', auth.logout_user), # auth
    path('add_gym/<int:user_id>', gym.add_gym), # gym
    path('query_gyms/', gym.query_gyms), # gym
    path('edit_gym/<int:gym_id>', gym.edit_gym), # gym
    path('choose_gym/<int:user_id>/<int:gym_id>', gym.choose_gym), # gym
    path('delete_gym/<int:gym_id>', gym.delete_gym), # gym
    path('queried_gym_spraywall/<int:gym_id>', spraywall.queried_gym_spraywall), # spraywall
    path('add_new_spraywall/<int:gym_id>', spraywall.add_new_spraywall), # spraywall
    path('delete_spraywall/<int:spraywall_id>', spraywall.delete_spraywall), # spraywall
    path('edit_spraywall/<int:spraywall_id>', spraywall.edit_spraywall), # spraywall
    path('composite/', boulder.composite), # boulder
    path('list/<int:spraywall_id>/<int:user_id>', boulder.list), # boulder
    path('add_boulder/<int:spraywall_id>/<int:user_id>', boulder.add_boulder), # boulder
    path('like_boulder/<int:boulder_id>/<int:user_id>', boulder.like_boulder), # boulder
    path('bookmark_boulder/<int:boulder_id>/<int:user_id>', boulder.bookmark_boulder), # boulder
    path('sent_boulder/<int:user_id>/<int:boulder_id>', boulder.sent_boulder), # boulder
    path('updated_boulder_data/<int:boulder_id>/<int:user_id>', boulder.updated_boulder_data), # boulder
    path('delete_boulder/<int:boulder_id>', boulder.delete_boulder), # boulder
    path('add_or_remove_boulder_in_circuit/<int:circuit_id>/<int:boulder_id>', boulder.add_or_remove_boulder_in_circuit), # boulder
    path('get_boulders_from_circuit/<int:user_id>/<int:circuit_id>', boulder.get_boulders_from_circuit), # boulder
    path('boulder_stats/<int:boulder_id>', boulder.boulder_stats), # boulder
    path('delete_logged_ascent/<int:send_id>', boulder.delete_logged_ascent), # boulder
    path('circuits/<int:user_id>/<int:spraywall_id>/<int:boulder_id>', circuit.circuits), # circuit
    path('delete_circuit/<int:user_id>/<int:spraywall_id>/<int:circuit_id>', circuit.delete_circuit), # circuit
    path('filter_circuits/<int:user_id>/<int:spraywall_id>', circuit.filter_circuits), # circuit
    path('add_profile_banner_image/<int:user_id>', profile.add_profile_banner_image), # profile
    path('get_all_user_gyms/<int:user_id>', profile.get_all_user_gyms), # profile
    path('edit_headshot/<int:user_id>', profile.edit_headshot), # profile
    path('edit_user_info/<int:user_id>', profile.edit_user_info), # profile
    path('update_user_gym/<int:user_id>', profile.update_user_gym), # profile
    path('profile_boulder_section_list/<int:spraywall_id>/<int:user_id>', profile.profile_boulder_section_list), # profile
    path('profile_stats_section/<int:user_id>/<int:spraywall_id>', profile.profile_stats_section), # profile
    path('profile_quick_data/<int:user_id>/<int:spraywall_id>', profile.profile_quick_data), # profile
    path('user_activity/<int:user_id>/<int:gym_id>', activity.user_activity), # activity
]

# serve those static image files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
