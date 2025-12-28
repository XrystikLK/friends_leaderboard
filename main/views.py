from django.shortcuts import render, redirect, get_object_or_404
from . import forms, api
from .models import Users


def index(request):
    if request.method == 'POST':
        form = forms.SteamUrlForm(request.POST)
        if form.is_valid():
            profile_url = form.cleaned_data['profile_url']
            try:
                steamid = api.get_user_steamid(profile_url)
                user_summary = api.get_user_summaries(steamid)['players'][0]
                user, created = Users.objects.update_or_create(
                    steamid=steamid,
                    defaults={
                        'personaname': user_summary.get('personaname', 'N/A'),
                        'avatar_url': user_summary.get('avatarfull', ''),
                    }
                )
                return redirect('user_profile', steamid=steamid)

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                form.add_error(None, "Не удалось найти пользователя по этой ссылке. Убедитесь, что ссылка верна.")

    else:
        form = forms.SteamUrlForm()

    context = {
        'form': form,
    }
    return render(request, 'index.html', context)


def user_profile(request, steamid):
    user = get_object_or_404(Users, steamid=steamid)
    try:
        user_summary_data = api.get_user_summaries(steamid)
        user_summary = user_summary_data['players'][0] if user_summary_data['players'] else None
    except Exception as e:
        print(f"Ошибка при получении пользователя из Steam API: {e}")
        user_summary = None

    context = {
        'user': user,
        'user_summary': user_summary,
    }
    return render(request, 'user_profile.html', context)
